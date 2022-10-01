$('#experiment_evaluate_button').click(function(){
    var resultData = {}
    resultData['uaid'] = $("#uaid").text();
    $.ajax({
      url:'/ARPicture/experiment_evaluate_click/',
      type:'POST',
      data: resultData,
      datatype: 'json',
      success:function (response) {
        console.log(response);
        url = '/ARPicture/finish/' + resultData['uaid'] + '/'
        window.location.href = url;
      }
    })
  }
  )