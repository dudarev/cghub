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
        usedReservedCharsTitle: 'Using "*" or "?" in search query are disallowed',
        usedReservedCharsContent: '"*" and "?" chars reserved for future extensions',
        reservedChars: '*?',
        init:function () {
            cghub.base.cacheElements();
            cghub.base.bindEvents();
            cghub.base.mockIePlaceholder();
        },
        cacheElements:function () {
            cghub.base.$navbarAnchors = $('div.navbar ul.nav li a');
            cghub.base.$navbarListItem = $('div.navbar ul li');
            cghub.base.$messageModal = $('#messageModal');
            cghub.base.$messageModal = $('#messageModal');
            cghub.base.$searchForm = $('form.navbar-search');
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
            cghub.base.activateTaskStatusChecking();
            cghub.base.$searchForm.on('submit', cghub.base.checkSearchField);
        },
        showMessage: function (title, content) {
            cghub.base.$messageModal.find('.modal-label').text(title);
            cghub.base.$messageModal.find('.modal-body').html(content);
            cghub.base.$messageModal.modal();
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
        activateTaskStatusChecking:function () {
            setTimeout(cghub.base.activateTaskStatusChecking, 30000);
            var tasks = $.cookie('active_tasks');
            if(tasks) {
                var task_id = tasks.split(',')[0];
                $.ajax({
                    url: cghub.vars.taskStatusUrl,
                    dataType: "json",
                    data: {'task_id': task_id},
                    type: 'GET',
                    success: function (data) {
                        var status = data['status'];
                        if(status=='success' || status=='failure') {
                            tasks = tasks.split(',');
                            if(tasks.length > 1) {
                                tasks.shift();
                                $.cookie('active_tasks', tasks.join(','), { path: '/', expires: 7 });
                            } else {
                                $.removeCookie('active_tasks', { path: '/' });
                            }
                        }
                        if(status=='failure') {
                            cghub.base.$messageModal.find('.modal-label').text('Error Adding to Cart');
                            cghub.base.$messageModal.find('.modal-body').html(
                                'There was an error while adding to the cart. Please contact admin: <a href="mailto:support@cghub.ucsc.edu">support@cghub.ucsc.edu</a>');
                            cghub.base.$messageModal.modal();
                        }
                    }
                });
            }
        },
        mockIePlaceholder:function() {
            $('input[placeholder]').placeholder();
            if($.browser.msie) {
                $('input[placeholder]').css({'height': '18px', 'line-height': '18px'})
            }
        },
        checkSearchField:function(){
            var searchValue = $(this).find('input').val();
            for (var i = 0; i < cghub.base.reservedChars.length; i++){
                if (searchValue.indexOf(cghub.base.reservedChars[i]) != -1){
                    cghub.base.showMessage(cghub.base.usedReservedCharsTitle, cghub.base.usedReservedCharsContent);
                    return false;
                }
            }
            return true;
        }
    };
    cghub.base.init();
});
