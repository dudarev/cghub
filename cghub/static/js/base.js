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
        tabPressed: 0,
        init:function () {
            cghub.base.cacheElements();
            cghub.base.bindEvents();
            cghub.base.mockIePlaceholder();
            cghub.base.activateSkipNavigation();
        },
        cacheElements:function () {
            cghub.base.$navbarAnchors = $('header.navbar ul.nav li a');
            cghub.base.$navbarListItem = $('header.navbar ul li');
            cghub.base.$messageModal = $('#messageModal');
            cghub.base.$messageModal = $('#messageModal');
            cghub.base.$searchForm = $('form.navbar-search');
            cghub.base.$accessibilityLinks = $('#accessibility-links');
        },
        bindEvents:function () {
            cghub.base.defineActiveLink();
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
            if (a_el.href.split('?')[0] !== (window.location.origin + window.location.pathname)) {
                pageLink.closest('li').removeClass('active');
            } else {
                pageLink.closest('li').addClass('active');
            }
        },
        activateSkipNavigation:function () {
            /* default main content - base container */
            if(!$('#main-content').length) {
                $('.base-container').attr('id', 'main-content');
            }
            /* fix webkit bug 17450 */
            if($.browser.webkit) {
                if(window.location.hash) {
                    var anchor = $(window.location.hash);
                    if(anchor.length) {
                        setTimeout(function() {
                            $(window).scrollTop(anchor.offset().top);
                            anchor.focus();
                        }, 0)
                    }
                }
            }
            cghub.base.$accessibilityLinks.find('a').on('click', function() {
                var anchor = $($(this).attr('href'));
                if(anchor.length) {
                    $(window).scrollTop(anchor.offset().top - 50);
                    var $controls = anchor.find('a, input, button, .ui-dropdownchecklist-selector').filter(':visible');
                    if($controls.length) {
                        $controls.eq(0).focus();
                    } else {
                        anchor.focus();
                        $(this).parents('ul').css({'height': 0});
                    }
                }
                return false;
            });
            cghub.base.$accessibilityLinks.on('focusin', function(){
                if(cghub.base.hideSkipLinksTimeout) {
                    clearTimeout(cghub.base.hideSkipLinksTimeout);
                }
                $(this).css({height: 'auto'});
            }).on('focusout', function(e) {
                var $this = $(this);
                cghub.base.hideSkipLinksTimeout = setTimeout(function() {
                    $this.css({height: 0});
                }, 100);
            });
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
