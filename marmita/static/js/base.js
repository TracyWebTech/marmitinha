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

  $('.uncheck_icon').click(function() {
    var $el = $(this);
    var request = $.ajax({
      url: $(this).parent().parent().attr('rel'),
      type: 'POST',
      data: {
        'type_of': $(this).attr('rel'),
        'date': $('#datepicker').val(),
        'person_pk': $(this).parent().parent().find('.person').attr('rel'),
      },
    });
    request.done(function( data ) {
      $el.attr('class', 'check_icon');
      if (data == 'wash') {
        $el.parents('table').find('[rel="wash"]').each(function() {
          $(this).attr('class', 'uncheck_icon');
        });
        $el.parents('tr').find('.uncheck_icon').each(function() {
          $(this).attr('class', 'check_icon');
        });
      }
    });
  });
});
