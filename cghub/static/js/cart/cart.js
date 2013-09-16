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
            $('.flexigrid .bDiv tr').contextmenu();
            $('.data-table').css('visibility', 'visible');
            /* add fieldset element */
            var $data_table = $('.bDiv table');
            $data_table.wrap($('<fieldset/>'));
            $data_table.parent().prepend($('<legend class="hidden">Select files to remove from cart:</legend>'));
        },
        // replace current action with needed, /\/[a-z_]+\/$/ = "/some_action/",
        // slashes in '/.../' are needed!
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            cghub.selected.save();
            if(!cghub.selected.exists) return false;
            form.append($('<textarea name="ids" style="display: none;">'+cghub.selected.get_ids_list().join(' ')+'</textarea>'))
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/remove/'));
        },
        clearCart: function(){
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/clear/'));
        },
        downloadManifest:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            if(btn.is('a')) {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/manifest/?gzip=true'));
                form.trigger('submit');
                btn.parent().trigger('click');
                return false;
            } else {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/manifest/'));
            }
        },
        downloadMetadata:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            if(btn.is('a')) {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/metadata/?gzip=true'));
                form.trigger('submit');
                btn.parent().trigger('click');
                return false;
            } else {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/metadata/'));
            }
        },
        downloadSummary:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            if(btn.is('a')) {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/summary/?gzip=true'));
                form.trigger('submit');
                btn.parent().trigger('click');
                return false;
            } else {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/summary/'));
            }
        },
    };
    cghub.cart.init();
});
