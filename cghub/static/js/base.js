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
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
            cghub.base.activateItemDetailsLinks();
            $(document).on('change', '.js-select-all', cghub.base.changeCheckboxes);
            $(document).on('change', '.data-table-checkbox', cghub.base.updateSelectAll);
        },
        changeCheckboxes:function () {
            $('.data-table-checkbox').prop('checked', $(this).is(':checked'));
            return false;
        },
        updateSelectAll:function () {
            $('.js-select-all').prop('checked',
                $('.data-table-checkbox').length == $('.data-table-checkbox:checked').length);
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
                var $tr = $(this);
                var modal = $($tr.attr('data-target'));
                var loaded = false;
                modal.on('shown', function(){
                    if (!loaded){
                        modal.find('.modal-body').load($tr.attr('data-details-url'), function(response, status, xhr){
                            if (status == "error") {
                                modal.find('.modal-body').html('There was an error loading data. Please contact admin.');
                            } else {
                                cghub.base.highlightCode('.modal-body pre.xml-code');
                                loaded = true;
                            }
                        });
                    }
                }).on('show', function(){
                    modal.find('.modal-body').html('Loading ...');
                    modal.find('.modal-label').html('Details for UUID '+$tr.attr('data-uuid'));
                }).modal('show');
                return false;
            });
            $(document).on('click', '.js-details-popup', function() {
                var $tr = $($(this).parents('ul').data('e').target).parents('tr');
                $tr.trigger('click');
                return false;
            });
            $(document).on('click', '.js-details-page', function() {
                var $tr = $($(this).parents('ul').data('e').target).parents('tr');
                /* open in new tab */
                window.open($tr.attr('data-details-url'), '_blank');
                window.focus();
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
        }
    };
    cghub.base.init();
});
