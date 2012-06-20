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
            cghub.cart.$downloadManifestBtn = $('.btn.cart-form-download-manifest');
            cghub.cart.$downloadXmlBtn = $('.btn.cart-form-download-xml');
            cghub.cart.$removeBtn = $('.btn.cart-form-remove');
            cghub.cart.$addFilesForm = $('form#id_add_files_form');
        },
        bindEvents:function () {
            cghub.cart.$downloadManifestBtn.on('click', cghub.cart.downloadManifest);
            cghub.cart.$downloadXmlBtn.on('click', cghub.cart.downloadXml);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
            cghub.cart.$addFilesForm.on('submit', cghub.cart.addFilesFormSubmit);
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
        },
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('action', 'remove'));
        },
        downloadManifest:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('action', 'manifest'));
        },
        downloadXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('action', 'xml'));
        }
    };
    cghub.cart.init();
});
