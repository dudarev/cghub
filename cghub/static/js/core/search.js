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
        spaceStr: '\xa0\xa0\xa0\xa0',
        init:function () {
            cghub.search.cacheElements();
            cghub.search.bindEvents();
            cghub.search.initFlexigrid();
            cghub.search.parseAppliedFilters();
            cghub.search.initDdcl();
            cghub.search.initCustomPeriodButtons();
            cghub.search.initRememberFilters();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$addFilesForm = $('#id_add_files_form');
            cghub.search.$addFilesButton = $('.add-to-cart-btn');
            cghub.search.$addAllFilesButton = $('button.add-all-to-cart-btn');
            cghub.search.$applyFiltersButton = $('button.js-apply-filters');
            cghub.search.$resetFiltersButton = $('button.js-reset-filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.clear-all');
            cghub.search.$filterSelects = $('select.filter-select');
            cghub.search.$navbarSearchForm = $('form.navbar-search');
            cghub.search.$messageModal = $('#messageModal');
            cghub.search.$manyItemsModal = $('#manyItemsModal');
            cghub.search.$numResults = $('.js-num-results');
            cghub.search.$searchField = $('.navbar-search input');
            cghub.search.$rememberFiltersCheckbox = $('.js-remember-filters input');
        },
        bindEvents:function () {
            cghub.search.$navbarSearchForm.on('submit', cghub.search.onNavbarSearchFormSubmit);
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
            cghub.search.$resetFiltersButton.on('click', cghub.search.resetFilters);
            cghub.search.$addAllFilesButton.on('click', cghub.search.addAllFilesClick);
            cghub.search.$manyItemsModal.find('.js-yes').on('click', cghub.search.addAllFiles);
        },
        initRememberFilters: function() {
            var remember = sessionStorage.getItem('remember-filters');
            if(remember===null) {remember = 'true'};
            cghub.search.$rememberFiltersCheckbox.prop('checked', remember == 'true');
            cghub.search.$rememberFiltersCheckbox.on('change', function() {
                sessionStorage.setItem('remember-filters', $(this).prop('checked'));
            })
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
        updateRootItemValue: function(root) {
            /* used by hierarchical filters, ticket:395 */
            if(!root) return;
            var unchecked = 0;
            var next = root.next();
            var level = root.data('level') + 1;
            while(parseInt(next.data('level')) == level) {
                if(!next.find('input').prop('checked')) {
                    unchecked += 1;
                    break;
                }
                next = next.next();
            }
            if (unchecked == 0) {
                root.find('input').prop('checked', true);
            } else {
                root.find('input').prop('checked', false);
            }
            /* update higher roots */
            if(level > 1) {
                while (parseInt(root.data('level')) == level - 1) {
                    root = root.prev();
                    if (!root) {
                        break;
                    }
                }
                cghub.search.updateRootItemValue(root);
            }
        },
        updateToggleAll: function(item) {
            /* update toggle all */
            var unchecked = 0;
            item.parent().find('.ui-dropdownchecklist-item:not(:first)').each(function(i, f) {
                if($(f).find('input').prop('checked') == false) {
                    unchecked += 1;
                }
            })
            item.parent().find('.ui-dropdownchecklist-item').first().find('input').prop('checked', !Boolean(unchecked));
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
                    /* add space for subitems */
                    cghub.search.$filterSelects.each(function(i, f) {
                        var previous_space = '';
                        var previous_option = undefined;
                        $(f).find('option').each(function(i, f) {
                            var text = $.trim($(f).text());
                            var space = '';
                            while(text.indexOf('-') == 0) {
                                space += cghub.search.spaceStr;
                                text = text.substring(1);
                            }
                            if(space.length) {
                                $(f).text(space + text);
                                /* roots should have empty query */
                                if(space.length > previous_space.length) {
                                    previous_option.attr('value', '');
                                }
                            }
                            previous_space = space;
                            previous_option = $(f);
                        })
                    });
                    $(select).dropdownchecklist({
                        firstItemChecksAll: true,
                        width: 180,
                        zIndex: 1010,
                        textFormatFunction: cghub.search.ddclTextFormatFunction,
                        onComplete: cghub.search.ddclOnComplete,
                        explicitClose: 'close'
                    });
                    /* Fixing width bug */
                    var width = $(select).next().next().width();
                    $(select).next().next().width(width + 30);
                    cghub.search.ddclOnComplete(select);
                }
                /* Bug #1982, connect <label> and ui-dropdownchecklist-selector by attaching id to selector */
                $(select).attr("id", $(select).prev().attr('for'));
            }
            /* multiselect feature for hierarchical filters, ticket:395 */
            $('#filters-bar .ui-dropdownchecklist-item label').each(function(i, f) {
                var level = $(f).text().split(cghub.search.spaceStr).length - 1;
                $(f).parent().attr('data-level', level);
            });
            $('#filters-bar .ui-dropdownchecklist-item input[type="checkbox"][value=""]').each(function(i, f) {
                cghub.search.updateRootItemValue($(f).parent());
            });
            $('#filters-bar .ui-dropdownchecklist-item input[type="checkbox"][value=""]').on('change', function(f) {
                var list_item = $(f.target).parent();
                var level = parseInt(list_item.data('level'));
                var next = list_item.next();
                var new_val = $(f.target).prop('checked');
                while(parseInt(next.data('level')) > level) {
                    next.find('input').prop('checked', new_val);
                    next = next.next();
                }
                if(level > 0) {
                    while (parseInt(list_item.data('level')) < level) {
                        list_item = list_item.prev();
                        if(!list_item) {
                            break;
                        }
                    }
                    cghub.search.updateRootItemValue(list_item);
                }
                cghub.search.updateToggleAll(list_item);
            });
            $('#filters-bar .ui-dropdownchecklist-item input[type="checkbox"]:not([value=""])').on('change', function(f) {
                var list_item = $(f.target).parent();
                var level = parseInt(list_item.data('level'));
                if (level > 0) {
                    /* count of checked subitems */
                    var root = list_item.prev()
                    while (parseInt(root.data('level')) == level) {
                        root = root.prev();
                    }
                    cghub.search.updateRootItemValue(root);
                }
                if($(f.target).val() != '(Toggle all)') {
                    cghub.search.updateToggleAll(list_item);
                }
            });
            /* show ddcls */
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
                var $el = $(el);
                if($el.find('input').val().length) {
                    /* skip root elements */
                    preview += '<span class="ui-dropdownchecklist-text-item">' +
                            $el.find('label').html().split('&nbsp;').join('') +
                            '</span><br>';
                }
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
            // collect all data attributes
            cghub.selected.save()

            // show message if nothing selected
            if (!cghub.selected.exists) {
                cghub.base.showMessage(cghub.search.nothingSelectedTitle, cghub.search.nothingSelectedContent);
                cghub.search.$addFilesButton.removeClass('disabled');
                cghub.base.hideSpinner();
                return false;
            }

            cghub.base.showSpinner();

            $.ajax({
                data:$(this).serialize() + "&selected_items=" + JSON.stringify(cghub.selected.get_data_list()),
                type:$(this).attr('method'),
                dataType:'json',
                url:$(this).attr('action'),
                success:function (data) {
                    if (data['action']=='redirect') {
                        window.location.href = data['redirect'];
                    }
                    if (data['action']=='message') {
                        cghub.search.$addFilesButton.removeClass('disabled');
                        cghub.base.hideSpinner();
                        cghub.base.showMessage(data['title'], data['content']);
                    }
                    if (data['action']=='error') {
                        cghub.search.$addFilesButton.removeClass('disabled');
                        cghub.base.hideSpinner();
                        cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                    }
                },
                error:function (){
                    cghub.search.$addFilesButton.removeClass('disabled');
                    cghub.base.hideSpinner();
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
            cghub.base.showSpinner();
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
                        $($button).removeClass('disabled');
                        cghub.base.hideSpinner();
                        cghub.base.showMessage(data['title'], data['content']);
                    }
                    if (data['action']=='error') {
                        $($button).removeClass('disabled');
                        cghub.base.hideSpinner();
                        cghub.base.showMessage(cghub.search.addToCartErrorTitle, cghub.search.addToCartErrorContent);
                    }
                },
                error:function (){
                    $($button).removeClass('disabled');
                    cghub.base.hideSpinner();
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
                    query = [],
                    section_name = $(section).attr('data-section');
                // Checked some boxes
                if (!all_checked && dropContainer.find('input:checked').length !== 0) {
                    dropContainer.find('input:checked').each(function (j, checkbox) {
                        if($(checkbox).val().length) {
                            query.push($(checkbox).val());
                        };
                    });
                    new_search[section_name] = '(' + query.join(' OR ') + ')';
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
            var href = URI(cghub.search.$applyFiltersButton.data('search-url'));
            if(!filters['is_error']) {
                if(cghub.search.$rememberFiltersCheckbox.prop('checked')) {
                    filters['filters']['remember'] = 'true';
                } else {
                    delete filters['filters']['remember'];
                }
                if($.isEmptyObject(filters['filters'])) {
                    window.location.href = href;
                } else {
                    window.location.href = href.search(filters['filters']);
                }
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
                    maxDate: cghub.base.toUTC(new Date),
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
            var now_utc = cghub.base.toUTC(new Date());
            var end_parsed = Date.parse(end_date);
            var start_parsed = Date.parse(start_date);
            $('.dp-container > .text-error').remove();
            if (start_parsed > now_utc) {
                start_parsed = now_utc;
            }
            if (end_parsed > now_utc) {
                end_parsed = now_utc;
            }
            if (end_parsed < start_parsed) {
                var buf = start_parsed;
                start_parsed = end_parsed;
                end_parsed = buf;
            }
            var now_to_end = Math.floor(( now_utc - end_parsed) / MS);
            var start_to_now = Math.floor(( now_utc - start_parsed) / MS);
            if(start_to_now == now_to_end) {start_to_now += 1;}
            var start_str = '[NOW-' + start_to_now + 'DAY';
            var end_str = 'NOW-' + now_to_end + 'DAY]';
            if ((now_utc - end_parsed)/MS < 1) { end_str = 'NOW]'; }
            return start_str + ' TO ' + end_str;
        },
        convertValueToPeriod:function(value) {
            var MS = 86400000;
            var now_utc = cghub.base.toUTC(new Date());
            // Get the number of days
            var values = value.slice(1, -1).split(' TO ');
            var start_now = parseInt(values[0].split('-').reverse()[0].slice(0, -3));
            var end_now = parseInt(values[1].split('-').reverse()[0].slice(0, -3));
            // Convert each to date objects
            isNaN(start_now) ? start_now = 0 : start_now = start_now * MS;
            isNaN(end_now) ? end_now = 0 : end_now = end_now * MS;
            var start_date = new Date(now_utc - start_now);
            var end_date = new Date(now_utc - end_now);
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
