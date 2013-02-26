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
            var $block_label = $('<h6/>').text('Please select the period.');
            var $start_dp = $('<div class="dp-date" id="dp-start" data-defaultdate="-1y">');
            var $end_dp = $('<div class="dp-date" id="dp-end" data-defaultdate="+0d">');
            var $btn_submit = $('<button/>').addClass('btn-submit btn').attr('type', 'submit').text('Submit');
            var $btn_cancel = $('<button/>').addClass('btn-cancel btn').text('Cancel');

            $.each([$block_label, $start_dp, $end_dp, $('<br/>'), $btn_submit, $btn_cancel], function(i,e) {
                $(this).appendTo($dp_container)
            });
            $.each(([$start_dp, $end_dp]), function(i,e){
                var $d = $(this);
                $d.datepicker({
                    changeMonth: true,
                    changeYear: true,
                    defaultDate: $d.data('defaultdate'),
                    yearRange: "-5y:2013",
                });
            });
            $('.sidebar').append($dp_container);
        },
        convertCustomPeriod:function(start_date, end_date) {
            var ms = 86400000;
            var current = new Date();
            var current_parsed = Date.parse(current);
            var end_parsed = Date.parse(end_date);
            var start_parsed = Date.parse(start_date);

            $('.dp-container > .text-error').remove();
            if (start_parsed > end_parsed || end_parsed > current_parsed || start_parsed > current_parsed) {
                $('.dp-container').append($('<span/>').addClass('text-error').text('Selected range is incorrect.'));
                return false;
            } else {
                var now_to_end = Math.floor(( current_parsed - end_parsed) / ms);
                var start_to_now = Math.floor(( current_parsed - start_parsed) / ms);
                var start_str = '[NOW-' + start_to_now + 'DAY';
                var end_str = 'NOW-' + now_to_end + 'DAY]';
                if ((current_parsed - start_parsed)/ms < 0.6) { start_str = '[NOW' };
                if ((current_parsed - end_parsed)/ms < 0.6) { end_str = 'NOW]' };
                var result = start_str + ' TO ' + end_str;
                return result;
            }
        },
        createNewMenuItem:function(item) {
            var $dp_container = $('.dp-container');
            var $start_date = $('#dp-start').datepicker({ dateFormat: 'dd/mm/yyyy' }).val();
            var $end_date = $('#dp-end').datepicker({ dateFormat: 'dd/mm/yyyy' }).val();
            var $new_container = $('<div class="ui-dropdownchecklist-item ui-state-default" style="white-space: nowrap;">');

            var new_name = item.attr('id').slice(0, -3);
            var new_index = item.parent().siblings().length;
            var new_id = item.attr('id').slice(0, -1) + new_index;
            var date_query = cghub.search.convertCustomPeriod($start_date, $end_date);

            if (date_query) {
                var $new_input = $('<input class="active" type="radio" tabindex="0" disabled=""/>')
                    .attr({
                        'value': date_query,
                        'id': new_id,
                        'name': new_name,
                        'index': new_index,
                        'checked': 'checked'
                    });
                var $new_label = $('<label class="ui-dropdownchecklist-text" style="cursor: default;"></label>').attr('for', new_id).text($start_date + ' -');
                $new_label.append($('<br/>')).append($('<span/>').text($end_date));
                $new_input.appendTo($new_container);
                $new_label.appendTo($new_container);
                $new_container.insertBefore(item.parent('.ui-dropdownchecklist-item').siblings().last());
                $dp_container.fadeOut();
            }
        },
        customPeriodEvents:function() {
            var $dp_container = $('.dp-container');
            var $custom_period =  $('input[value=custom_period]');

            $custom_period.on('change', function() {
                var $item = $(this); // Menu item that is being clicked
                $dp_container.fadeIn();
                $('.btn-cancel').unbind('click').on('click', function() { $dp_container.fadeOut(); });
                $('.btn-submit').unbind('click').on('click', function() { cghub.search.createNewMenuItem($item); });
            });
        }
    };
    cghub.search.init();
});
