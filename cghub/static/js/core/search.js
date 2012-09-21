jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.search = {
        init:function () {
            cghub.search.cacheElements();
            cghub.search.bindEvents();
            cghub.search.initFlexigrid();
            cghub.search.parseFiltersFromHref();
            cghub.search.initDdcl();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.clear-all');
            cghub.search.$filterSelects = $('select.filter-select');
            cghub.search.$navbarSearchForm = $('form.navbar-search')
        },
        bindEvents:function () {
            cghub.search.$navbarSearchForm.on('submit', cghub.search.onNavbarSearchFormSubmit);
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
        },
        onNavbarSearchFormSubmit: function () {
            cghub.search.applyFilters();
            return false
        },
        parseFiltersFromHref: function () {
            var filters = URI.parseQuery(window.location.search);
            // parsing for filters
            cghub.search.$filterSelects.each(function (i, el) {
                var select = $(el),
                    section = select.attr('section');
                if (section in filters) {
                    if (section == 'last_modified') {
                        var value = filters[section];
                        select.find('option[value = "' + value + '"]').attr('selected', 'selected');
                    } else {
                        var values = filters[section].slice(1, -1).split(' OR ');
                        for (var i = values.length - 1; i >= 0; i--) {
                            select.find('option[value = "' + values[i] + '"]').attr('selected', 'selected')
                        };
                    }
                } else {
                    if (section == 'last_modified') {
                        if (window.location.search == '') {
                            select.find('option[value = "[NOW-1DAY TO NOW]"]').attr('selected', 'selected')
                        } else {
                            select.find('option[value = ""]').attr('selected', 'selected')
                        }
                    } else {
                        select.find('option[value = "(all)"]').attr('selected', 'selected')
                    }
                }
            })
            // checking for search query
            if ('q' in filters) {
                $('input.search-query').val(filters['q'])
            }
        },
        initFlexigrid: function() {
            cghub.search.$searchTable.flexigrid({height: 'auto'});
        },
        initDdcl: function() {
            for (var i = cghub.search.$filterSelects.length - 1; i >= 0; i--) {
                var select = cghub.search.$filterSelects[i];
                if ($(select).attr('section') == 'last_modified') {
                    $(select).dropdownchecklist({
                        width: 170,
                        explicitClose: 'close'
                    })
                } else {
                    $(select).dropdownchecklist({
                        firstItemChecksAll: true,
                        width: 170,
                        textFormatFunction: cghub.search.ddclTextFormatFunction,
                        onComplete: cghub.search.ddclOnComplete,
                        explicitClose: 'close'
                    });
                    $(select).next().find('.ui-dropdownchecklist-selector').click(function() {
                        $(this).css('height', '18px')
                        $(this).find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'})
                    })
                    // Fixing width bug
                    var width = $(select).next().next().width();
                    $(select).next().next().width(width + 20)
                    cghub.search.ddclOnComplete(select)
                }
            }
        },
        ddclTextFormatFunction: function(options) {
            $(options).parent().next().find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'})
            return 'selecting...';
        },
        ddclOnComplete: function(selector) {
            var preview = '',
                countSelected = 0,
                color = '#333';
            $(selector).next().next().find('.ui-dropdownchecklist-item:has(input:checked)').each(function (i, el) {
                preview += $(el).find('label').html() + '<br>'
                countSelected++;
            })
            if (countSelected == 0) {
                countSelected = 1;
                preview = 'Please select';
            }
            if (preview.indexOf('(all)') != -1) {
                countSelected = 1;
                preview = 'All';
            }
            $(selector).next().find('.ui-dropdownchecklist-selector').css('height', countSelected * 19 + 'px')
            $(selector).next().find('.ui-dropdownchecklist-text').html(preview).css({'color': color})
        },
        addFilesFormSubmit:function () {
            // collect all data attributes
            var data = {};
            var selected_files = $('input[type="checkbox"][name="selected_files"]:checked');
            selected_files.each(function (i, f) {
                var file_data = $(f).data();
                data[file_data.analysis_id] = file_data;
            });
            $.ajax({
                data:$(this).serialize() + "&attributes=" + JSON.stringify(data),
                type:$(this).attr('method'),
                dataType:'json',
                url:$(this).attr('action'),
                success:function (data) {
                    window.location.href = data.redirect;
                }
            });
            return false;
        },
        applyFilters:function () {
            var href = URI(location.href);
            var new_search = URI.parseQuery(window.location.search);
            var is_error = false;
            var sections = $('select.filter-select[section != "last_modified"]');
            var searchQuery = $('input.search-query').val();

            // loop by sections excluding date
            sections.each(function (i, section) {
                var dropContainer = $(section).next().next(),
                    all_checked = Boolean(dropContainer.find('input[value = "(all)"]:checked').length),
                    query = '',
                    section_name = $(section).attr('section');
                // Checked some boxes
                if (!all_checked && dropContainer.find('input:checked').length != 0) {
                    dropContainer.find('input:checked').each(function (j, checkbox) {
                        query += $(checkbox).val() + ' OR ';
                    });
                    new_search[section_name] = '(' + query.slice(0,-4) + ')'
                    return true;
                }

                if (all_checked) {
                    delete new_search[section_name];
                    return true;
                }
                // Nothing checked
                alert('Select some values.');
                is_error = true;
                return false;
            });
            // add date filter
            if (searchQuery == '' || window.location.search != '') {
                var dateQuery = $('.date-filters').next().next().find('input[type = "radio"]:checked').val();
                if (dateQuery != ''){
                    new_search['last_modified'] = dateQuery;
                } else {
                    delete new_search['last_modified'];
                };
            }
            // check search input
            if (searchQuery != '') {
                new_search['q'] = searchQuery
            } else {
                delete new_search['q']
            }
            console.log(new_search)
            // redirect to the page with filtered results
            if (!is_error){
                window.location.href = href.search(new_search);
            };
        },
    };
    cghub.search.init();
});
