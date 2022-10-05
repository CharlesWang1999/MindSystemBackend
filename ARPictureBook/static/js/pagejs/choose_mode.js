$("#choose_mode_submit").click(
	function() {
			console.log($("#choose_mode_form").serialize())
			$.ajax({
				url: "/ARPicture/choose_mode_submit/",
				type: "POST",
				data: $("#choose_mode_form").serialize(),
				success:function(context){
					// alert(context['status'], context['answer_id'], context['next_page']);
					console.log(context['status'], context['uaid'] , context['mode'])
					url = "/ARPicture/question_s1/" + context['uaid'] + '/1/' +context['mode']
        	window.location.href = url;
				}
			})
	}
)