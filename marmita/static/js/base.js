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
      $('.people_manager').find('.check_icon').each(function () {
        $(this).attr('class', 'uncheck_icon');
      });
      for (index in data) {
        var person_l = $('.person[rel="'+data[index][0]+'"]').parent();
        person_l.find('[rel="eat"]').attr('class', 'check_icon');
        if (data[index][1] == true) {
          person_l.find('[rel="wash"]').attr('class', 'check_icon');
        }
      }
    });
  });
});
