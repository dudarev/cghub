/*jslint browser: true*/
jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.table = {
        init:function () {
            cghub.table.cacheElements();
            cghub.table.bindEvents();
            cghub.table.selectFiles();
            cghub.table.$selectAllCheckbox.removeAttr('disabled');
        },
        cacheElements:function () {
            cghub.table.$itemsPerPageLink = $('div.items-per-page-label > a');
            cghub.table.$selectAllCheckbox = $('.js-select-all');
            cghub.table.$checkboxes = $('.data-table-checkbox');
            cghub.table.$flexigrid = $('.flexigrid');
            cghub.table.$tableContainer = $('.bDiv');
        },
        bindEvents:function () {
            cghub.table.activateItemDetailsLinks();
            cghub.table.$itemsPerPageLink.on('click', cghub.table.saveSelectedFiles);
            cghub.table.$selectAllCheckbox.on('change', cghub.table.changeCheckboxes);
            cghub.table.$checkboxes.on('change', cghub.table.updateSelectAll);
            cghub.table.$checkboxes.on('focusin', cghub.table.tableCheckboxFocus);
            cghub.table.$checkboxes.on('focusout', cghub.table.tableCheckboxFocus);
            cghub.table.$flexigrid.on('keydown', cghub.table.arrowPress);
        },
        activateItemDetailsLinks:function () {
            $(document).on('click', '.bDiv tr', function(obj){
                var $first_td = $(obj.target).find('input[name=selected_files]');
                if(obj.target.name=='selected_files' || $first_td.length) { return };
                var $tr = $(this);
                var modal = $($tr.attr('data-target'));
                var loaded = false;
                modal.on('shown', function(){
                    if (!loaded){
                        modal.find('.modal-body').load($tr.attr('data-details-url'), function(response, status, xhr){
                            if (status == "error") {
                                modal.find('.modal-body').html('There was an error loading data. Please contact admin.');
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
        },
        changeCheckboxes:function () {
            cghub.table.$checkboxes.prop('checked', $(this).is(':checked'));
            return;
        },
        updateSelectAll:function () {
            cghub.table.$selectAllCheckbox.prop('checked',
                cghub.table.$checkboxes.length == $('.data-table-checkbox:checked').length);
        },
        selectFiles: function() {
            var selected_items = $.cookie('browser_checked_items');
            if (selected_items) {
                selected_items = selected_items.split(',');
                for (var item in selected_items) {
                    var checkbox = $('.data-table-checkbox[value='+selected_items[item]+']');
                    if(checkbox.length) {
                        checkbox.prop('checked', true);
                    }
                }
                if($('input.data-table-checkbox:checked').length == $('input.data-table-checkbox').length) {
                    $('.js-select-all').prop('checked', true);
                }
                $.removeCookie('browser_checked_items', { path: '/' });
            }
        },
        saveSelectedFiles:function(){
            var selected_items = [];
            $('form .data-table-checkbox').serializeArray().map(
                function(i) {
                    selected_items.push(i.value);
                }
            )
            $.cookie('browser_checked_items', selected_items.join(','), { path: '/', expires: 7 });
        },
        tableCheckboxFocus:function(event){
            if (event.type == "focusin" && !$('.tdSelected').length){
                $(this).parents('td').addClass("tdSelected");
            }
            else if (event.type == "focusout" && $(this).parents('td').hasClass("tdSelected")) {
                $('.tdSelected').removeClass("tdSelected");
            }
        },
        arrowPress:function(event){
            /* alt + arrow press handler
            arrowLeft: 37
            arrowUp: 38
            arrowRight: 39
            arrowDown: 40 */
            if(!event.altKey) return;
            var charCode = (event.which) ? event.which : event.keyCode;
            if($.inArray(charCode, [37, 39, 38, 40]) == -1) return;
            var currentCell = $('td.tdSelected');
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
