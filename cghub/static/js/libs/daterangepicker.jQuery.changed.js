(function ($) {

    /**
     * --------------------------------------------------------------------
     * jQuery-Plugin "daterangepicker.jQuery.js"
     * by Scott Jehl, scott@filamentgroup.com
     * reference article: http://www.filamentgroup.com/lab/update_date_range_picker_with_jquery_ui/
     * demo page: http://www.filamentgroup.com/examples/daterangepicker/
     *
     * Copyright (c) 2010 Filament Group, Inc
     * Dual licensed under the MIT (filamentgroup.com/examples/mit-license.txt) and GPL (filamentgroup.com/examples/gpl-license.txt) licenses.
     *
     * Dependencies: jquery, jquery UI datepicker, date.js, jQuery UI CSS Framework

     *  12.15.2010 Made some fixes to resolve breaking changes introduced by jQuery UI 1.8.7
     * --------------------------------------------------------------------
     */
    $.fn.daterangepicker = function(settings){
        var rangeInput = $(this);

        //defaults
        var options = $.extend({
            presets: {
                dateRange: 'Date Range'
        },
        rangeStartTitle: 'Start date',
        rangeEndTitle: 'End date',
        nextLinkText: 'Next',
        prevLinkText: 'Prev',
        target: rangeInput,
        doneButtonText: 'Submit',
        closeButtonText: 'Close',
        earliestDate: Date.parse('-15years'), //earliest date allowed 
        latestDate: Date.parse('+15years'), //latest date allowed 
        constrainDates: false,
        rangeSplitter: '-', //string to use between dates in single input
        dateFormat: 'm/d/yy', // date formatting. Available formats: http://docs.jquery.com/UI/Datepicker/%24.datepicker.formatDate
        closeOnSelect: false, //if a complete selection is made, close the menu
        arrows: false,
        appendTo: 'body',
        onClose: function(){},
        onOpen: function(){},
        onChange: function(){},
        datepickerOptions: null //object containing native UI datepicker API options
    }, settings);
    
    

    //custom datepicker options, extended by options
    var datepickerOptions = {
        onSelect: function(dateText, inst) {
            var range_start = rp.find('.range-start');
            var range_end = rp.find('.range-end');
                
            if(rp.find('.ui-daterangepicker-specificDate').is('.ui-state-active')){
                range_end.datepicker('setDate', range_start.datepicker('getDate') ); 
            }
            
            $(this).trigger('constrainOtherPicker');
            
            var rangeA = fDate( range_start.datepicker('getDate') );
            var rangeB = fDate( range_end.datepicker('getDate') );
            
            //send back to input or inputs
            if(rangeInput.length == 2){
                rangeInput.eq(0).val(rangeA);
                rangeInput.eq(1).val(rangeB);
            }
            else{
                rangeInput.val((rangeA != rangeB) ? rangeA+' '+ options.rangeSplitter +' '+rangeB : rangeA);
            }
            //if closeOnSelect is true
            if(options.closeOnSelect){
                if(!rp.find('li.ui-state-active').is('.ui-daterangepicker-dateRange') && !rp.is(':animated') ){
                    hideRP();
                }

                $(this).trigger('constrainOtherPicker');

                options.onChange();
            }
        },
        defaultDate: +0
    };

        //change event fires both when a calendar is updated or a change event on the input is triggered
        rangeInput.bind('change', options.onChange);

        //datepicker options from options
        options.datepickerOptions = (settings) ? $.extend(datepickerOptions, settings.datepickerOptions) : datepickerOptions;

        //Capture Dates from input(s)
        var inputDateA, inputDateB = Date.parse('today');
        var inputDateAtemp, inputDateBtemp;
        if(rangeInput.size() == 2){
            inputDateAtemp = Date.parse( rangeInput.eq(0).val() );
            inputDateBtemp = Date.parse( rangeInput.eq(1).val() );
            if(inputDateAtemp == null){inputDateAtemp = inputDateBtemp;}
            if(inputDateBtemp == null){inputDateBtemp = inputDateAtemp;}
        }
        else {
            inputDateAtemp = Date.parse( rangeInput.val().split(options.rangeSplitter)[0] );
            inputDateBtemp = Date.parse( rangeInput.val().split(options.rangeSplitter)[1] );
            if(inputDateBtemp == null){inputDateBtemp = inputDateAtemp;} //if one date, set both
        }
        if(inputDateAtemp != null){inputDateA = inputDateAtemp;}
        if(inputDateBtemp != null){inputDateB = inputDateBtemp;}


        //build picker and
        var rp = $('<div class="ui-daterangepicker ui-widget ui-helper-clearfix ui-widget-content ui-corner-all"></div>');
        var rpPresets = (function(){
                rangeInput.click(function(){
                    clickActions($(this),rp, rpPickers, doneBtn);
                    return false;
                });
        })();

        //function to format a date string
        function fDate(date){
             if(!date.getDate()){return '';}
             var day = date.getDate();
             var month = date.getMonth();
             var year = date.getFullYear();
             month++; // adjust javascript month
             var dateFormat = options.dateFormat;
             return $.datepicker.formatDate( dateFormat, date );
        }


        $.fn.restoreDateFromData = function(){
            if($(this).data('saveDate')){
                $(this).datepicker('setDate', $(this).data('saveDate')).removeData('saveDate');
            }
            return this;
        };
        $.fn.saveDateToData = function(){
            if(!$(this).data('saveDate')){
                $(this).data('saveDate', $(this).datepicker('getDate') );
            }
            return this;
        };

        //show, hide, or toggle rangepicker
        function showRP(){
            if(rp.data('state') == 'closed'){
                positionRP();
                rp.fadeIn(300).data('state', 'open');
                options.onOpen();
            }
        }
        function hideRP(){
            if(rp.data('state') == 'open'){
                rp.fadeOut(300).data('state', 'closed');
                options.onClose();
            }
        }
        function toggleRP(){
            if( rp.data('state') == 'open' ){ hideRP(); }
            else { showRP(); }
        }
        function positionRP(){
            var relEl = riContain || rangeInput; //if arrows, use parent for offsets
            var riOffset = relEl.offset(),
                side = 'left',
                val = riOffset.left,
                offRight = $(window).width() - val - relEl.outerWidth();

            if(val > offRight){
                side = 'right', val =  offRight;
            }

            rp.parent().css(side, val).css('top', riOffset.top + relEl.outerHeight());
        }



        //preset menu click events
        function clickActions(el, rp, rpPickers, doneBtn){
                doneBtn.hide();
                rpPickers.show();
                rp.find('.title-start').text(options.rangeStartTitle);
                rp.find('.title-end').text(options.rangeEndTitle);
                rp.find('.range-start').restoreDateFromData().css('opacity',1).show(400);
                rp.find('.range-end').restoreDateFromData().css('opacity',1).show(400);
                setTimeout(function(){doneBtn.fadeIn();}, 400);
                return false;
        }


        //picker divs
        var rpPickers = $('<div class="ranges ui-widget-header ui-corner-all ui-helper-clearfix"><div class="range-start"><span class="title-start">Start Date</span></div><div class="range-end"><span class="title-end">End Date</span></div></div>').appendTo(rp);
        rpPickers.find('.range-start, .range-end')
            .datepicker(options.datepickerOptions);


        rpPickers.find('.range-start').datepicker('setDate', inputDateA);
        rpPickers.find('.range-end').datepicker('setDate', inputDateB);

        rpPickers.find('.range-start, .range-end')
            .bind('constrainOtherPicker', function(){
                if(options.constrainDates){
                    //constrain dates
                    if($(this).is('.range-start')){
                        rp.find('.range-end').datepicker( "option", "minDate", $(this).datepicker('getDate'));
                    }
                    else{
                        rp.find('.range-start').datepicker( "option", "maxDate", $(this).datepicker('getDate'));
                    }
                }
            })
            .trigger('constrainOtherPicker');

        var doneBtn = $('<button class="btnDone ui-state-default ui-corner-all">'+ options.doneButtonText +'</button>')
        .click(function(){
            rp.find('.ui-datepicker-current-day').trigger('click');
            hideRP();
        })
        .appendTo(rpPickers);
        var closeBtn = $('<button class="btnClose ui-state-default ui-corner-all">'+ options.closeuttonText +'</button>')
        .click(function(){
            hideRP();
        })
        .appendTo(rpPickers);

        //inputs toggle rangepicker visibility
        $(this).click(function(){
            toggleRP();
            return false;
        });
        //hide em all
        rpPickers.hide().find('.range-start, .range-end, .btnDone').hide();

        rp.data('state', 'closed');

        //Fixed for jQuery UI 1.8.7 - Calendars are hidden otherwise!
        rpPickers.find('.ui-datepicker').css("display","block");

        //inject rp
        $(options.appendTo).append(rp);

        //wrap and position
        rp.wrap('<div class="ui-daterangepickercontain"></div>');

        //add arrows (only available on one input)
        if(options.arrows && rangeInput.size()==1){
            var prevLink = $('<a href="#" class="ui-daterangepicker-prev ui-corner-all" title="'+ options.prevLinkText +'"><span class="ui-icon ui-icon-circle-triangle-w">'+ options.prevLinkText +'</span></a>');
            var nextLink = $('<a href="#" class="ui-daterangepicker-next ui-corner-all" title="'+ options.nextLinkText +'"><span class="ui-icon ui-icon-circle-triangle-e">'+ options.nextLinkText +'</span></a>');

            $(this)
            .addClass('ui-rangepicker-input ui-widget-content')
            .wrap('<div class="ui-daterangepicker-arrows ui-widget ui-widget-header ui-helper-clearfix ui-corner-all"></div>')
            .before( prevLink )
            .before( nextLink )
            .parent().find('a').click(function(){
                var dateA = rpPickers.find('.range-start').datepicker('getDate');
                var dateB = rpPickers.find('.range-end').datepicker('getDate');
                var diff = Math.abs( new TimeSpan(dateA - dateB).getTotalMilliseconds() ) + 86400000; //difference plus one day
                if($(this).is('.ui-daterangepicker-prev')){ diff = -diff; }

                rpPickers.find('.range-start, .range-end ').each(function(){
                        var thisDate = $(this).datepicker( "getDate");
                        if(thisDate == null){return false;}
                        $(this).datepicker( "setDate", thisDate.add({milliseconds: diff}) ).find('.ui-datepicker-current-day').trigger('click');
                });
                return false;
            })
            .hover(
                function(){
                    $(this).addClass('ui-state-hover');
                },
                function(){
                    $(this).removeClass('ui-state-hover');
                });

            var riContain = rangeInput.parent();
        }


        $(document).click(function(){
            if (rp.is(':visible')) {
                hideRP();
            }
        });

        rp.click(function(){return false;}).hide();
        return this;
    }

})(jQuery);
