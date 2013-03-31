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
        hoverTime: 1500, /* time, after which tooltip will be shown, in ms */
        hintShow: false,
        keysIgnore: ['uuid', 'uploaded', 'last modified', 'barcode', 'files size'],
        init:function () {
            cghub.help.hintUrl = $('body').data('help-hint-url');
            cghub.help.textUrl = $('body').data('help-text-url');
            cghub.help.bindEvents();
            cghub.help.activateTableHeaderTooltipHelp();
            cghub.help.activateTableCellTooltipHelp();
            cghub.help.activateFilterTooltipHelp();
            cghub.help.activateFilterItemTooltipHelp();
            cghub.help.activateFilterTextTooltipHelp();
            cghub.help.activateHelpLinks();
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
        activateHelpLinks:function () {
            $(document).on('click', '.js-help-link', function(){
                var modal = $('#helpTextModal');
                if(!modal.length) return;
                var slug = $(this).data('slug');
                $.ajax({
                    url: cghub.help.textUrl,
                    dataType: "json",
                    data: {'slug': slug},
                    type: 'GET',
                    success: function (data) {
                        if(data['success']) {
                            cghub.help.removeTooltips();
                            modal.find('.modal-label').text(data['title']);
                            modal.find('.modal-body').html(data['content']);
                            modal.modal();
                        }
                    }
                });
                return false;
            });
        },
        activateTooltipsForSelector:function (selector, find_key) {
            $(document).on('mouseenter', selector, function(e){
                cghub.help.tooltipShowTimeout = setTimeout(function() {
                    var $target = $(e.target);
                    cghub.help.hintShow = true;
                    cghub.help.showToolTip($target, find_key($target));
                }, cghub.help.hoverTime);
            });
            $(document).on('mouseenter', '.js-tooltip, .js-tooltip > *', function(){
                if(cghub.help.tooltipHideTimeout) {
                    clearTimeout(cghub.help.tooltipHideTimeout);
                }
            });
            $(document).on('mouseout', selector + ', .js-tooltip, .js-tooltip > *', function(obj){
                if($(obj.relatedTarget).parents('.js-tooltip').length) return;
                if($(obj.target).parents('.js-tooltip').length) return;
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
                return $target.text().replace(decodeURI('%C2%A0%E2%86%93'), '');
            });
        },
        activateTableCellTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.bDiv td div', function($target) {
                if(!$target.text().length) return '';
                var index = $target.parent().index();
                var column = $('.hDivBox table').find('tr').eq(0).find('th')
                .eq(index).text().replace(decodeURI('%C2%A0%E2%86%93'), '');
                if($.inArray(column.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return column + ':' + $target.text();
            });
        },
        activateFilterTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar h5', function($target) {
                return $target.text().replace(':', '').replace('By ', '');
            });
        },
        activateFilterItemTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar label', function($target) {
                var filter = $target.parents('.ui-dropdownchecklist-dropcontainer-wrapper').prev().prev().prev().text();
                filter = filter.replace(':', '').replace('By ', '');
                if($.inArray(filter.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return filter + ':' + $target.text();
            });
        },
        activateFilterTextTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar .ui-dropdownchecklist-text-item', function($target) {
                var filter = $target.parents('.ui-dropdownchecklist-selector-wrapper').prev().prev().text();
                filter = filter.replace(':', '').replace('By ', '');
                if($.inArray(filter.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return filter + ':' + $target.text();
            });
        }
    };
    cghub.help.init();
});
