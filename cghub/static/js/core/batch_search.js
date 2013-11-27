jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.batch_search = {
        init:function () {
            cghub.batch_search.cacheElements();
            cghub.batch_search.initFlexigrid();
            cghub.batch_search.bindEvents();
        },
        cacheElements:function () {
            cghub.batch_search.$searchTable = $('table.data-table');
            cghub.batch_search.$removeBtn = $('.ids-remove');
            cghub.batch_search.$addToCartBtn = $('.ids-add-to-cart');
            cghub.batch_search.$addToCartInput = $('input[name=add_to_cart]');
            cghub.batch_search.$ResetBtn = $('button[type=reset]');
            cghub.batch_search.$idsStorage = $('.js-ids-storage');
            cghub.batch_search.$paginationLinks = $('.pagination li a');
            cghub.batch_search.$form = $('form');
            cghub.batch_search.$items_per_page_links = $('.items-per-page-label a');
        },
        bindEvents:function () {
            cghub.batch_search.$removeBtn.on('click', cghub.batch_search.removeIDs);
            cghub.batch_search.$paginationLinks.on('click', cghub.batch_search.goToPage);
            cghub.batch_search.$items_per_page_links.on('click', cghub.batch_search.goToPage);
            cghub.batch_search.$addToCartBtn.on('click', cghub.batch_search.addToCart);
            cghub.batch_search.$ResetBtn.on('click', cghub.batch_search.clearForm);
        },
        initFlexigrid:function () {
            cghub.batch_search.$searchTable.flexigrid({height: 'auto', showToggleBtn: false});
            $('.data-table').css('visibility', 'visible');
            /* add fieldset element */
            var $data_table = $('.bDiv table');
            $data_table.wrap($('<fieldset/>'));
            $data_table.parent().prepend($('<legend class="hidden">Select files to remove from:</legend>'));
            /* disable sorting */
            $('.sort-link').attr('title', '').attr('href', '#').on('click', function() {
                return false;
            });
        },
        clearForm:function () {
            var $fileinput = cghub.batch_search.$form.find('input[type=file]');
            if (cghub.batch_search.$form.length) {
                if ($.browser.msie) {
                    $fileinput.replaceWith($fileinput.clone());
                } else {
                    $fileinput.val('');
                }
                cghub.batch_search.$form.find('textarea').val('');
            }
            return false;
        },
        removeIDs:function () {
            cghub.selected.save();
            if(!cghub.selected.exists) return false;
            var ids = cghub.batch_search.$idsStorage.val().split(' ');
            $.each(cghub.selected.get_ids_list(), function(i, id) {
                var index = ids.indexOf(id);
                if (index != -1) {
                    ids.splice(index, 1)
                }
            });
            cghub.batch_search.$idsStorage.val(ids.join(' '))
        },
        goToPage:function () {
            var link = $(this);
            if(link.parent().hasClass('disabled') || link.parent().hasClass('active')) return false;
            var action = $(this).attr('href');
            cghub.batch_search.$form.attr('action', action).submit();
            return false;
        },
        addToCart:function () {
            cghub.batch_search.$addToCartInput.val('true');
        },
    };
    cghub.batch_search.init();
});
