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
            cghub.cart.$downloadManifestXml = $('.cart-form-download-manifest-xml');
            cghub.cart.$downloadManifestTsv = $('.cart-form-download-manifest-tsv');
            cghub.cart.$downloadXmlBtn = $('.btn.cart-form-download-xml');
            cghub.cart.$removeBtn = $('.btn.cart-form-remove');
        },
        bindEvents:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid .bDiv tr').contextmenu();
            cghub.cart.$downloadManifestXml.on('click', cghub.cart.downloadManifestXml);
            cghub.cart.$downloadManifestTsv.on('click', cghub.cart.downloadManifestTsv);
            cghub.cart.$downloadXmlBtn.on('click', cghub.cart.downloadXml);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
        },
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|xml|manifest_xml|manifest_tsv)/, 'remove'));
        },
        downloadManifestXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|xml|remove|manifest_tsv)/, 'manifest_xml'));
        },
        downloadManifestTsv:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|xml|remove|manifest_xml)/, 'manifest_tsv'));
        },
        downloadXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|remove|manifest_xml|manifest_tsv)/, 'xml'));
        }
    };
    cghub.cart.init();
});
