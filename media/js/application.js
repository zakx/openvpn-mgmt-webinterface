$('document').ready(function() {
  
  /******************
    Tablet rotation
  ******************/
  
  var isiPad = navigator.userAgent.match(/iPad/i) !== null;
  
  if(isiPad) {
    $('body').prepend('<div id="rotatedevice"><h1>Please rotate your device 90 degrees.</div>');
  }
  
  /********
    Login
  ********/
  
  $('#login_entry > a').click(function() {
    $(this).fadeOut(200, function() {
      $('#login_form').fadeIn();
    });

    return false;
  });
  
  /********************
    Modal preparation
  ********************/
  
  $('body').prepend('<div id="overlay"><div id="modalcontainer"></div></div>');
  
  /*******
    PJAX
  *******/
  
  $('nav#primary a').click(function() {
    window.location = $(this).attr("href");
    return false;
  });
  
  $('nav#secondary a').pjax({
    container: '#main',
    success: function(data) {
      init();
    }
  });
  
  /****************
    Notifications
  ****************/

  var maxHeight = $(window).height() - $('#secondary ul').height() - 50;
  $('#notifications').css({'max-height': maxHeight});
  
  $('#notifications ul li').livequery(function() {
    $('#notifications').fadeIn();
  });
  
  $('#notifications').prepend('<a href="#">Show all notifications</a>');
  
  $('#notifications > a').click(function() {
    var container = $('#notifications');
    var height = $('#notifications ul').height() + 24;
    
    if(container.hasClass('expanded')) {
      container.animate({'height': 42}, 200);
      container.removeClass('expanded');
      $(this).html('show all notifications');
    } else {
      container.animate({'height': height}, 200);
      container.addClass('expanded');
      $(this).html('hide notifications');
    }
    
    return false;
  });
  
  function init() {
    
    /**************************
      Obtrusive notifications
    **************************/
    
    $('.notification .close').click(function() {
      $(this).closest('.notification').animate({'opacity': 0.01}, 200, function() {
        $(this).slideUp(200);
      });
    });
    
    /*************
      Datepicker
    *************/
    
    $('.datepicker').datepicker();
        
    /***********
      Calendar
    ***********/
    
    $('#calendar').fullCalendar({
      events: [{
                title  : 'Event with another event',
                start  : '2012-01-16'
              },
              {
                title  : 'Another event',
                start  : '2012-01-19',
                end    : '2012-01-05'
              },
              {
                title  : 'Third eventw peofjpwo eifj pwoeifj pwoiefjpow iejf',
                start  : '2012-01-17 12:30:00',
                allDay : false
              },
              {
                title  : 'This is a multi-day event',
                start  : '2012-01-12 11:00:00',
                end    : '2012-01-14 13:30:00'
              }],
      editable: true,
      selectable: true,
      eventBackgroundColor: '#477dae',
      eventBorderColor: '#0E69A1',
      header: {
        left: '',
        center: 'title',
        right: 'prev,today,next month,basicWeek,basicDay'
      },
      buttonText: {
        prev: '<span class="glyph left"></span>',
        next: '<span class="glyph right"></span>'
      },
      aspectRatio: 2
    });
    
    /*****************
      Wysiwym-editor
    *****************/
   
    $('.wysiwym').wymeditor({
      logoHtml: '',
      toolsItems: [
        {'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'},
        {'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},
        {'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
        {'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
        {'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
        {'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
        {'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
        {'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},
        {'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
        {'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'}
      ],
      containersItems: [
        {'name': 'P', 'title': 'Paragraph', 'css': 'wym_containers_p'},
        {'name': 'H4', 'title': 'Heading_4', 'css': 'wym_containers_h4'}
      ]
    });
    
    /************
      Code view
    ************/
  
    $('code').each(function() {
      var elem = $(this);
      var lang = elem.attr("class");
    
      elem.sourcerer(lang);
    });
  
    /*************
      Datatables
    *************/
  
    $('.datatable').dataTable({
      "sPaginationType": "full_numbers",
      "bStateSave": true
    });
  
    $('.dataTables_wrapper').each(function() {
      var table = $(this);
      var info = table.find('.dataTables_info');
      var paginate = table.find('.dataTables_paginate');
    
      table.find('.datatable').after('<div class="action_bar nomargin"></div>');
      table.find('.action_bar').prepend(info).append(paginate);
    });
    
    /************************
      Combined input fields
    ************************/
    
    $('div.combined p:last-child').addClass('last-child');
  
    /**********
      Sliders
    **********/
  
    $(".slider").each(function() {
      var options = $(this).metadata();
      $(this).slider(options, {
        animate: true
      });
    });
  
    $(".slider-vertical").each(function() {
      var options = $(this).metadata();
      $(this).slider(options, {
        animate: true
      });
    });
    
    /*******
      Tags
    *******/
    
    $('.taginput').tagsInput({
      'width':'auto'
    });
  
    /****************
      Progress bars
    ****************/
  
    $(".progressbar").each(function() {
      var options = $(this).metadata();
      $(this).progressbar(options);
    });
  
    /**********************
      Modal functionality
    **********************/
  
    $('a.modal').each(function() {
      var link = $(this);
      var id = link.attr('href');
      var target = $(id);
      
      if($("#modalcontainer " + id).length === 0) {
        $("#modalcontainer").append(target);
      }
      
      $("#main " + id).remove();
    
      link.click(function() {
        $('#modalcontainer > div').hide();
        target.show();
        $('#overlay').show();
        return false;
      });
    });
  
    $('.close').click(function() {
      $('#modalcontainer > div').hide();
      $('#overlay').hide();
    
      return false;
    });
    
    /***********************
      Secondary navigation
    ***********************/
    
    $('nav#secondary > ul > li > a').click(function() {
      $('nav#secondary li').removeClass('active');
      $(this).parent().addClass('active');
    });
  
    /********************
      Pretty checkboxes
    ********************/
  
    $('input[type=checkbox], input[type=radio]').each(function() {
      if($(this).siblings('label').length > 0) {
        $(this).prettyCheckboxes();
      }
    });
  
    /**********************
      Pretty select boxes
    **********************/
  
    $('select').parent().each(function(index) {
      $(this).css('position', 'relative');
      $(this).css('z-index', 99-index);
    });
    
    $('select').chosen();
  
    /******************
      Window resizing
    ******************/

    $(window).resize(function() {
      $('.chzn-container').each(function(){
        $(".chzn-container").css({'width': '100%'});
        var res_wid_drop = ($(".chzn-container").width() - 2);
        $(".chzn-drop").css({'width': res_wid_drop});
      });
    });

    /*********************
      Pretty file inputs
    *********************/

    $('input[type="file"]').customFileInput();
    
    /*******
      Tabs
    *******/
  
    // Hide all .tab-content divs
    $('.tab-content').livequery(function() {
      $(this).hide();
    });

    // Show all active tabs
    $('.box-header ul li.active a').livequery(function() {
      var target = $(this).attr('href');
      $(target).show();
    });
  
    // Add click eventhandler
    $('.box-header ul li').livequery(function() {
      $(this).click(function() {
        var item = $(this);
        var target = item.find('a').attr('href');
        
        if($(target).parent('form').length > 0) {
          if($(target).parent('form').valid()) {
            item.siblings().removeClass('active');
            item.addClass('active');
    
            item.parents('.box').find('.tab-content').hide();
            $(target).show();
          }
        } else {
          item.siblings().removeClass('active');
          item.addClass('active');
    
          item.parents('.box').find('.tab-content').hide();
          $(target).show();
        }

        // Needed for Chosen plugin resizing
        $(window).trigger('resize');
    
        return false;
      });
    });
    
    /***********
      Tooltips
    ***********/
    
    $('.tooltip').tipsy({gravity: 's'});
  
    /******************
      Form Validation
    ******************/
  
    $("form").each(function() {
      $(this).validate({
        wrapper: 'span class="error"',
        meta: 'validate',
        highlight: function(element, errorClass, validClass) {
          if (element.type === 'radio') {
            this.findByName(element.name).addClass(errorClass).removeClass(validClass);
          } else {
            $(element).addClass(errorClass).removeClass(validClass);
          }
        
          // Show icon in parent element
          var error = $(element).parent().find('span.error');
        
          error.siblings('.icon').hide(0, function() {
            error.show();
          });
        },
        unhighlight: function(element, errorClass, validClass) {
          if (element.type === 'radio') {
            this.findByName(element.name).removeClass(errorClass).addClass(validClass);
          } else {
            $(element).removeClass(errorClass).addClass(validClass);
          }
        
          // Hide icon in parent element
          $(element).parent().find('span.error').hide(0, function() {
            $(element).parent().find('span.valid').fadeIn(200);
          });
        }
      });
    });
    
    // Calendar icon fix
    $('form p > .error').livequery(function() {
      $(this).siblings('span.calendar').hide();
    });
  
    // Add valid icons to validatable fields
    $('form p > *').each(function() {
      var element = $(this);
      
      if(element.metadata().validate) {
        element.parent().append('<span class="icon tick valid"></span>');
      }
    });
  }
  
  init();

});

/*************************
  Notification function!
*************************/

function notification(message, error, icon, image) {
  if(icon === null) {
    icon = 'tick2';
  }
  
  if(image) {
    image = 'icon16';
  } else {
    image = 'glyph';
  }
  
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
    
  if (hours < 10) {
    hours = "0" + hours;
  }
  
  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  
  var time = hours + ':' + minutes;
  
  if(error) {
    $('#notifications ul').append('<li class="error"><span class="' + image + ' cross"></span> ' + message + ' <span class="time">' + time + '</span></li>');
  } else {
    $('#notifications ul').append('<li><span class="' + image + ' ' + icon + '"></span> ' + message + ' <span class="time">' + time + '</span></li>');
  }
  
  $('#notifications ul li:last-child').hide();
  $('#notifications ul li:last-child').slideDown(200);
}