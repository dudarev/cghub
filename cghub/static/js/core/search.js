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
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$searchTable.colResizable({
                liveDrag:true
            });
            cghub.search.$addFilesForm = $('form#id_add_files_form');
            cghub.search.$applyFiltersButton = $('button#id_apply_filters');
            console.log(cghub.search.$addFiltersForm);
        },
        bindEvents:function () {
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
            cghub.search.$applyFiltersButton.on('click', cghub.search.applyFilters);
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
            var categories = $('.filter-category');
            categories.each(function (i,f) {
                console.log(($(this).attr('data-filter')));
                var values = $(this).find(':checkbox');
                console.log(values);
                values.each(function (ii,ff) {
                    console.log($(this).attr('checked'));
                });
            });
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
