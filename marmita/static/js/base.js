$(function () {
  $('#btn_add_person').click(function() {
    var name = $('#add_person').val();
    if (!name) {
      $(this).parent().find('.status').empty().append('Não foi possível criar a pessoa');
      return false;
    }
    var request = $.ajax({
      url: $(this).attr('rel'),
      type: 'POST',
      data: {'name': name},
    });
    request.done(function ( data ) {
      $('.empty_ranking').remove();
      $a = $('<a>');
      $a.attr('class', 'list-group-item im_new');
      $a.append(data + ' 0,0');
      $('.list-group').append($a);
      $('.button-wrapper').find('.a-btn-slide-text').empty().append(data);
    });
  });

  $('.people_manager').on('click', '.uncheck_icon', function() {
    var $el = $(this);
    var request = $.ajax({
      url: $(this).parents('tr').attr('rel'),
      type: 'POST',
      data: {
        'type_of': $(this).attr('rel'),
        'date': $('#datepicker').val(),
        'person_pk': $(this).parents('tr').find('.person').attr('rel'),
      },
    });
    request.done(function( data ) {
      $el.attr('class', 'check_icon');
      if (data['wash'] == true) {
        $el.parents('table').find('[rel="wash"]').each(function() {
          $(this).attr('class', 'uncheck_icon');
        });
        $el.parents('tr').find('.uncheck_icon').each(function() {
          $(this).attr('class', 'check_icon');
        });
      }
      $('.person_ranking[rel="'+data['pk']+'"]').text(data['person_data']);
      $('.a-btn-slide-text').text(data['washer']);
    });
  });

  $('.people_manager').on('click', '.check_icon', function () {
    var $el = $(this);
    var request = $.ajax({
      url: $(this).parents('tbody').attr('rel'),
      type: 'POST',
      data: {
        'type_of': $(this).attr('rel'),
        'date': $('#datepicker').val(),
        'person_pk': $(this).parents('tr').find('.person').attr('rel'),
      },
    });
    request.done(function( data ) {
      $('.a-btn-slide-text').text(data['washer']);
      if (data['wash'] == true) {
        $el.attr('class', 'uncheck_icon');
        return false;
      }
      $el.parents('tr').find('.check_icon').each(function () {
        $(this).attr('class', 'uncheck_icon');
      });
    });
  });

  $('#datepicker').change(function () {
    var request = $.ajax({
      url: $(this).attr('rel'),
      type: 'POST',
      data: {'date': $(this).val(),},
    });
    request.done(function ( data ) {
      //console.log(data['list']);
      $('.people_manager').find('.check_icon').each(function () {
        $(this).attr('class', 'uncheck_icon');
      });                              
      $('#spinner').empty().val(data['tickets']); 
      for (index in data['list']) {
        var person_l = $('.person[rel="'+data['list'][index][0]+'"]').parent();
        person_l.find('[rel="eat"]').attr('class', 'check_icon');
        if (data['list'][index][1] == true) {
          person_l.find('[rel="wash"]').attr('class', 'check_icon');
        }
      }
    });
  });


  $('#updown').on('click', '.ui-icon-triangle-1-n', function () {                 
    var $el = $(this);                                                          
    var abcde = parseInt($('#spinner').val()) + 1; 
    var request = $.ajax({                                                      
      url: $(this).parent().attr('rel'),                                
      type: 'POST',                                                             
      data: {                                                                   
        'date': $('#datepicker').val(),                                         
        'ticket_num': abcde,
      },                                                                        
    });                                                                         
    request.done(function( data ) {
      $('#spinner').empty().val(abcde);
          
    });                                                                         
  });
  $('#updown').on('click', '.ui-icon-triangle-1-s', function () {               
    var $el = $(this);                                                          
    var abcde = parseInt($('#spinner').val()) - 1;                              
    var request = $.ajax({                                                      
      url: $(this).parent().attr('rel'),                                        
      type: 'POST',                                                             
      data: {                                                                   
        'date': $('#datepicker').val(),                                         
        'ticket_num': abcde,                                                    
      },                                                                        
    });                                                                         
    request.done(function( data ) {                                             
      $('#spinner').empty().val(abcde);                                         
                                                                                
    });                                                                         
  });


});
