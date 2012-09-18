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
            cghub.cart.$columnNumber = 0;
            cghub.cart.$nextColumn;
            cghub.cart.$nextColumnWidth = 0;
            cghub.cart.$searchTable = $('table.data-table');
            cghub.cart.$downloadManifestBtn = $('.btn.cart-form-download-manifest');
            cghub.cart.$downloadXmlBtn = $('.btn.cart-form-download-xml');
            cghub.cart.$removeBtn = $('.btn.cart-form-remove');
        },
        bindEvents:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto'});
            cghub.cart.$downloadManifestBtn.on('click', cghub.cart.downloadManifest);
            cghub.cart.$downloadXmlBtn.on('click', cghub.cart.downloadXml);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
        },
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|xml|manifest)/, 'remove'));
        },
        downloadManifest:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|xml|remove)/, 'manifest'));
        },
        downloadXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|manifest|remove)/, 'xml'));
        }
    };
    cghub.cart.init();
});
