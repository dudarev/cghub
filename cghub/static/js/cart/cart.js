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
            cghub.cart.initFlexigrid();
            cghub.cart.bindEvents();
        },
        cacheElements:function () {
            cghub.cart.$columnNumber = 0;
            cghub.cart.$nextColumn;
            cghub.cart.$nextColumnWidth = 0;
            cghub.cart.$searchTable = $('table.data-table');
            cghub.cart.$downloadManifestXml = $('.cart-download-manifest');
            cghub.cart.$downloadMetadataXml = $('.cart-download-metadata');
            cghub.cart.$downloadMetadataTsv = $('.cart-download-summary');
            cghub.cart.$removeBtn = $('.cart-remove');
            cghub.cart.$clearBtn = $('.cart-clear');
        },
        bindEvents:function () {
            cghub.cart.$downloadManifestXml.on('click', cghub.cart.downloadManifest);
            cghub.cart.$downloadMetadataXml.on('click', cghub.cart.downloadMetadata);
            cghub.cart.$downloadMetadataTsv.on('click', cghub.cart.downloadSummary);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
            cghub.cart.$clearBtn.on('click', cghub.cart.clearCart);
        },
        initFlexigrid:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.flexigrid').attr('id', 'data-table');
            $('.flexigrid .bDiv tr').contextmenu();
            $('.data-table').css('visibility', 'visible');
            $('.ui-dropdownchecklist-dropcontainer').attr('tabindex', -1);
            /* add text for screen readers for ddcl-id-columns-selector */
            $('#ddcl-id-columns-selector .ui-dropdownchecklist-selector')
                .prepend('<div class="hidden">' + $('#id-columns-selector').attr('title') + ', selected:</div>');
        },
        // replace current action with needed, /\/[a-z_]+\/$/ = "/some_action/",
        // slashes in '/.../' are needed!
        removeFromCart:function () {
            var btn = $(this);
            if(btn.hasClass('disabled')) return false;
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/remove/'));
        },
        clearCart: function(){
            var btn = $(this);
            if(btn.hasClass('disabled')) return false;
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/clear/'));
        },
        downloadManifest:function () {
            var btn = $(this);
            if(btn.hasClass('disabled')) return false;
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/manifest/'));
        },
        downloadMetadata:function () {
            var btn = $(this);
            if(btn.hasClass('disabled')) return false;
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/metadata/'));
        },
        downloadSummary:function () {
            var btn = $(this);
            if(btn.hasClass('disabled')) return false;
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/summary/'));
        }
    };
    cghub.cart.init();
});
