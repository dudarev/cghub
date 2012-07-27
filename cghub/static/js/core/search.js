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
            cghub.search.initFilterAccordions();
            cghub.search.updateCheckboxes();
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$searchTable.colResizable({
                liveDrag:true
            });
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            cghub.search.$selectAllLink = $('.select-all');
            cghub.search.$deselectAllLink = $('.deselect-all');
        },
        bindEvents:function () {
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
            cghub.search.$selectAllLink.on('click', cghub.search.selectAllFilterValues);
            cghub.search.$deselectAllLink.on('click', cghub.search.deselectAllFilterValues);
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
                        if ($.inArray($(this).attr('data'), selection) < 0){
                            $(this).attr('checked', false);
                        } else {
                            $(this).attr('checked', 'checked');
                        };
                    });
                }
            });
        },
        applyFilters:function () {
            var categories = $('.filter-category');
            // loop by categories: center_name, experiment_type etc.
            categories.each(function (i,f) {
                var filter = $(this).attr('data-filter');
                var values = $(this).find(':checkbox');
                var are_all_checked = true;
                var query = '';
                // loop by values in category
                values.each(function (ii,ff) {
                    if ($(this).attr('checked') == 'checked'){
                        if (query == ''){
                            query = $(this).attr('data');
                        } else {
                            query += ' OR ' + $(this).attr('data');
                        };
                    } else {
                        are_all_checked = false;
                    };
                });
                if (!are_all_checked && query != ''){
                    query = '(' + query + ')';
                    var new_param = [];
                    new_param[filter] = query;
                    var href = URI(location.href).search(new_param);
                    window.location.href = href;
                }
                console.log(location.pathname);
                console.log(are_all_checked);
                console.log(query);
            });
        },
        selectAllFilterValues: function () {
            var checkboxes = $(this).parent().parent().find(':checkbox');
            checkboxes.each(function (i,f) {
                $(this).attr('checked', 'checked');
            })
            return false;
        },
        deselectAllFilterValues: function () {
            var checkboxes = $(this).parent().parent().find(':checkbox');
            checkboxes.each(function (i,f) {
                $(this).attr('checked', false);
            })
            return false;
        },
        initFilterAccordions:function() {
            var accordions = $.find('.filter-accordion');
            for (var i=0; i<accordions.length; i++) {
                var acc = $(accordions[i]),
                    clickable = acc.children('.filter-accordion-header');
                clickable.bind('click', function() {
                    var content = $(this).parent().children('.filter-accordion-content'),
                        icon = $(this).children('.filter-accordion-icon');
                    content.slideToggle();
                    icon.toggleClass('ui-icon-triangle-1-e ui-icon-triangle-1-s')
                })
            }
        }
    };
    cghub.search.init();
});
