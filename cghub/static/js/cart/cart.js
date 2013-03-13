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
            cghub.cart.$downloadMetadataXml = $('.cart-form-download-metadata-xml');
            cghub.cart.$downloadMetadataTsv = $('.cart-form-download-metadata-tsv');
            cghub.cart.$removeBtn = $('.cart-form-remove');
            cghub.cart.$clearBtn = $('.cart-form-clear');
        },
        bindEvents:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid .bDiv tr').contextmenu();
            cghub.cart.$downloadManifestXml.on('click', cghub.cart.downloadManifestXml);
            cghub.cart.$downloadManifestTsv.on('click', cghub.cart.downloadManifestTsv);
            cghub.cart.$downloadMetadataXml.on('click', cghub.cart.downloadMetadataXml);
            cghub.cart.$downloadMetadataTsv.on('click', cghub.cart.downloadMetadataTsv);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
            cghub.cart.$clearBtn.on('click', cghub.cart.clearCart);
        },
        // replace current action with needed, /\/[a-z_]+\/$/ = "/some_action/",
        // slashes in '/.../' are needed!
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/remove/'));
        },
        clearCart: function(){
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/clear/'));
        },
        downloadManifestXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/manifest_xml/'));
            form.trigger('submit');
        },
        downloadManifestTsv:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/manifest_tsv/'));
            form.trigger('submit');
        },
        downloadMetadataXml:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/metadata_xml/'));
            form.trigger('submit');
        },
        downloadMetadataTsv:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/metadata_tsv/'));
            form.trigger('submit');
        }
    };
    cghub.cart.init();
});
