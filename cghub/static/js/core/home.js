jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.home = {
        init:function () {
            cghub.home.cacheElements();
            cghub.home.bindEvents();
        },
        cacheElements:function () {
            cghub.home.$homeTable = $('table.data-table');
            cghub.home.$homeTable.colResizable({
                liveDrag:true
            });
        },
        bindEvents:function () {

        }
    };
    cghub.home.init();
});
