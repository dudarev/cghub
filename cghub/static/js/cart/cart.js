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

        }
    };
    cghub.cart.init();
});
