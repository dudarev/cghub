/*jslint browser: true*/
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
        },
        activateItemDetailsLinks:function () {
            $(document).on('click', '.bDiv a', function(e) {
                e.stopPropagation();
            });
            $(document).on('click', '.bDiv tr', function(obj){
                var $first_td = $(obj.target).find('input[name=selected_files]');
                if(obj.target.name=='selected_files' || $first_td.length) { return; }
                var $tr = $(this);
                var modal = $($tr.attr('data-target'));
                var loaded = false;
                modal.on('shown', function(){
                    if (!loaded){
                        // ajax is hack for for IE10
                        modal.find('.modal-body').load($tr.attr('data-details-url')+'?ajax=1', function(response, status, xhr){
                            if (status == "error") {
                                modal.find('.modal-body').html('There was an error loading data. Please contact admin: <a href="mailto:'+cghub.vars.supportEmail+'">'+cghub.vars.supportEmail+'</a>');
                            } else {
                                loaded = true;
                            }
                        });
                    }
                }).on('show', function(){
                    modal.find('.modal-body').html('Loading ...');
                    modal.find('.modal-label').html('Details for Analysis Id '+$tr.attr('data-analysis_id'));
                }).modal('show');
                return false;
            });
            $(document).on('click', '.js-details-popup', function() {
                var $tr = $($(this).parents('ul').data('e').target).parents('td');
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
                    window.open(target.parents('tr').attr('data-details-url'), '_blank');
                    window.focus();
                }
                return false;
            }
            if(!event.altKey) return;
            if(charCode == 18) return false;
            if(charCode == 13) {
                /* show details popup on alt + enter click */
                $('td.tdSelected').click();
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
