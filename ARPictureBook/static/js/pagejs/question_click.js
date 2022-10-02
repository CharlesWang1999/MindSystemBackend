$('#question_button').click(function () {
  var resultData = {}
  resultData['uaid'] = $("#uaid").text();
  resultData['round_num'] = $("#round_num").text();
  resultData['page_round'] = $("#page_round").text();
  console.log('@6--', $("#question_form").serialize())
  $.ajax({
    url: '/ARPicture/question_click/',
    type: 'POST',
    data: resultData,
    datatype: 'json',
    success: function (response) {
      console.log(response);
      if (resultData['page_round'] === 'link') {
        if (response['running_mode'] === 'Testing') {
          if (response['have_next_page']) {
            url = "/ARPicture/question_link/" + resultData['uaid'] + '/' + response['next_round_num'] + '/'
          } else {
            url = "/ARPicture/question_s2/" + resultData['uaid'] + '/1/'
          }
        } else {
          url = "/ARPicture/smooth_music/" + resultData['uaid'] + '/' + resultData['round_num'] + '/link/'
        }
      } else {
        url = "/ARPicture/self_report_" + resultData['page_round'] + "/" + resultData['uaid'] + '/' + resultData['round_num'] + '/'
      }
      // window.location.href = url;
    }
  })
}
)
