$('#system_evaluate_button').click(function(){
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    $.ajax({
      url:'/ARPicture/system_evaluate_click/',
      type:'POST',
      data: resultData,
      datatype: 'json',
      success:function (response) {
        console.log(response);
        url = '/ARPicture/experiment_evaluate/' + resultData['uaid'] + '/'
        window.location.href = url;
      }
    })
  }
  )