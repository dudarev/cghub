jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.search = {
        addToCartErrorTitle: 'Error Adding to Cart',
        addToCartErrorContent: 'There was an error while adding to the cart. Please contact admin: <a href="mailto:'+cghub.vars.supportEmail+'">'+cghub.vars.supportEmail+'</a>',
        nothingSelectedTitle: 'No selected files',
        nothingSelectedContent: 'Please select some files to add them to cart',
        init:function () {
            cghub.search.cacheElements();
            cghub.search.bindEvents();
            cghub.search.initFlexigrid();
            cghub.search.parseAppliedFilters();
            cghub.search.initDdcl();
            cghub.search.initCustomPeriodButtons();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$addFilesButton = $('.add-to-cart-btn');
            cghub.search.$addAllFilesButton = $('button.add-all-to-cart-btn');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            cghub.search.$resetFiltersButton = $('button#id_reset_filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.clear-all');
            cghub.search.$filterSelects = $('select.filter-select');
            cghub.search.$navbarSearchForm = $('form.navbar-search');
            cghub.search.$messageModal = $('#messageModal');
            cghub.search.$manyItemsModal = $('#manyItemsModal');
            cghub.search.$spinner = $('.js-spinner');
            cghub.search.$numResults = $('.js-num-results');
            cghub.search.$searchField = $('.navbar-search input');
        },
        bindEvents:function () {
            cghub.search.$navbarSearchForm.on('submit', cghub.search.onNavbarSearchFormSubmit);
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
            cghub.search.$resetFiltersButton.on('click', cghub.search.resetFilters);
            cghub.search.$addAllFilesButton.on('click', cghub.search.addAllFilesClick);
            cghub.search.$manyItemsModal.find('.js-yes').on('click', cghub.search.addAllFiles);
        },
        onNavbarSearchFormSubmit: function () {
            cghub.search.applyFilters();
            return false;
        },
        parseAppliedFilters: function () {
            var filters = {};
            $('.applied-filters ul li').each(function() {
                // for not to lose '0' in sample_type
                var filters_code = $(this).data('filters');
                if (typeof(filters_code) == "number"){
                    if(filters_code < 10) {
                        filters_code = '0' + filters_code;
                    } else {
                        filters_code = '' + filters_code;
                    }
                }
                filters[$(this).data('name')] = filters_code.split('&');
            });
            cghub.search.$filterSelects.each(function (i, el) {
                var $select = $(el);
                var section = $select.attr('data-section');
                if(section in filters) {
                    if(section == 'refassem_short_name') {
                        $select.find('option').each(function(j, opt) {
                            var values = $(opt).val().split(' OR ');
                            var enable_option = true;
                            for(var i=0; i<values.length; i++) {
                                if($.inArray(values[i], filters[section]) == -1) {
                                    enable_option = false;
                                    break;
                                }
                            }
                            if(enable_option) {
                                $(opt).attr('selected', 'selected');
                            }
                        });
                    } else if (section == 'last_modified' || section == 'upload_date') {
                        var value = filters[section][0];
                        var time_filter = $select.find('option[value = "' + value + '"]');
                        if (time_filter.length > 0) {
                            time_filter.attr('selected', 'selected');
                        } else {
                            var $new_opt = $('<option/>').attr({'selected': 'selected','value': value})
                                .text(cghub.search.convertValueToPeriod(value));
                            $select.append($new_opt);
                        }
                    } else {
                        for(var i=0; i<filters[section].length; i++) {
                            $select.find('option[value="' + filters[section][i] + '"]').attr('selected', 'selected');
                        }
                    }
                } else {
                    /* for date filters */
                    $select.find('option[value=""]').attr('selected', 'selected');
                    /* for other filters */
                    $select.find('option[value="(Toggle all)"]').attr('selected', 'selected');
                }
            });
            // clear search query according to Bug #1829
            $('input.search-query').val('');
        },
        initFlexigrid: function() {
            cghub.search.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid .bDiv tr').contextmenu();
            $('.data-table').css('visibility', 'visible');
            /* add fieldset element */
            var $data_table = $('.bDiv table');
            $data_table.wrap($('<fieldset/>'));
            $data_table.parent().prepend($('<legend class="hidden">Select files to add to cart:</legend>'));
            /* disable sort link by files size, ticket #298 RM2220
            TODO: fix this in future */
            $('#id-col-files_size .sort-link').on('click', function() {return false;});
        },
        initDdcl: function() {
            for (var i=0; i<cghub.search.$filterSelects.length; i++) {
                var select = cghub.search.$filterSelects[i];
                if ($(select).hasClass('date-filters')) {
                    $(select).dropdownchecklist({
                        width: 180,
                        zIndex: 1010,
                        explicitClose: 'close'
                    });
                } else {
                    $(select).dropdownchecklist({
                        firstItemChecksAll: true,
                        width: 180,
                        zIndex: 1010,
                        textFormatFunction: cghub.search.ddclTextFormatFunction,
                        onComplete: cghub.search.ddclOnComplete,
                        explicitClose: 'close'
                    });
                    // Fixing width bug
                    var width = $(select).next().next().width();
                    $(select).next().next().width(width + 30);
                    cghub.search.ddclOnComplete(select);
                }
                // Bug #1982, connect <label> and ui-dropdownchecklist-selector by attaching id to selector
                $(select).attr("id", $(select).prev().attr('for'));
            }
            $('.sidebar').css('visibility', 'visible');
            /* fix for IE, saves focus on current element */
            if($.browser.msie) {
                $(document).on('keydown', '.ui-dropdownchecklist-dropcontainer', function(e) {
                    if(e.which == 13) {
                        return false;
                    }
                });
            }
        },
        ddclTextFormatFunction: function(options) {
            return;
        },
        ddclOnComplete: function(selector) {
            var preview = '',
                countSelected = 0,
                color = '#333';
            $(selector).next().next().find('.ui-dropdownchecklist-item:has(input:checked)').each(function (i, el) {
                preview += '<span class="ui-dropdownchecklist-text-item">' + $(el).find('label').html() + '</span><br>';
                countSelected++;
            });
            if (countSelected === 0) {
                countSelected = 1;
                preview = 'Please select';
            }
            if (preview.indexOf('(Toggle all)') != -1) {
                countSelected = 1;
                preview = 'All';
            }
            $(selector).next().find('.ui-dropdownchecklist-selector').css('height', 'auto');
            $(selector).next().find('.ui-dropdownchecklist-text').html(preview).css({'color': color});
        },
        addFilesFormSubmit:function () {
            // disable button
            if(cghub.search.$addFilesButton.hasClass('disabled')) return false;
            cghub.search.$addFilesButton.addClass('disabled');
            cghub.search.$spinner.show();
            // collect all data attributes
            var data = [];
            var selected_files = $('input[type="checkbox"][name="selected_files"]:checked');

            // show message if nothing selected
            if (selected_files.length == 0) {
                cghub.base.showMessage(cghub.search.nothingSelectedTitle, cghub.search.nothingSelectedContent);
                cghub.search.$addFilesButton.removeClass('disabled');
                cghub.search.$spinner.hide();
                return false;
            }

            selected_files.each(function (i, f) {
                data.push($(f).data());
            });
            $.ajax({
                data:$(this).serialize() + "&selected_items=" + JSON.stringify(data),
                type:$(this).attr('method'),
                dataType:'json',
                url:$(this).attr('action'),
                success:function (data) {
                    if (data['action']=='redirect') {
                        window.location.href = data['redirect'];
                    } else {
                        cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                        cghub.search.$addFilesButton.removeClass('disabled');
                        cghub.search.$spinner.hide();
                    }
                },
                error:function (){
                    cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                    cghub.search.$addFilesButton.removeClass('disabled');
                    cghub.search.$spinner.hide();
                }
            });
            return false;
        },
        addAllFilesClick:function () {
            if($(this).hasClass('disabled')) return false;
            var files_count = parseInt(cghub.search.$numResults.text(), 10);
            var many_files = parseInt($(this).parents('form').data('many-files'));
            if(files_count > many_files) {
                cghub.search.$manyItemsModal.find('.modal-body p b').text(files_count);
                cghub.search.$manyItemsModal.modal('show');
                cghub.search.$manyItemsModal.find('.js-no').focus();
            } else {
                cghub.search.addAllFiles();
            }
            return false;
        },
        addAllFiles:function() {
            var filters = URI.parseQuery(window.location.search);
            if(jQuery.isEmptyObject(filters)) {
                var filters_values = cghub.search.getFiltersValues();
                if(filters_values['is_error']) {
                    return false;
                }
                filters = filters_values['filters'];
            }
            var $button = cghub.search.$addAllFilesButton;
            $button.addClass('disabled');
            cghub.search.$spinner.show();
            var $form = $button.parents('form');
            $.ajax({
                data:$form.serialize() + '&filters=' + JSON.stringify(filters),
                type:$form.attr('method'),
                dataType:'json',
                url:$form.attr('action'),
                success:function (data) {
                    if (data['action']=='redirect') {
                        window.location.href = data['redirect'];
                    }
                    if (data['action']=='message') {
                        cghub.base.showMessage(data['title'], data['content']);
                        $($button).removeClass('disabled');
                        cghub.search.$spinner.hide();
                    }
                    if (data['action']=='error') {
                        cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                        $($button).removeClass('disabled');
                        cghub.search.$spinner.hide();
                    }
                },
                error:function (){
                    cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                    $($button).removeClass('disabled');
                    cghub.search.$spinner.hide();
                }
            });
            cghub.search.$manyItemsModal.modal('hide');
            return false;
        },
        getFiltersValues:function () {
            var new_search = URI.parseQuery(window.location.search);
            var is_error = !cghub.search.checkSearchField();
            var sections = $('select.filter-select:not(.date-filters)');
            var searchQuery = $('input.search-query').val();

            if(searchQuery=='Search') {
                searchQuery = '';
            }
            // loop by sections excluding date
            sections.each(function (i, section) {
                var dropContainer = $(section).next().next(),
                    all_checked = Boolean(dropContainer.find('input[value = "(Toggle all)"]:checked').length),
                    query = '',
                    section_name = $(section).attr('data-section');
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
                    var dateQuery = $(this).find('option:selected').val();
                    if (dateQuery !== ''){
                        new_search[$(this).attr('data-section')] = dateQuery;
                    } else {
                        delete new_search[$(this).attr('data-section')];
                    }
                });
            }
            // check search input
            if (searchQuery !== '') {
                new_search['q'] = searchQuery;
            } else {
                delete new_search['q'];
            }
            
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
            var url = $(this).data('url');
            $.removeCookie('last_query', { path: url });
            window.location.href = url;
            $(this).blur();
        },
        createCustomDatepickers:function() {
            $('.dp-container').remove();
            var $dp_container = $('<div/>').addClass('dp-container well');
            var $block_label = $('<h6/>').text('Please select the period');
            var $start_dp = $('<div class="dp-date" id="dp-start" data-defaultdate="+0d">');
            var $end_dp = $('<div class="dp-date" id="dp-end" data-defaultdate="+0d">');
            var $btn_submit = $('<button/>').addClass('btn-submit btn').attr('type', 'submit').text('Submit');
            var $btn_cancel = $('<button/>').addClass('btn-cancel btn').text('Cancel');

            $.each([$block_label, $start_dp, $end_dp, $('<br/>'), $btn_submit, $btn_cancel], function(i,e) {
                $(this).appendTo($dp_container)
            });
            $.each([$start_dp, $end_dp], function(i,e){
                var $d = $(this);
                $d.datepicker({
                    changeMonth: true,
                    changeYear: true,
                    defaultDate: $d.data('defaultdate'),
                    yearRange: "c-2y:c",
                    dateFormat: 'yy/mm/dd',
                    onChangeMonthYear:function(year, month, inst){
                        // calculate days in selected month
                        var daysInMonth = new Date(year, month, 0).getDate();
                        var currentDate = $d.datepicker("getDate");
                        if (currentDate.getDate() > daysInMonth) {
                            currentDate.setMonth(month-1, daysInMonth);
                        } else {
                            currentDate.setMonth(month-1);
                        }
                        currentDate.setYear(year);
                        $d.datepicker("setDate", currentDate);
                    }
                });
            });
            return $dp_container;
        },
        initCustomPeriodButtons:function() {
            /* add 'Pick period' buttons before 'close' button */
            $('.sidebar input[value="[NOW-1YEAR TO NOW]"]').each(function(n, obj){
                $(obj).parent().parent().find('.ui-dropdownchecklist-close')
                .before($('<div class="ui-state-default ui-dropdownchecklist-item js-pick-period" style="text-align: center">' +
                '<span class="ui-dropdownchecklist-text">Pick period</span></div>').hover(function() {
                    $(this).addClass('ui-state-hover');
                }, function() {
                    $(this).removeClass('ui-state-hover');
                }).click(function() {
                    var $datepickers = cghub.search.createCustomDatepickers()
                        .css('top', $(obj).parents('.ui-dropdownchecklist-dropcontainer-wrapper')
                        .offset().top - 40).appendTo('.sidebar');
                    $datepickers.find('.btn-cancel').click(function() {
                        $datepickers.remove();
                        return false;
                    });
                    $datepickers.find('.btn-submit').click(function() {
                        var $start_date = $datepickers.find('#dp-start').datepicker({ dateFormat: 'yy/mm/dd' }).val();
                        var $end_date = $datepickers.find('#dp-end').datepicker({ dateFormat: 'yy/mm/dd' }).val();
                        var date_query = cghub.search.convertPeriodToValue($start_date, $end_date);
                        var $block = $(obj).parents('.ui-dropdownchecklist-dropcontainer-wrapper');
                        var $select = $block.prev().prev();
                        $block.find('input').prop('checked', false).change(function() {
                            // select clicked option
                            $select.find('option').attr('selected', false);
                            $select.find('option[value = "' + $(this).val() + '"]').attr('selected', 'selected');
                            // delete custom period option
                            $select.find('.js-custom-option').remove();
                            $select.dropdownchecklist("refresh");
                        });
                        $select.find('option').attr('selected', false);
                        $select.find('.js-custom-option').remove();
                        $select.append($('<option/>')
                                .attr({'value': date_query,'selected': 'selected'})
                                .text(cghub.search.convertValueToPeriod(date_query))
                                .addClass('js-custom-option'));
                        $select.dropdownchecklist("refresh");
                        $datepickers.remove();
                        return false;
                    });
                }));
            });
        },
        convertPeriodToValue:function(start_date, end_date) {
            var MS = 86400000; // ms in one day
            var current = new Date();
            var current_parsed = Date.parse(current);
            var end_parsed = Date.parse(end_date);
            var start_parsed = Date.parse(start_date);
            $('.dp-container > .text-error').remove();
            if (start_parsed > current_parsed) {
                start_parsed = current_parsed;
            }
            if (end_parsed > current_parsed) {
                end_parsed = current_parsed;
            }
            if (end_parsed < start_parsed) {
                var buf = start_parsed;
                start_parsed = end_parsed;
                end_parsed = buf;
            }
            var now_to_end = Math.floor(( current_parsed - end_parsed) / MS);
            var start_to_now = Math.floor(( current_parsed - start_parsed) / MS);
            if(start_to_now == now_to_end) {start_to_now += 1;}
            var start_str = '[NOW-' + start_to_now + 'DAY';
            var end_str = 'NOW-' + now_to_end + 'DAY]';
            if ((current_parsed - end_parsed)/MS < 1) { end_str = 'NOW]'; }
            return start_str + ' TO ' + end_str;
        },
        convertValueToPeriod:function(value) {
            var MS = 86400000;
            var current = new Date();
            var current_parsed = Date.parse(current);
            // Get the number of days
            var values = value.slice(1, -1).split(' TO ');
            var start_now = parseInt(values[0].split('-').reverse()[0].slice(0, -3));
            var end_now = parseInt(values[1].split('-').reverse()[0].slice(0, -3));
            // Convert each to date objects
            isNaN(start_now) ? start_now = 0 : start_now = start_now * MS;
            isNaN(end_now) ? end_now = 0 : end_now = end_now * MS;
            var start_date = new Date(current_parsed - start_now);
            var end_date = new Date(current_parsed - end_now);
            start_date = $.datepicker.formatDate('yy/mm/dd', start_date);
            end_date = $.datepicker.formatDate('yy/mm/dd', end_date);
            return start_date + ' - ' + end_date;
        },
        checkSearchField:function(){
            var searchValue = cghub.search.$searchField.val();
            for (var i = 0; i < cghub.base.reservedChars.length; i++){
                if (searchValue.indexOf(cghub.base.reservedChars[i]) != -1){
                    cghub.base.showMessage(cghub.base.usedReservedCharsTitle, cghub.base.usedReservedCharsContent);
                    return false;
                }
            }
            return true;
        },
    };
    cghub.search.init();
});
