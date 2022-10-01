$('#self_report_button').click(function(){
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    resultData['round_num'] = $("#round_num").text();
    resultData['page_round'] = $("#page_round").text();
    $.ajax({
      url:'/ARPicture/self_report_click/',
      type:'POST',
      data: resultData,
      datatype: 'json',
      success:function (response) {
        console.log(response);
        if (response['status'] == 'error'){
          alert("error!", response['errormessage']);
          return;
        }
        if (response['have_next_page']){
          if(response['running_mode'] == 'Testing'){
            url = "/ARPicture/question_" + resultData['page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/'
          } else {
            url = "/ARPicture/smooth_music/" + response['uaid'] + '/' + response['round_num'] + '/' + resultData['page_round'] + '/'
          }
          window.location.href = url;
        } else {
          if(response['running_mode'] == 'Testing'){
            url = "/ARPicture/question_" + response['next_page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/'
          } else {
            url = "/ARPicture/smooth_music/" + response['uaid'] + '/' + response['round_num'] + '/' + resultData['page_round'] + '/'
          }
          window.location.href = url;
        }
      }
    })
  }
  )
  