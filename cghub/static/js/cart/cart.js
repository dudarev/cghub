jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.cart = {
        init:function () {
            cghub.cart.cacheElements();
            cghub.cart.bindEvents();
        },
        cacheElements:function () {
            cghub.cart.$cartTable = $('table.data-table');
            cghub.cart.$cartTable.colResizable({
                liveDrag:true
            });
        },
        bindEvents:function () {
            $('#id_add_files_form').submit(function() {
                // collect all data attributes
                var data = {};
                var selected_files = $('input[type="checkbox"][name="selected_files"]:checked');
                selected_files.each(function(i, f) {
                    var file_data = $(f).data()
                    data[file_data.legacy_sample_id] = file_data;
                });
                $.ajax({
                    data: $(this).serialize() + "&attributes=" + JSON.stringify(data),
                    type: $(this).attr('method'),
                    dataType: 'json',
                    url: $(this).attr('action'),
                    success: function(data) {
                        window.location.href = data.redirect;
                    }
                });
                return false;
            });
        }
    };
    cghub.cart.init();
});
