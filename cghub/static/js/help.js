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
        hintShow: false,
        keysIgnore: ['UUID', 'Upload time', 'Last modified', 'Barcode', 'Files Size'],
        hintUrl: '/help/hint/',
        init:function () {
            cghub.help.bindEvents();
            cghub.help.activateTableHeaderTooltipHelp();
            cghub.help.activateTableCellTooltipHelp();
        },
        removeTooltips:function() {
            if(cghub.help.tooltipShowTimeout) {
                clearTimeout(cghub.help.tooltipShowTimeout);
            }
            if(cghub.help.tooltipHideTimeout) {
                clearTimeout(cghub.help.tooltipHideTimeout);
            }
            cghub.help.hintShow = false;
            $('.js-tooltip').remove();
        },
        showToolTip:function($target, key) {
            if(!key.length) return;
            console.log(key);
            $.ajax({
                url: cghub.help.hintUrl,
                dataType: "json",
                data: {'key': key},
                type: 'GET',
                success: function (data) {
                    if(!cghub.help.hintShow) return;
                    cghub.help.removeTooltips();
                    if(data['success']) {
                        var posX = $target.offset().left - $(window).scrollLeft();
                        var posY = $target.offset().top - $(window).scrollTop();
                        var tooltip = $('<div class="tooltip js-tooltip"></div>').html(data['text']).appendTo($('body'));
                        tooltip.css({top: posY - tooltip.outerHeight(), left: posX}).fadeIn(100, 'swing');
                    }
                }
            });
        },
        bindEvents:function () {
            $(window).scroll(function(){
                cghub.help.removeTooltips()
            });
        },
        activateTooltipsForSelector:function (selector, find_key) {
            $(document).on('mouseenter', selector, function(e){
                cghub.help.tooltipShowTimeout = setTimeout(function() {
                    var $target = $(e.target);
                    cghub.help.hintShow = true;
                    cghub.help.showToolTip($target, find_key($target));
                }, 1500);
            });
            $(document).on('mouseenter', selector + ', .js-tooltip, .js-tooltip > *', function(){
                if(cghub.help.tooltipHideTimeout) {
                    clearTimeout(cghub.help.tooltipHideTimeout);
                }
            });
            $(document).on('mouseout', selector + ', .js-tooltip, .js-tooltip > *', function(obj){
                if($(obj.target).parents('.js-tooltip').length)return;
                if(cghub.help.tooltipShowTimeout) {
                    clearTimeout(cghub.help.tooltipShowTimeout);
                }
                cghub.help.tooltipHideTimeout = setTimeout(function() {
                    if(cghub.help.tooltipHideTimeout) {
                        clearTimeout(cghub.help.tooltipHideTimeout);
                        $('.tooltip').remove();
                        cghub.help.hintShow = false;
                    }
                }, 0);
            });
        },
        activateTableHeaderTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.hDivBox a', function($target) {
                return $target.text();
            });
        },
        activateTableCellTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.bDiv td div', function($target) {
                var index = $target.parent().index();
                var column = $('.hDivBox table').find('tr').eq(0).find('th').eq(index).text();
                if($.inArray(column, cghub.help.keysIgnore) != -1) return '';
                return column + ':' + $target.text();
            });
        },
    };
    cghub.help.init();
});

