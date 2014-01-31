/*jslint browser: true*/

!function ($) {
    /*
    * used code from
    * bootstrap-contextmenu.js
    * by Nikolai Fedotov
    */
    "use strict";
    var ContextMenu = function (element) {
        /* show on click (replace click to contextmenu if necessary) */
        $(element).on('click.context-menu.data-api', this.show);
        $(element).on('keydown.context-menu.data-api', this.show);
        $('html').on('click.context-menu.data-api', clearMenus);
        $('.dropdown-close').on('focus.context-menu.data-api', clearMenus);
    }
    ContextMenu.prototype = {
        constructor: ContextMenu,
        show: function (e) {
            var $this = $(this);
            if ($this.is('.disabled, :disabled')) return;
            clearMenus();
            var pos_x = 0, pos_y = 0;
            if(e.clientX) {
                /* mouse event */
                pos_x = e.clientX;
                pos_y = e.clientY;
            } else {
                if (e.ctrlKey || e.altKey) return;
                var position = $(e.target).offset();
                var charCode = (e.which) ? e.which : e.keyCode;
                if(charCode != 13 && charCode != 32) {
                    clearMenus();
                    return;
                };
                pos_x = position.left - $(window).scrollLeft();
                pos_y = position.top + $(e.target).outerHeight() - $(window).scrollTop();
            }

            var $menu = $($this.data('context-menu'));
            $menu.data('e', e)
                .css('position', 'fixed')
                .css('left', pos_x)
                .css('top', pos_y)
                .css('display', 'block')
            $menu.find('li').first().find('a').focus();
            return false
        }

    }
    function clearMenus() {
        $('.context-menu')
            .css('display','none')
            .data('e',undefined)
    }

    $.fn.contextmenu = function (option) {
        return this.each(function () {
            var $this = $(this);
            if (!$this.data('context-menu-obj')) $this.data('context-menu-obj', new ContextMenu(this));
        })
    }
    $.fn.contextmenu.Constructor = ContextMenu
}(jQuery);


jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }

    cghub.selected = {
        /* used to store list of selected ids while pagination */
        _storage_key: 'selectedItems',
        exists: false,
        items: {},
        init:function () {
            var saved_items = sessionStorage.getItem(cghub.selected._storage_key);
            if(saved_items !== null) {
                cghub.selected.items = $.parseJSON(saved_items);
                sessionStorage.setItem(cghub.selected._storage_key, '{}');
            }
            cghub.selected.count();
        },
        save:function () {
            /* add checked items */
            var selected_items = $('input[type="checkbox"][name="selected_files"]:checked');
            selected_items.each(function (i, f) {
                cghub.selected.add($(f).val());
            });
            /* remove unchecked */
            var selected_items = $('input[type="checkbox"][name="selected_files"]:not(:checked)');
            selected_items.each(function (i, f) {
                delete cghub.selected.items[$(f).val()];
            });
            sessionStorage.setItem(cghub.selected._storage_key, JSON.stringify(cghub.selected.items));
        },
        add:function (analysis_id) {
            var item = $('input[type="checkbox"][value="'+analysis_id+'"]');
            if(item.length) {
                cghub.selected.items[analysis_id] = item.data();
                cghub.selected.exists = true;
            }
        },
        ids:function () {
            var ids = [];
            for (var i in cghub.selected.items) {
                ids.push(i);
            }
            return ids;
        },
        get_ids_list:function () {
            sessionStorage.setItem(cghub.selected._storage_key, '{}');
            return cghub.selected.ids();
        },
        get_data_list:function() {
            var data = [];
            $.each(cghub.selected.items, function (i, d) {
                data.push(d);
            });
            sessionStorage.setItem(cghub.selected._storage_key, '{}');
            return data
        },
        count:function () {
            var count = 0;
            for (var i in cghub.selected.items) {
                count += 1;
            }
            if(count > 0) {
                cghub.selected.exists = true;
            } else {
                cghub.selected.exists = false;
            }
            return count;
        },
    }
    cghub.selected.init();

    cghub.table = {
        clearSelectionTimeout: undefined,
        init:function () {
            cghub.table.cacheElements();
            cghub.table.bindEvents();
            cghub.table.$selectAllCheckbox.removeAttr('disabled');
            cghub.table.repairSelection();
        },
        cacheElements:function () {
            cghub.table.$itemsPerPageLink = $('.items-per-page-label > a');
            cghub.table.$pageLink = $('.pagination ul li a');
            cghub.table.$selectAllCheckbox = $('.js-select-all');
            cghub.table.$checkboxes = $('.data-table-checkbox');
            cghub.table.$flexigrid = $('.flexigrid');
            cghub.table.$tableContainer = cghub.table.$flexigrid.find('.bDiv');
            cghub.table.$tableHeaderContainer = cghub.table.$flexigrid.find('.hDiv');
        },
        bindEvents:function () {
            cghub.table.activateItemDetailsLinks();
            cghub.table.$itemsPerPageLink.unbind('click');
            cghub.table.$itemsPerPageLink.on('click', cghub.selected.save);
            cghub.table.$pageLink.on('click', cghub.selected.save);
            cghub.table.$selectAllCheckbox.on('change', cghub.table.changeCheckboxes);
            cghub.table.$checkboxes.on('change', cghub.table.updateSelectAll);
            cghub.table.$checkboxes.on('focusin', cghub.table.tableCheckboxFocus);
            cghub.table.$checkboxes.on('focusout', cghub.table.tableCheckboxFocus);
            cghub.table.$flexigrid.on('keydown', cghub.table.arrowPress);
            /* scroll table on header scroll */
            cghub.table.$tableHeaderContainer.on('scroll', function() {
                cghub.table.$tableContainer.scrollLeft(cghub.table.$tableHeaderContainer.scrollLeft());
            });
            /* context menu */
            cghub.table.$flexigrid.find('.details-link').contextmenu();
        },
        showDetailsPopup:function(td) {
            var modal = $(td.attr('data-target'));
            var loaded = false;
            modal.on('shown', function(){
                if (!loaded){
                    // ajax is hack for for IE10
                    modal.find('.modal-body').load(td.attr('data-details-url')+'?ajax=1', function(response, status, xhr){
                        if (status == "error") {
                            modal.find('.modal-body').html('There was an error loading data. Please contact admin: <a href="mailto:'+cghub.vars.supportEmail+'">'+cghub.vars.supportEmail+'</a>');
                        } else {
                            loaded = true;
                        }
                    });
                }
            }).on('show', function(){
                modal.find('.modal-body').html('Loading ...');
                modal.find('.modal-label').html('Details for Analysis Id ' + td.parents('tr').attr('data-analysis_id'));
            }).modal('show');
            return false;
        },
        activateItemDetailsLinks:function () {
            /* activate link for details popup */
            $(document).on('click', '.js-details-popup', function() {
                var $td = $($(this).parents('ul').data('e').target).parents('td');
                cghub.table.showDetailsPopup($td);
                return false;
            });
            $(document).on('keydown', '.js-details-popup', function(e) {
                var charCode = (e.which) ? e.which : e.keyCode;
                if(charCode != 13 && charCode != 32) return;
                var $td = $($(e.target).parents('ul').data('e').target);
                cghub.table.showDetailsPopup($td);
                return false;
            });
            /* activate link to details page */
            $(document).on('click', '.js-details-page', function() {
                var $td = $($(this).parents('ul').data('e').target).parents('tr').find('.details-link');
                /* open in new tab */
                window.open($td.attr('data-details-url'), '_blank');
                window.focus();
                return false;
            });
            $(document).on('keydown', '.js-details-page', function(e) {
                var charCode = (e.which) ? e.which : e.keyCode;
                if(charCode != 13 && charCode != 32) return;
                var $td = $($(this).parents('ul').data('e').target).parents('tr').find('.details-link');
                /* open in new tab */
                window.open($td.attr('data-details-url'), '_blank');
                window.focus();
                return false;
            });
            /* activate link to sample metadata at dcc */
            $(document).on('click', '.js-sample-metadata', function() {
                var $td = $($(this).parents('ul').data('e').target).parents('tr').find('td[headers="id-col-legacy_sample_id"]');
                /* open in new tab */
                window.open($td.find('span').data('url'), '_blank');
                window.focus();
                return false;
            });
            $(document).on('keydown', '.js-sample-metadata', function(e) {
                var charCode = (e.which) ? e.which : e.keyCode;
                if(charCode != 13 && charCode != 32) return;
                var $td = $($(this).parents('ul').data('e').target).parents('tr').find('td[headers="id-col-legacy_sample_id"]');
                window.open($td.find('span').data('url'), '_blank');
                window.focus();
                return false;
            });
            // fix IE submit outer forms bug
            if ($.browser.msie) {
                $(document).on('click', '.js-cart-add-item-button', function(e) {
                    var url = $(this).parent().attr('action');
                    var form = document.createElement('form');
                    form.action = url;
                    form.method = 'POST';
                    form.id = 'ie-form';
                    document.body.appendChild(form);
                    form.submit();
                    document.body.removeChild(form);
                    return false;
                });
            }
        },
        changeCheckboxes:function () {
            cghub.table.$checkboxes.prop('checked', $(this).is(':checked'));
            return;
        },
        updateSelectAll:function () {
            cghub.table.$selectAllCheckbox.prop('checked',
                cghub.table.$checkboxes.length == $('.data-table-checkbox:checked').length);
        },
        repairSelection:function() {
            var selected_items = cghub.selected.ids();
            if (selected_items.length) {
                for (var item in selected_items) {
                    var checkbox = $('.data-table-checkbox[value='+selected_items[item]+']');
                    if(checkbox.length) {
                        checkbox.prop('checked', true);
                    }
                }
                if($('input.data-table-checkbox:checked').length == $('input.data-table-checkbox').length) {
                    $('.js-select-all').prop('checked', true);
                }
            }
        },
        tableCheckboxFocus:function(event){
            if (event.type == 'focusin'){
                $(this).parents('td').addClass('tdSelected');
            }
            else if (event.type == 'focusout') {
                $(this).parents('td').removeClass('tdSelected');
                if(cghub.table.clearSelectionTimeout) {
                    clearTimeout(cghub.table.clearSelectionTimeout);
                }
                cghub.table.clearSelectionTimeout = setTimeout(function(){
                    var selected = $('.tdSelected');
                    if(selected.length == 1 && !selected.find('input').length) {
                        selected.removeClass('tdSelected');
                    }
                }, 500);
            }
        },
        arrowPress:function(event){
            /* alt + arrow press handler
            arrowLeft: 37
            arrowUp: 38
            arrowRight: 39
            arrowDown: 40 */
            var charCode = (event.which) ? event.which : event.keyCode;
            if(event.ctrlKey && charCode == 13) {
                /* show details in new tab */
                var target = $('td.tdSelected');
                if(target.length) {
                    window.open(
                            target.parents('tr').find('.details-link').attr('data-details-url'),
                            '_blank');
                    window.focus();
                }
                return false;
            }
            if(!event.altKey) return;
            if(charCode == 18) return false;
            if(charCode == 13) {
                /* show details popup on alt + enter click */
                $('td.tdSelected').parents('tr').find('.details-link').click();
                return false;
            }
            if($.inArray(charCode, [37, 39, 38, 40]) == -1) return;
            var currentCell = $('td.tdSelected');
            if(currentCell.length > 1){
                currentCell = currentCell.eq(1);
            }
            var nextStep = currentCell;
            var currentRow = currentCell.parents('tr');
            var currentIndex = currentRow.children().index(currentCell);
            var nextRow = currentRow;
            //left
            if (charCode == 37){
                do
                    nextStep = $(nextStep).prev();
                while (nextStep.is('td') && !$(nextStep).is(":visible"));
            }
            //right
            if (charCode == 39){
                do
                    nextStep = $(nextStep).next();
                while (nextStep.is('td') && !$(nextStep).is(":visible"));
            }
            //up
            if (charCode == 38){
                nextRow = $(nextRow).prev();
                if (!nextRow.is('tr')) return false;
                nextStep = nextRow.find('td:nth-child('+(currentIndex+1)+')');
            }
            //down
            if (charCode == 40){
                nextRow = $(nextRow).next();
                if (!nextRow.is('tr')) return false;
                nextStep = nextRow.find('td:nth-child('+(currentIndex+1)+')');
            }

            if(!nextStep.is('td')) return false;
            $('.tdSelected').removeClass("tdSelected");
            nextStep.addClass('tdSelected');
            /* set focus to row checkbox */
            nextStep.parents('tr').find('input').focus();

            cghub.table.scrollTableToCell(nextStep);

            return false;
        },
        scrollTableToCell:function(target){
            /* is cell fully visible ? */
            var cell_left = $(target).offset().left;
            var cell_right = cell_left + $(target).width();
            var table_left = cghub.table.$flexigrid.offset().left;
            var table_right = table_left + cghub.table.$flexigrid.width();
            if(cell_right > table_right) {
                cghub.table.$tableContainer.scrollLeft(cghub.table.$tableContainer.scrollLeft() + cell_right - table_right + 50);
            }
            if(cell_left < table_left) {
                cghub.table.$tableContainer.scrollLeft(cghub.table.$tableContainer.scrollLeft() - table_left + cell_left - 50);
            }
        }
    }
    cghub.table.init();
});
