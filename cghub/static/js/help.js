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
        keysIgnore: ['analysis id', 'uploaded', 'modified', 'barcode',
                'files size', 'aliquot id', 'tss id', 'participant id',
                'published', 'sample id', 'sample accession', 'checksum',
                'filename'],
        init:function () {
            cghub.help.bindEvents();
            cghub.help.activateTableHeaderTooltipHelp();
            cghub.help.activateDetailsHeaderTooltipHelp();
            cghub.help.activateColumnsDropdownTooltipHelp();
            cghub.help.activateTableCellTooltipHelp();
            cghub.help.activateDetailsValueTooltipHelp();
            cghub.help.activateFilterHeaderTooltipHelp();
            cghub.help.activateFilterSelectorItemTooltipHelp();
            cghub.help.activateFilterTextTooltipHelp();
            cghub.help.activateCommonTooltipHelp();
            cghub.help.activateAppliedFiltersSectionTooltipHelp();
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
                url: cghub.vars.helpHintUrl,
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
                        var tooltipTop = posY;
                        var tooltipLeft = posX;
                        if (tooltipLeft > $(window).width() - 200) {
                            tooltipLeft -= 100;
                        }
                        tooltip.css({left: tooltipLeft})
                        if (posY < tooltip.outerHeight()){
                            tooltipTop += $target.outerHeight();//tooltip on bottom
                        }
                        else {
                            tooltipTop -= tooltip.outerHeight();//tooltip on top
                        }
                        tooltip.css({top: tooltipTop}).fadeIn(100, 'swing');
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
            $(document).on('click', '.js-help-link', function() {
                var slug = $(this).data('slug');
                $.ajax({
                    url: cghub.vars.helpTextUrl,
                    dataType: "json",
                    data: {'slug': slug},
                    type: 'GET',
                    success: function (data) {
                        if(data['success']) {
                            cghub.help.removeTooltips();
                            cghub.base.showMessage(data['title'], data['content']);
                        }
                    }
                });
                return false;
            });
        },
        activateTooltipsForSelector:function (selector, find_key) {
            selector = selector + ', ' + selector + ' > abbr';
            $(document).on('mouseenter', selector, function(e){
                cghub.help.tooltipShowTimeout = setTimeout(function() {
                    var $target = $(e.target);
                    if($target.is('abbr')) {
                        $target = $target.parent();
                    }
                    cghub.help.hintShow = true;
                    cghub.help.showToolTip($target, find_key($target));
                }, cghub.vars.tooltipHoverTime);
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
        // for headers in results table
        activateTableHeaderTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.hDivBox a', function($target) {
                return $target.text()
            });
        },
        // for headers in details table
        activateDetailsHeaderTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('table.js-details-table th', function($target) {
                return $target.text();
            });
        },
        // for items in Columns dropdown
        activateColumnsDropdownTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('#ddcl-id-columns-selector-ddw .ui-dropdownchecklist-item label', function($target) {
                return $target.text()
            });
        },

        // for cells in result table
        activateTableCellTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.bDiv td[headers] div', function($target) {
                if(!$.trim($target.text()).length) return '';
                var index = $target.parent().index();
                var columnName = $('.hDivBox table').find('tr').eq(0).find('th').eq(index).text();
                if($.inArray(columnName.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return columnName + ':' + $target.text();
            });
        },
        // for values in details table
        activateDetailsValueTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('table.js-details-table td', function($target) {
                if(!$.trim($target.text()).length) return '';
                var columnName = $target.parent().find('th').text();
                if($.inArray(columnName.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return columnName + ':' + $target.text();
            });
        },
        // for filter headers
        activateFilterHeaderTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar .filter-label', function($target) {
                return 'filter:' + $target.text().replace(':', '').replace('By ', '');
            });
        },
        // for items in dropdown list when selecting checkboxes with filters
        activateFilterSelectorItemTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar .ui-dropdownchecklist-text', function($target) {
                var filterName = $target.parents('.ui-dropdownchecklist-dropcontainer-wrapper').prev().prev().prev().text();
                filterName = filterName.replace(':', '').replace('By ', '');
                if($.inArray(filterName.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return filterName + ':' + $.trim($target.text());
            });
        },
        // for selected filters when dropdown list is closed
        activateFilterTextTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.sidebar .ui-dropdownchecklist-text-item', function($target) {
                var filterName = $target.parents('.ui-dropdownchecklist-selector-wrapper').prev().prev().text();
                filterName = filterName.replace(':', '').replace('By ', '');
                if($.inArray(filterName.toLowerCase(), cghub.help.keysIgnore) != -1) return '';
                return filterName + ':' + $target.text();
            });
        },
        // for other elements on the page
        activateCommonTooltipHelp:function () {
            cghub.help.activateTooltipsForSelector('.js-common-tooltip', function($target) {
                return 'common:' + $target.data('key');
            });
        },
        // for 'Applied filter(s)' section
        activateAppliedFiltersSectionTooltipHelp:function() {
            cghub.help.activateTooltipsForSelector('.base-content div.applied-filters li span', function($target) {
                var text = $($target).parents('li').text();
                var filterName = text.substring(0, text.indexOf(':'));
                var filterValue = $target.text().trim()
                if (filterValue.indexOf('(') != -1) {
                    filterValue = filterValue.substring(0, filterValue.indexOf(' ('));
                }
                return filterName + ':' + filterValue;
            })
        }
    };
    cghub.help.init();
});
