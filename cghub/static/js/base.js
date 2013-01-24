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
            cghub.base.highlightCode('pre.xml-code');
            cghub.base.activateTooltipHelp();
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
            $(document).on('click', '.bDiv tr', function(obj){
                if(obj.target.localName=='input') return;
                var tr = $(this);
                var modal = $(tr.attr('data-target'));
                var loaded = false;
                modal.on('shown', function(){
                    if (!loaded){
                        modal.find('.modal-body').load(tr.attr('data-details-url'), function(){
                            cghub.base.highlightCode('.modal-body pre.xml-code');
                            loaded = true;
                        });
                    };
                }).on('show', function(){
                    modal.find('.modal-body').html('Loading ...');
                    modal.find('.modal-label').html('Details for UUID='+tr.attr('data-uuid'));
                }).modal('show');
                return false;
            });
        },
        activateTooltipHelp:function () {
            $(document).on('mouseenter', '.js-tooltip-help', function(e){
                cghub.base.tooltipTimeout = setTimeout(function() {
                    var posX = $(e.target).offset().left - $(window).scrollLeft();
                    var posY = $(e.target).offset().top - $(window).scrollTop() - 2;
                    var content = $(e.target).attr('data-tooltip');
                    if(!content) {
                        content = 'Click to view help for ' + $(e.target).text();
                    }
                    var tooltip = $('<div class="tooltip"></div>').html(content).appendTo($('body'));
                    tooltip.css({top: posY - tooltip.outerHeight(), left: posX}).fadeIn(100, 'swing');
                }, 1500);
            });
            $(document).on('mouseout', '.js-tooltip-help', function(){
                if(cghub.base.tooltipTimeout) {
                    clearTimeout(cghub.base.tooltipTimeout);
                    $('.tooltip').remove();
                }
            });
        },
        highlightCode:function(element) {
            var xmlcontainer = $(element);
            if (xmlcontainer.length) {
                xmlcontainer.text(vkbeautify.xml(xmlcontainer.text(), 2));
                hljs.highlightBlock(xmlcontainer[0]);
            }
        },
    };
    cghub.base.init();
});
