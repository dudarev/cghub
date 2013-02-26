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
            cghub.search.createPeriodDatepickers();
            cghub.search.customPeriodEvents();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$addAllFilesButton = $('button.add-all-to-cart-btn');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            cghub.search.$resetFiltersButton = $('button#id_reset_filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.clear-all');
            cghub.search.$filterSelects = $('select.filter-select');
            cghub.search.$navbarSearchForm = $('form.navbar-search');
        },
        bindEvents:function () {
            cghub.search.$navbarSearchForm.on('submit', cghub.search.onNavbarSearchFormSubmit);
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
            cghub.search.$resetFiltersButton.on('click', cghub.search.resetFilters);
            cghub.search.$addAllFilesButton.on('click', cghub.search.addAllFilesClick);
        },
        onNavbarSearchFormSubmit: function () {
            cghub.search.applyFilters();
            return false;
        },
        parseFiltersFromHref: function () {
            var filters = URI.parseQuery(window.location.search);
            // parsing for filters
            cghub.search.$filterSelects.each(function (i, el) {
                var select = $(el),
                    section = select.attr('section');
                if (section in filters) {
                    if (section == 'last_modified' || section == 'upload_date') {
                        var value = filters[section];
                        select.find('option[value = "' + value + '"]').attr('selected', 'selected');
                    } else {
                        var values = filters[section].slice(1, -1).split(' OR ');
                        if(section == 'refassem_short_name') {
                            for (var i = values.length - 1; i >= 0; i--) {
                                select.find('option[value *= "' + values[i] + '"]').attr('selected', 'selected');
                            }
                        } else {
                            for (var i = values.length - 1; i >= 0; i--) {
                                select.find('option[value = "' + values[i] + '"]').attr('selected', 'selected');
                            }
                        }
                    }
                } else {
                    if (section == 'upload_date') {
                        if (window.location.search === '') {
                            select.find('option[value = "[NOW-7DAY TO NOW]"]').attr('selected', 'selected');
                        } else {
                            select.find('option[value = ""]').attr('selected', 'selected');
                        }
                    } else if (section == 'state') {
                        if (window.location.pathname.indexOf('search') > 0) {
                            select.find('option[value = "(all)"]').attr('selected', 'selected');
                        } else {
                            // default state to live
                            select.find('option[value = "live"]').attr('selected', 'selected');
                        }
                    } else {
                        select.find('option[value = "(all)"]').attr('selected', 'selected');
                    }
                }
            });

            var modified_filter_applied = $('#modified-filter-applied').attr('data');
            $(".date-filters[section='last_modified']").find('option[value = "' + modified_filter_applied + '"]').attr('selected', 'selected');
            var uploaded_filter_applied = $('#uploaded-filter-applied').attr('data');
            $(".date-filters[section='upload_date']").find('option[value = "' + uploaded_filter_applied + '"]').attr('selected', 'selected');

            // checking for search query
            if ('q' in filters) {
                $('input.search-query').val(filters['q']);
            }
        },
        initFlexigrid: function() {
            cghub.search.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid .bDiv tr').contextmenu();
        },
        initDdcl: function() {
            for (var i = cghub.search.$filterSelects.length - 1; i >= 0; i--) {
                var select = cghub.search.$filterSelects[i];
                if ($(select).hasClass('date-filters')) {
                    $(select).dropdownchecklist({
                        width: 170,
                        explicitClose: 'close'
                    });
                } else {
                    $(select).dropdownchecklist({
                        firstItemChecksAll: true,
                        width: 170,
                        textFormatFunction: cghub.search.ddclTextFormatFunction,
                        onComplete: cghub.search.ddclOnComplete,
                        explicitClose: 'close'
                    });
                    $(select).next().find('.ui-dropdownchecklist-selector').click(function() {
                        $(this).css('height', '18px');
                        $(this).find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'});
                    });
                    // Fixing width bug
                    var width = $(select).next().next().width();
                    $(select).next().next().width(width + 20);
                    cghub.search.ddclOnComplete(select);
                }
            }
        },
        ddclTextFormatFunction: function(options) {
            $(options).parent().next().find('.ui-dropdownchecklist-text').html('selecting...').css({'color': '#08c'});
            return 'selecting...';
        },
        ddclOnComplete: function(selector) {
            var preview = '',
                countSelected = 0,
                color = '#333';
            $(selector).next().next().find('.ui-dropdownchecklist-item:has(input:checked)').each(function (i, el) {
                preview += $(el).find('label').html() + '<br>';
                countSelected++;
            });
            if (countSelected === 0) {
                countSelected = 1;
                preview = 'Please select';
            }
            if (preview.indexOf('(all)') != -1) {
                countSelected = 1;
                preview = 'All';
            }
            $(selector).next().find('.ui-dropdownchecklist-selector').css('height', countSelected * 19 + 'px');
            $(selector).next().find('.ui-dropdownchecklist-text').html(preview).css({'color': color});
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
                    if (!data['success']) {
                        $('#errorAddCartModal').modal();
                    } else {
                        window.location.href = data['redirect'];
                    }
                },
                error:function (){
                    $('#errorAddCartModal').modal();
                }
            });
            return false;
        },
        addAllFilesClick:function () {
            if($(this).hasClass('disabled')) return false;
            $(this).addClass('disabled');
            var $form = $(this).parents('form');
            var attributes = [];
            for (var key in $($form.find('input[type="checkbox"][name="selected_files"]')[0]).data()) {
                attributes.push(key);
            }
            var filters = URI.parseQuery(window.location.search);
            if(jQuery.isEmptyObject(filters)) {
                filters = cghub.search.getFiltersValues()['filters'];
            }
            $.ajax({
                data:$form.serialize() + '&attributes=' + JSON.stringify(attributes) + '&filters=' + JSON.stringify(filters),
                type:$form.attr('method'),
                dataType:'json',
                url:$form.attr('action'),
                success:function (data) {
                    if (!data['success']) {
                        $('#errorAddCartModal').modal();
                    } else {
                        window.location.href = data['redirect'];
                    }
                },
                error:function (){
                    $('#errorAddCartModal').modal();
                }
            });
            return false;
        },
        getFiltersValues:function () {
            var new_search = URI.parseQuery(window.location.search);
            var is_error = false;
            var sections = $('select.filter-select:not(.date-filters)');
            var searchQuery = $('input.search-query').val();

            // loop by sections excluding date
            sections.each(function (i, section) {
                var dropContainer = $(section).next().next(),
                    all_checked = Boolean(dropContainer.find('input[value = "(all)"]:checked').length),
                    query = '',
                    section_name = $(section).attr('section');
                // Checked some boxes
                if (!all_checked && dropContainer.find('input:checked').length !== 0) {
                    dropContainer.find('input:checked').each(function (j, checkbox) {
                        query += $(checkbox).val() + ' OR ';
                    });
                    new_search[section_name] = '(' + query.slice(0,-4) + ')';
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
            if (searchQuery === '' || window.location.search !== '') {
                $('.date-filters').each(function() {
                    var dateQuery = $(this).next().next().find('input[type = "radio"]:checked').val();
                    if (dateQuery !== ''){
                        new_search[$(this).attr('section')] = dateQuery;
                    } else {
                        delete new_search[$(this).attr('section')];
                    }
                });
            }
            // check search input
            if (searchQuery !== '') {
                new_search['q'] = searchQuery;
            } else {
                delete new_search['q'];
            }
            
            delete new_search['limit'];
            delete new_search['offset'];
            // redirect to the page with filtered results
            return {'is_error': is_error, 'filters': new_search};
        },
        applyFilters:function () {
            var filters = cghub.search.getFiltersValues();
            var href = URI(location.href);
            if(!filters['is_error']) {
                window.location.href = href.search(filters['filters']);
            }
            $(this).blur();
        },
        resetFilters:function() {
            window.location.href = "/";
            $(this).blur();
        },
        createPeriodDatepickers:function() {
            var $dp_container = $('<div/>').css('display', 'none').addClass('dp-container well');
            var $start_input = $('<input type="text" name="startdate" id="startdate"/>').css('display', 'none');
            var $end_input = $('<input type="text" name="enddate" id="enddate"/>').css('display', 'none');
            var $block_label = $('<h6/>').text('Please select the period.');
            var $start_div = $('<div class="dp-date" data-altfield="#startdate" data-defaultdate="-1y">');
            var $end_div = $('<div class="dp-date" data-altfield="#enddate" data-defaultdate="+0d">');
            var $btn_submit = $('<button/>').addClass('btnSubmit btn').attr('type', 'submit').text('Submit');
            var $btn_cancel = $('<button/>').addClass('btnCancel btn').text('Cancel');

            $.each([$start_input, $end_input, $block_label, $start_div, $end_div, $('<br/>'), $btn_submit, $btn_cancel], function(i,e) {
                $(this).appendTo($dp_container)
            });
            $.each(([$start_div, $end_div]), function(i,e){
                var $d = $(this);
                $d.datepicker({
                    changeMonth: true,
                    changeYear: true,
                    altField: $d.data('altfield'),
                    defaultDate: $d.data('defaultdate'),
                    yearRange: "-5y:2013",
                });
            });
            $('.sidebar').append($dp_container);
        },
        customPeriodEvents:function() {
            var $dp_container = $('.dp-container');
            var $custom_period =  $('input[value=custom_period]');

            $custom_period.on('change', function() {
                $dp_container.fadeIn();
            });
            $('.btnCancel').on('click', function(){
                $dp_container.fadeOut();
            });
        }
    };
    cghub.search.init();
});
