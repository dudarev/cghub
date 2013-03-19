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
            return;
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
                if(obj.target.name=='selected_files') { return };
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
    };
    cghub.base.init();
});
