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
            cghub.cart.$downloadFileBtn = $('.cart-download');
            cghub.cart.$removeBtn = $('.cart-remove');
            cghub.cart.$clearBtn = $('.cart-clear');
            cghub.cart.$form = $('#cart-form');
            cghub.cart.$cbCompressed = $('.js-compressed');
        },
        bindEvents:function () {
            cghub.cart.$downloadFileBtn.on('click', cghub.cart.downloadFile);
            cghub.cart.$removeBtn.on('click', cghub.cart.removeFromCart);
            cghub.cart.$clearBtn.on('click', cghub.cart.clearCart);
            if (cghub.cart.$form.length) {
                cghub.cart.$form[0].onsubmit = cghub.cart.formSubmit;
            }
            cghub.cart.compressedCheckbox();
        },
        initFlexigrid:function () {
            cghub.cart.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.data-table').css('visibility', 'visible');
            /* add fieldset element */
            var $data_table = $('.bDiv table');
            $data_table.wrap($('<fieldset/>'));
            $data_table.parent().prepend($('<legend class="hidden">Select files to remove from cart:</legend>'));
        },
        // protection from submitting form before js initialised
        formSubmit:function () {
            console.log($(this).attr('action'));
            if($(this).attr('action').indexOf('action') != -1) return false;
        },
        // replace current action with needed, /\/[a-z_]+\/$/ = "/some_action/",
        // slashes in '/.../' are needed!
        removeFromCart:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            cghub.selected.save();
            if(!cghub.selected.exists) return false;
            form.append($('<textarea name="ids" style="display: none;">'+cghub.selected.get_ids_list().join(' ')+'</textarea>'))
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/remove/'));
        },
        clearCart: function() {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, '/clear/'));
        },
        compressedCheckbox: function() {
            var initial_value = sessionStorage.getItem('download-compressed');
            if(initial_value === null) {initial_value = 'false'};
            cghub.cart.$cbCompressed.prop('checked', initial_value == 'true');
            cghub.cart.$cbCompressed.on('change', function() {
                var val = $(this).prop('checked');
                sessionStorage.setItem('download-compressed', val);
                cghub.cart.$cbCompressed.prop('checked', val);
            });
        },
        downloadFile:function () {
            var btn = $(this);
            var form = btn.closest('form');
            form.attr('action', form.attr('action').replace('?gzip=true', ''));
            var url = '/' + btn.data('download') + '/';
            if(cghub.cart.$cbCompressed.prop('checked')) {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, url + '?gzip=true'));
                form.trigger('submit');
                btn.parent().trigger('click');
                return false;
            } else {
                form.attr('action', form.attr('action').replace(/\/[a-z_]+\/$/, url));
            }
        },
    };
    cghub.cart.init();
});
