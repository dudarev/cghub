/*jslint browser: true*/
jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.base = {
        init:function () {
            cghub.base.cacheElements();
            cghub.base.bindEvents();
        },
        cacheElements:function () {
            cghub.base.$navbarAnchors = $('div.navbar ul.nav li a');
            cghub.base.$navbarListItem = $('div.navbar ul li');
            cghub.base.$selectAll = $('.select_all_items');
            cghub.base.$resultCheckboxes = $('.data-table-checkbox-cell input');
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
            cghub.base.$selectAll.each(function(i, e) {
                $(e).on('click', cghub.base.changeCheckboxes);
            });
        },
        changeCheckboxes:function () {
            var btn = $(this);
            if (btn.html() == 'Select all') {
                cghub.base.$resultCheckboxes.prop('checked', true);
                cghub.base.$selectAll.each(function(i, e) {
                    $(e).html('Unselect all');
                });
            } else if (btn.html() == 'Unselect all') {
                cghub.base.$resultCheckboxes.prop('checked', false);
                cghub.base.$selectAll.each(function(i, e) {
                    $(e).html('Select all');
                });
            };
            return false;
        },
        defineActiveLink:function () {
            cghub.base.$navbarAnchors.each(cghub.base.resetActiveLink);
        },
        resetActiveLink:function (idx, a_el) {
            var pageLink = $(a_el);
            if (a_el.href !== (window.location.origin + window.location.pathname)) {
                pageLink.closest('li').removeClass('active');
            } else {
                pageLink.closest('li').addClass('active');
            }
        }
    };
    cghub.base.init();
});
