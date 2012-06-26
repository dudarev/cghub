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
        },
        cacheElements:function () {
            cghub.search.$searchTable = $('table.data-table');
            cghub.search.$searchTable.colResizable({
                liveDrag:true
            });
            cghub.search.$addFilesForm = $('form#id_add_files_form');
        },
        bindEvents:function () {
            cghub.search.$addFilesForm.on('submit', cghub.search.addFilesFormSubmit);
        },
        addFilesFormSubmit:function () {
            // collect all data attributes
            var data = {};
            var selected_files = $('input[type="checkbox"][name="selected_files"]:checked');
            selected_files.each(function (i, f) {
                var file_data = $(f).data();
                data[file_data.legacy_sample_id] = file_data;
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
        }
    };
    cghub.search.init();
});
