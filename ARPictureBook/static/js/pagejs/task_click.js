$('#task_button').click(function () {
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    resultData['round_num'] = '0';
    resultData['page_round'] = $("#page_round").text();
    console.log(resultData)
    $.ajax({
      url: '/ARPicture/task_click/',    
      type: 'POST',
      data: resultData,
      datatype: 'json',
      success: function (response) {
        console.log(response);
        // if (resultData['page_round'] === 'link') {
        //   // if (response['running_mode'] === 'Testing') {
        //   //   if (response['have_next_page']) {
        //   //     console.log(response['running_mode'])
        //   //     url = "/ARPicture/question_link/" + resultData['uaid'] + '/' + response['next_round_num'] + '/' + response['running_mode'] + '/'
        //   //   } else {
        //   //     url = "/ARPicture/question_s2/" + resultData['uaid'] + '/1/' + response['running_mode'] + '/'
        //   //   }
        //   // } else {
        //   //   url = "/ARPicture/smooth_music/" + resultData['uaid'] + '/' + resultData['round_num'] + '/link/'
        //   // }
        //   if (response['have_next_page']) {
        //     url = "/ARPicture/question_link/" + resultData['uaid'] + '/' + response['next_round_num'] + '/' + response['running_mode'] + '/'
        //   } else {
        //     url = "/ARPicture/question_s2/" + resultData['uaid'] + '/1/' + response['running_mode'] + '/' 
        //   }
        // } else {
        //   url = "/ARPicture/self_report_" + resultData['page_round'] + "/" + resultData['uaid'] + '/' + resultData['round_num'] + '/'
        // }
        url = "/ARPicture/question_" + resultData['page_round'] + "/" + resultData['uaid'] + '/1/'+ response['running_mode'] + '/'
        window.location.href = url;
      }
    })
  }
  )
  