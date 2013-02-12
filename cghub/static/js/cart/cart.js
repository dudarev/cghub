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
            cghub.cart.$downloadMetadataBtn = $('.cart-form-download-metadata');
            cghub.cart.$removeBtn = $('.btn.cart-form-remove');
        },
        bindEvents:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid .bDiv tr').contextmenu();
            cghub.cart.$downloadManifestXml.on('click', cghub.cart.downloadManifestXml);
            cghub.cart.$downloadManifestTsv.on('click', cghub.cart.downloadManifestTsv);
            cghub.cart.$downloadMetadataBtn.on('click', cghub.cart.downloadMetadata);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
        },
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|metadata|manifest_xml|manifest_tsv)/, 'remove'));
        },
        downloadManifestXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|metadata|remove|manifest_tsv)/, 'manifest_xml'));
        },
        downloadManifestTsv:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|metadata|remove|manifest_xml)/, 'manifest_tsv'));
        },
        downloadMetadata:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/(action|remove|manifest_xml|manifest_tsv)/, 'metadata'));
        }
    };
    cghub.cart.init();
});
