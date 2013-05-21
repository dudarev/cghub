/*jslint browser: true*/
jQuery(function ($) {
    'use strict';
    var cghub = {};
    if (this.cghub !== undefined) {
        cghub = this.cghub;
    } else {
        this.cghub = cghub;
    }
    cghub.accessibility = {
        init:function () {
            cghub.accessibility.fixDDCLs();
            cghub.accessibility.attachAbbrs();
            cghub.accessibility.refreshFiltersDDCL();
        },
        attachAbbrs:function(){
            cghub.accessibility.insertAbbrs('.sidebar > div .ui-dropdownchecklist-item > label');
            cghub.accessibility.insertAbbrs('.applied-filters > ul > li');
            cghub.accessibility.insertAbbrs('.flexigrid td[headers] > div');
            cghub.accessibility.insertAbbrs('.details-content table td');
        },
        insertAbbrs: function(selector) {
            var $elements = $(selector);
            if(!$elements.length) return;
            $elements.each(function(){
                var text = $(this).text().trim();
                var parts = text.split(/([\-\_\/\s])/); // split by '-', '_', '/', ' ' to get array of pure strings and separators
                for (var i in parts) {
                    var found = parts[i].match(/[A-Z]{2,5}/g);
                    if (found && found.length == 1){
                        parts[i] = '<abbr>' + parts[i] + '</abbr>';
                    }
                }
                $(this).html(parts.join(''));
            });
        },
        refreshFiltersDDCL:function() {
            var $filters = $('select.filter-select');
            if(!$filters.length) return;
            $filters.each(function(){
                if(!$(this).hasClass('date-filters')) {
                    cghub.search.ddclOnComplete($(this));
                }
            });
        },
        fixDDCLs:function() {            
            $('.ui-dropdownchecklist-dropcontainer').attr('tabindex', -1);
            /* add text for screen readers for ddcl-id-columns-selector */
            $('#ddcl-id-columns-selector .ui-dropdownchecklist-selector')
                .prepend('<div class="hidden">' + $('#id-columns-selector').attr('title') + ', selected:</div>')
                .attr('id', 'id-columns-ui-selector').attr('aria-labelledby', 'id-columns-ui-selector');
            /* add text for screenreaders for filters */
            $('.sidebar .ui-dropdownchecklist-selector').each(function() {
                var filter_name = $(this).parent().prev().prev().text().toLowerCase().slice(0,-1);
                var filter_slug = $(this).parent().prev().attr('id').split('id-')[1];
                $(this).prepend('<div class="hidden">Filter ' + filter_name + ', selected:</div>');
                $(this).attr('id', 'id-' + filter_slug + '-ui-selector').attr('aria-labelledby', 'id-' + filter_slug + '-ui-selector');
            });
        },
    };
    cghub.accessibility.init();
});

