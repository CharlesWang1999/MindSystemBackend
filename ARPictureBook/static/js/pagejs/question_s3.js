$('#imitation_button').click(function () {
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    resultData['round_num'] = $("#round_num").text();
    $.ajax({
      url: '/ARPicture/imitation_finish/',
      type: 'POST',
      data: resultData,
      datatype: 'json',
      success: function (response) {
        console.log(response);
        $('#imitation_button').css('display', 'none');
        $('#question_container').attr('style', '');
    //     $('.box_right').empty();
    //     $('.box_right').html(
    //    ' <form id="question_form">'+
    //     '<div class="question_title">'+
    //         '<span class="badge rounded-pill bg-primary">单选题</span>'+
    //         '<div class="fs-2 fw-bold lh-base question_text">根据大屏幕中视频及文字或AR模型，选择对应的情绪</div>'+
    //     '</div>'+
    //     '<ul start="" class="question_option" name="single">'+
    //         '<li class="answer">'+
    //             '<input id="emotion_a"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="A"/>'+
    //             '<label for="emotion_a" class="btn btn-outline-primary btn-lg answer-label">A. 快乐</label>'+
    //         '</li>'+
    //         '<li class="answer">'+
    //             '<input id="emotion_b"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="B"/>'+
    //             '<label for="emotion_b" class="btn btn-outline-primary btn-lg answer-label">B. 悲伤</label>'+
    //         '</li>'+
    //         '<li class="answer">'+
    //             '<input id="emotion_c"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="C"/>'+
    //             '<label for="emotion_c" class="btn btn-outline-primary btn-lg answer-label">C. 愤怒</label>'+
    //         '</li>'+
    //         '<li class="answer">'+
    //             '<input id="emotion_d"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="D"/>'+
    //             '<label for="emotion_d" class="btn btn-outline-primary btn-lg answer-label">D. 恐惧</label>'+
    //         '</li>'+
    //         '<li class="answer">'+
    //             '<input id="emotion_e"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="E"/>'+
    //             '<label for="emotion_e" class="btn btn-outline-primary btn-lg answer-label">E. 厌恶</label>'+
    //         '</li>'+
    //         '<li class="answer">'+
    //             '<input id="emotion_f"'+
    //                     'class="btn-check"'+
    //                     'type="radio"'+
    //                     'name="place1"'+
    //                     'value="F"/>'+
    //             '<label for="emotion_f" class="btn btn-outline-primary btn-lg answer-label">F. 惊奇</label>'+
    //         '</li>'+
    //     '</ul>'+
    // '</form> ' +
    // '<button type="button" id="question_button" class="btn btn-primary btn-lg">确定提交</button>'
    // )
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
        // window.location.href = url;
      }
    })
  }
  )