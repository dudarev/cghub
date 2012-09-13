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
            cghub.cart.$searchTable.colResizable({
                onResize: cghub.cart.adjustColumns
            });
            cghub.cart.$downloadManifestBtn = $('.btn.cart-form-download-manifest');
            cghub.cart.$downloadXmlBtn = $('.btn.cart-form-download-xml');
            cghub.cart.$removeBtn = $('.btn.cart-form-remove');
        },
        bindEvents:function () {
            var CRC = $('table.data-table').prev();
            CRC.children().each(function (i, e) {
                $(e).children().mousedown(function(e) {
                    cghub.cart.nextColumn = $($('table.data-table').find('thead > tr').children()[i + 1])
                    cghub.cart.nextColumnWidth = cghub.cart.nextColumn.width();
                });
                $(e).children().mouseup(function(e) {
                    cghub.cart.columnNumber = i + 1;
                });
            });
            cghub.cart.$downloadManifestBtn.on('click', cghub.cart.downloadManifest);
            cghub.cart.$downloadXmlBtn.on('click', cghub.cart.downloadXml);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
        },
        adjustColumns: function () {
            var columnNumber = cghub.cart.columnNumber,
                totalWidth = 0,
                columns = $('table.data-table').find('thead > tr').children();

            cghub.cart.nextColumn.width(cghub.cart.nextColumnWidth);
            $('table.data-table').prev().children().each(function (i, e) {
                totalWidth += $(columns[i]).width();
                $(e).css('left', (totalWidth + 2) + 'px');
            });
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
