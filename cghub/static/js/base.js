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
            cghub.base.$messageModal = $('#messageModal');
            cghub.base.taskStatusURL = $('body').data('task-status-url');
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
            cghub.base.activateItemDetailsLinks();
            cghub.base.activateTaskStatusChecking();
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
        activateTaskStatusChecking:function () {
            setTimeout(cghub.base.activateTaskStatusChecking, 30000);
            var tasks = $.cookie('active_tasks');
            if(tasks) {
                var task_id = tasks.split(',')[0];
                $.ajax({
                    url: cghub.base.taskStatusURL,
                    dataType: "json",
                    data: {'task_id': task_id},
                    type: 'GET',
                    success: function (data) {
                        var status = data['status'];
                        if(status=='success' || status=='failure') {
                            tasks = tasks.split(',');
                            if(tasks.length > 1) {
                                tasks.shift();
                                $.cookie('active_tasks', tasks.join(','), { path: '/' });
                            } else {
                                $.removeCookie('active_tasks', { path: '/' });
                            }
                        }
                        if(status=='failure') {
                            cghub.base.$messageModal.find('.modal-label').text('Error Adding to Cart');
                            cghub.base.$messageModal.find('.modal-body').html('There was an error while adding to the cart. Please contact admin.');
                            cghub.base.$messageModal.modal();
                        }
                    }
                });
            }
        },
    };
    cghub.base.init();
});
