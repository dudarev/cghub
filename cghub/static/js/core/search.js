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
            // cghub.search.initFilterAccordions();
            cghub.search.initFlexigrid();
            cghub.search.initDdcl();
            cghub.search.updateCheckboxes();
            cghub.search.updateDate();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.clear-all');
            cghub.search.$filterSelects = $('select.filter-select');
        },
        bindEvents:function () {
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
            // cghub.search.$selectAllLink.on('click', cghub.search.selectAllFilterValues);
            // cghub.search.$deselectAllLink.on('click', cghub.search.deselectAllFilterValues);
            // $(window).unload(cghub.search.storeOpenedFilters);
            // $(window).load(cghub.search.reStoreOpenedFilters);
        },
        initFlexigrid: function() {
            cghub.search.$searchTable.flexigrid({height: 'auto'});
        },
        initDdcl: function() {
            for (var i = cghub.search.$filterSelects.length - 1; i >= 0; i--) {
                var select = cghub.search.$filterSelects[i];
                if ($(select).attr('section') == 'last_modified') {
                    $(select).dropdownchecklist({
                        width: 142,
                    })
                } else {
                    $(select).dropdownchecklist({
                        firstItemChecksAll: true,
                        width: 142,
                        textFormatFunction: cghub.search.ddclTextFormatFunction,
                        onComplete: cghub.search.ddclOnComplete
                    });
                    $(select).next().find('.ui-dropdownchecklist-selector').click(function() {
                        $(this).css('height', '18px')
                        $(this).find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'})
                    })
                }
                // After rendering ddcl show filters
                if (i == cghub.search.$filterSelects.length - 1) {$('.sidebar-filters').show()}
            }
        },
        ddclTextFormatFunction: function(options) {
            var countSelected = options.filter(":selected").size();
            switch (countSelected) {
                case options.size(): {
                    $(options).parent().next().find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#333'})
                    return 'All'
                };
                default: {
                    $(options).parent().next().find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'})
                    return 'selecting...';
                };
            }
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
        // storeOpenedFilters: function () {
        //     var ss = sessionStorage;
        //     $('.filter-accordion-content').each(function(i, e) {
        //         // setting storage (key:value) pair
        //         // (filters-section-name:display-attr)
        //         ss.setItem($(e).children().attr('data-filter'), $(e).css('display'));
        //     });
        // },
        // reStoreOpenedFilters: function () {
        //     var ss = sessionStorage;
        //     $('.filter-accordion-content').each(function(i, e) {
        //         var display = ss.getItem($(e).children().attr('data-filter'));
        //         if (display == 'block') {cghub.search.openFilterSection($(e).parent())}
        //     });            
        // },
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
        updateCheckboxes:function () {
            var categories = $('.filter-category');
            // loop by categories: center_name, experiment_type etc.
            var filters = URI.parseQuery(window.location.search);
            categories.each(function (i,f) {
                var filter = $(this).attr('data-filter');
                if (filter in filters){
                    var selection = filters[filter];
                    selection = selection.replace(/[)(]/g,'');
                    selection = selection.split(' OR ');
                    var values = $(this).find(':checkbox');
                    // loop by values in categories
                    values.each(function (ii,ff) {
                        if ($.inArray($(this).attr('data-value'), selection) < 0){
                            $(this).attr('checked', false);
                        } else {
                            $(this).attr('checked', 'checked');
                        };
                    });
                }
            });
        },
        updateDate:function () {
            var filters = URI.parseQuery(window.location.search);
            var last_modified_filter = filters['last_modified'];
            if (last_modified_filter.search('1DAY') > 0){
                $("#id_date_today").attr('checked', 'checked');
            };
            if (last_modified_filter.search('7DAY') > 0){
                $("#id_date_week").attr('checked', 'checked');
            };
            if (last_modified_filter.search('1MONTH') > 0){
                $("#id_date_month").attr('checked', 'checked');
            };
            if (last_modified_filter.search('1YEAR') > 0){
                $("#id_date_year").attr('checked', 'checked');
            };
        },
        applyFilters:function () {
            var href = URI(location.href);
            var new_search = URI.parseQuery(window.location.search);
            var is_error = false;
            var sections = $('select.filter-select[section != "last_modified"]');

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
            var dateQuery = $('.sidebar-filters').find('input[type = "radio"]:checked').val();
            if (dateQuery != ''){
                new_search['last_modified'] = dateQuery;
            } else {
                delete new_search['last_modified'];
            };

            // redirect to the page with filtered results
            if (!is_error){
                window.location.href = href.search(new_search);
            };
        },
        // selectAllFilterValues: function () {
        //     var checkboxes = $(this).parent().parent().find(':checkbox');
        //     checkboxes.each(function (i,f) {
        //         $(this).attr('checked', 'checked');
        //     })
        //     return false;
        // },
        // deselectAllFilterValues: function () {
        //     var checkboxes = $(this).parent().parent().find(':checkbox');
        //     checkboxes.each(function (i,f) {
        //         $(this).attr('checked', false);
        //     })
        //     return false;
        // },
        // initFilterAccordions:function() {
        //     var accordions = $.find('.filter-accordion');
        //     for (var i=0; i<accordions.length; i++) {
        //         var acc = $(accordions[i]),
        //             clickable = acc.children('.filter-accordion-header');
        //         clickable.bind('click', function() {cghub.search.openFilterSection($(this).parent())})
        //     }
        // },
        // openFilterSection: function(accordionDiv) {
        //     accordionDiv.find('.filter-accordion-content').slideToggle();
        //     accordionDiv.find('.filter-accordion-header')
        //                 .children()
        //                 .toggleClass('ui-icon-triangle-1-e ui-icon-triangle-1-s');
        // },
    };
    cghub.search.init();
});
