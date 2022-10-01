$('#question_button').click(function(){
  var resultData = {}
  resultData['uaid'] = $("#uaid").text();
  resultData['round_num'] = $("#round_num").text();
  resultData['page_round'] = $("#page_round").text();
  $.ajax({
    url:'/ARPicture/question_click/',
    type:'POST',
    data: resultData,
    datatype: 'json',
    success:function (response) {
      console.log(response);
      url = "/ARPicture/self_report_" + resultData['page_round'] + "/" + resultData['uaid'] + '/' + resultData['round_num'] + '/'
      window.location.href = url;
    }
  })
}
)
