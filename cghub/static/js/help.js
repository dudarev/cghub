/*jslint browser: true*/
jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.help = {
        init:function () {
            cghub.help.activateTooltipHelp();
        },
        removeTooltips:function() {
            if(cghub.help.tooltipShowTimeout) {
                clearTimeout(cghub.help.tooltipShowTimeout);
            }
            if(cghub.help.tooltipHideTimeout) {
                clearTimeout(cghub.help.tooltipHideTimeout);
            }
            $('.js-tooltip').remove();
        },
        activateTooltipHelp:function () {
            $(document).on('mouseenter', '.js-tooltip-help', function(e){
                cghub.help.tooltipShowTimeout = setTimeout(function() {
                    var $target = $(e.target); 
                    var posX = $(e.target).offset().left - $(window).scrollLeft();
                    var posY = $(e.target).offset().top - $(window).scrollTop();
                    var content = '';
                    if($target.hasClass('js-tooltip-help')) {
                        content = $target.find('.js-tooltip-text').html();
                    } else {
                        content = $target.parents('.js-tooltip-help').find('.js-tooltip-text').html();
                    }
                    cghub.help.removeTooltips();
                    if(!content) return;
                    var tooltip = $('<div class="tooltip js-tooltip"></div>').html(content).appendTo($('body'));
                    tooltip.css({top: posY - tooltip.outerHeight(), left: posX}).fadeIn(100, 'swing');
                }, 1500);
            });
            $(document).on('mouseenter', '.js-tooltip-help, .js-tooltip, .js-tooltip > *', function(){
                if(cghub.help.tooltipHideTimeout) {
                    clearTimeout(cghub.help.tooltipHideTimeout);
                }
            });
            $(document).on('mouseout', '.js-tooltip-help, .js-tooltip, .js-tooltip > *', function(obj){
                if($(obj.target).parents('.js-tooltip').length)return;
                if(cghub.help.tooltipShowTimeout) {
                    clearTimeout(cghub.help.tooltipShowTimeout);
                }
                cghub.help.tooltipHideTimeout = setTimeout(function() {
                    if(cghub.help.tooltipHideTimeout) {
                        clearTimeout(cghub.help.tooltipHideTimeout);
                        $('.tooltip').remove();
                    }
                }, 0);
            });
            $(window).scroll(function(){
                cghub.help.removeTooltips()
            });
        }
    };
    cghub.help.init();
});

