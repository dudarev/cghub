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
            cghub.base.highlightCode();
        },
        cacheElements:function () {
            cghub.base.$navbarAnchors = $('div.navbar ul.nav li a');
            cghub.base.$navbarListItem = $('div.navbar ul li');
            cghub.base.$selectAll = $('.select_all_items');
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
            cghub.base.activateItemDetailsLinks();
            cghub.base.$selectAll.each(function(i, e) {
                $(e).on('click', cghub.base.changeCheckboxes);
            });
        },
        changeCheckboxes:function () {
            var btn = $(this),
                resultCheckboxes = $('.data-table-checkbox');
            if (btn.html() == 'Select all') {
                resultCheckboxes.prop('checked', true);
                cghub.base.$selectAll.each(function(i, e) {
                    $(e).html('Unselect all');
                });
            } else if (btn.html() == 'Unselect all') {
                resultCheckboxes.prop('checked', false);
                cghub.base.$selectAll.each(function(i, e) {
                    $(e).html('Select all');
                });
            }
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
        },
        activateItemDetailsLinks:function () {
            $('.js-item-details-link').live('click', function(obj){
                var link = $(obj.target);
                var modal = $(link.attr('data-target'));
                var loaded = false;
                modal.on('shown', function(){
                    if (!loaded){
                        modal.find('.modal-body').load(link.attr('href'), function(){
                            $('.modal-body pre.xml-code').each(function(i, e) {hljs.highlightBlock(e)});
                            loaded = true;
                        });
                    };
                }).on('show', function(){
                    modal.find('.modal-body').html('Loading ...');
                    modal.find('.modal-label').html('Details for UUID='+link.text());
                }).modal('show');
                return false;
            });
        },
        highlightCode:function() {
            $('pre.xml-code').each(function(i, e) {hljs.highlightBlock(e)});
        },
    };
    cghub.base.init();
});
