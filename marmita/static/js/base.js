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
      $a.append(data + ' 0.0');
      $('.list-group').append($a);
      $('.button-wrapper').find('.a-btn-slide-text').empty().append(data);
    });
  });


  $('.people_manager').on('click', '.uncheck_icon, .check_icon', function() {
    var $el = $(this);
    var class_ = $el.attr('class');
    var request = $.ajax({
      url: 'meals/check_uncheck/',
      type: 'POST',
      data: {
        'type_of': $(this).attr('rel'),
        'date': $('#datepicker').val(),
        'person_pk': $(this).parents('tr').find('.person').attr('rel'),
        'check_uncheck': class_,
      },
    });
    request.done(function( data ) {
      $el.attr('class', 'check_icon');
      if (class_ == 'uncheck_icon') {
        if (data['wash'] == true) {
          /*$el.parents('table').find('[rel="wash"]').each(function() {
            $(this).attr('class', 'uncheck_icon');
          });*/
          $el.parents('table').find('.check_icon[rel=wash]').attr('class', 'uncheck_icon');
          $el.attr('class', 'check_icon');
          $el.parents('tr').find('.uncheck_icon').attr('class', 'check_icon');
        }
      } else if (class_ == 'check_icon') {
        if (data['wash'] == false) {
          $el.parents('tr').find('.check_icon').attr('class', 'uncheck_icon')
        }
        $el.attr('class', 'uncheck_icon');
      }
      $('.list-group-item').remove();

      $('.list-group').append("<a href='javascript:void(0);' class='active list-group-item'>Ranking</a>");
      for (var i = 0; i < data['number_of_people']; i++) {
        $a = $('<a>');
        $a.attr('href', 'javascript:void(0);');
        $a.attr('class', 'list-group-item person_ranking');
        // person data [3] comes with the result of a person if he is new or not
        if (data['person_data'][i][3] == true) {
          $a.addClass('im_new');
        }
        // person data [4] is the pk of the person at Data Base
        $a.attr('rel', data['person_data'][i][4]);
        /*
        person data [0] is the name of the person
        person data [1] is the media between the number of times the person
          washed the dishes compared to the times he ate
        person data [2] is the number to be used in case of tie ate [1]
        */
        $a.text(data['person_data'][i][0]+' '+data['person_data'][i][1]+' | '+data['person_data'][i][2])
        $('.list-group').append($a);
      }

      $('.button-wrapper').remove();
      if (data['number_of_meals']==0) {
        $('.lavar').find('.text-center').text('Não há ninguém para lavar.');
      } else {
        $div = $('<div>');
        $div.addClass('button-wrapper');
        $('.a-btn-slide-text').text(data['washer']);
        $a = $('<a>');
        $a.attr('href', 'javascript:void(0);');
        $a.addClass('a-btn');
        $a.attr('href', 'javascript:void(0);');
        $a.attr('style', 'text-decoration:none');
        $span = $('<span>');
        $span.addClass('a-btn-text');
        $span.text('Veja');
        $a.append($span);
        $span = $('<span>');
        $span.attr('class', 'a-btn-slide-text');
        $span.text(data['washer']);
        $a.append($span);
        $span = $('<span>');
        $span.attr('class', 'a-btn-icon-right');
        $span2 = $('<span>');
        $span.append($span2);
        $a.append($span);
        $div.append($a);
        $('.lavar').append($div)
        $('.lavar').find('.text-center').text('De quem é a vez de lavar?');
      }
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
