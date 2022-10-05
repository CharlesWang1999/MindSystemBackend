$('#self_report_button').click(function(){
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    resultData['round_num'] = $("#round_num").text();
    resultData['page_round'] = $("#page_round").text();
    resultData['question_info'] = $('input[name="place1"]:checked').val()
    resultData['other_info'] = $('input[name="other_info"]').val()
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
            if (resultData['page_round'] == 's2'||resultData['page_round'] == 's1') {
              url = "/ARPicture/question_" + resultData['page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/' +response['running_mode'] + '/'
            }
          } else {
            url = "/ARPicture/smooth_music/" + response['uaid'] + '/' + response['round_num'] + '/' + resultData['page_round'] + '/'
            if (resultData['page_round'] == 's1') {
              url = "/ARPicture/question_" + resultData['page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/' +response['running_mode'] + '/'
            }
          }
          window.location.href = url;
        } else {
          if(response['running_mode'] === 'Testing'){
            url = "/ARPicture/question_" + response['next_page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/'
            if(response['next_page_round'] == 's4') {
              url = "/ARPicture/finish/" + resultData['uaid'] + '/'
            }
            else if (response['next_page_round'] == 's2'|| response['next_page_round'] === 'link'||resultData['next_page_round'] == 's1') {
              url = "/ARPicture/question_" + response['next_page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/' +response['running_mode'] + '/'
            }
          } else {
            url = "/ARPicture/smooth_music/" + response['uaid'] + '/' + response['round_num'] + '/' + resultData['page_round'] + '/'
            if (response['next_page_round'] === 'link'||resultData['next_page_round'] == 's1'){
              url = "/ARPicture/question_" + response['next_page_round'] + "/" + response['uaid'] + '/' + response['next_round_num'] + '/' +response['running_mode'] + '/'
            }
          }
          window.location.href = url;
        }
      }
    })
  }
  )
  