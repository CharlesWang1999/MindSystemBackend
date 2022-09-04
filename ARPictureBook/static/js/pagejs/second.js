document.addEventListener("DOMContentLoaded", function () {
  const sceneEl = document.querySelector("a-scene");
  // const arSystem = sceneEl.systems["mindar-image-system"];
  sceneEl.addEventListener("arReady", (event) => {
      speckText("小头爸爸和大头儿子发现钓到的时垃圾时，是什么心情？点击按钮帮助大头儿子做出选择");
  });

  scene_1_display();
});

const enumState = {
  SCENE_1_DISPLAY: 0,
  SCENE_1_CORRECT: 1,
  SCENE_1_WRONG: 2,
  SCENE_2_DISPLAY: 3,
  SCENE_2_CORRECT: 4,
  SCENE_2_WRONG: 5,
  SCENE_3_DISPLAY: 6,
  SCENE_3_CORRECT: 7,
  SCENE_3_WRONG: 8,
};

var state = enumState.SCENE_1_DISPLAY;
var topInfo = document.querySelector("#top-info");
var select_1 = document.querySelector("#select-1");
var select_2 = document.querySelector("#select-2");
var select_3 = document.querySelector("#select-3");
var correctInfo = document.querySelector("#correct-info");
var bottomInfo = document.querySelector("#bottom-info");
const correctText = "恭喜!<br/>回答正确"
const wrongText = "回答错误<br/>再接再厉!";

var resultData = {'page_name': 'second'};
var partitionData = {'page_name': 'second'};

function scene_1_display() {
  topInfo.innerHTML =
    "小头爸爸和大头儿子发现钓到的时垃圾时，是什么心情？<br/>点击按钮做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;害怕&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;开心&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;生气&nbsp;&nbsp;&nbsp;&nbsp;";
  correctInfo.innerHTML = "正确答案:";
  bottomInfo.innerHTML = "知道了!";

  correctInfo.style.visibility = "hidden";
  bottomInfo.style.visibility = "hidden";

  select_3.addEventListener("click", scene_1_correct);
  select_2.addEventListener("click", scene_1_wrong);
  select_1.addEventListener("click", scene_1_wrong);
}

function scene_1_correct() {
  state = enumState.SCENE_1_CORRECT;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_1.style.visibility = "hidden";
  select_2.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-success");
  topInfo.innerHTML = correctText;

  resultData['result1'] = 'correct';

  partitionData['question_num'] = 1
  partitionVideo();

  select_3.removeEventListener("click", scene_1_correct);
  select_2.removeEventListener("click", scene_1_wrong);
  select_1.removeEventListener("click", scene_1_wrong);

  bottomInfo.addEventListener("click", scene_2_display);
}

function scene_1_wrong() {
  state = enumState.SCENE_1_WRONG;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_1.style.visibility = "hidden";
  select_2.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-danger");
  topInfo.innerHTML = wrongText;

  resultData['result1'] = 'wrong';

  partitionData['question_num'] = 1
  partitionVideo();

  select_3.removeEventListener("click", scene_1_correct);
  select_2.removeEventListener("click", scene_1_wrong);
  select_1.removeEventListener("click", scene_1_wrong);

  bottomInfo.addEventListener("click", scene_2_display);
}

function scene_2_display() {
  if (state === enumState.SCENE_1_CORRECT) {
    topInfo.classList.replace("btn-success", "btn-primary");
  } else if (state === enumState.SCENE_1_WRONG) {
    topInfo.classList.replace("btn-danger", "btn-primary");
  } else {
    console.log("state error in scene 2 display, current state: " + state);
  }
  state = enumState.SCENE_2_DISPLAY;

  topInfo.innerHTML =
    "动画中小头爸爸和大头儿子为什么会生气呢？<br/>点击按钮帮助大头儿子做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;钓上来的不是大鱼，而是垃圾&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;他们钓的鱼太小了&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;大头儿子掉进水里&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
  correctInfo.innerHTML = "正确答案:";
  bottomInfo.innerHTML = "知道了!";

  select_2.style.visibility = "visible";
  select_1.style.visibility = "visible";
  correctInfo.style.visibility = "hidden";
  bottomInfo.style.visibility = "hidden";

  bottomInfo.removeEventListener("click", scene_2_display);
  select_1.addEventListener("click", scene_2_correct);
  select_2.addEventListener("click", scene_2_wrong);
  select_3.addEventListener("click", scene_2_wrong);
}

function scene_2_correct() {
  state = enumState.SCENE_2_CORRECT;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_2.style.visibility = "hidden";
  select_3.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-success");
  topInfo.innerHTML = correctText;

  resultData['result2'] = 'correct';

  partitionData['question_num'] = 2
  partitionVideo();

  select_1.removeEventListener("click", scene_2_correct);
  select_2.removeEventListener("click", scene_2_wrong);
  select_3.removeEventListener("click", scene_2_wrong);

  bottomInfo.addEventListener("click", scene_3_display);
}

function scene_2_wrong() {
  state = enumState.SCENE_2_WRONG;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_2.style.visibility = "hidden";
  select_3.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-danger");
  topInfo.innerHTML = wrongText;

  resultData['result2'] = 'wrong';

  partitionData['question_num'] = 2
  partitionVideo();

  select_1.removeEventListener("click", scene_2_correct);
  select_2.removeEventListener("click", scene_2_wrong);
  select_3.removeEventListener("click", scene_2_wrong);

  bottomInfo.addEventListener("click", scene_3_display);
}

function scene_3_display() {
  if (state === enumState.SCENE_2_CORRECT) {
    topInfo.classList.replace("btn-success", "btn-primary");
  } else if (state === enumState.SCENE_2_WRONG) {
    topInfo.classList.replace("btn-danger", "btn-primary");
  } else {
    console.log("state error in scene 3 display, current state: " + state);
  }
  state = enumState.SCENE_3_DISPLAY;

  topInfo.innerHTML =
    "小头爸爸和大头儿子钓鱼的时候应该怎么做呢？<br/>点击按钮帮助大头儿子做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;大声说话，走来走去&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;要有耐心，保持安静&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;一边钓鱼，一边玩耍&nbsp;&nbsp;&nbsp;&nbsp;";
  correctInfo.innerHTML = "正确答案:";
  bottomInfo.innerHTML = "知道了!";

  select_2.style.visibility = "visible";
  select_3.style.visibility = "visible";
  correctInfo.style.visibility = "hidden";
  bottomInfo.style.visibility = "hidden";

  bottomInfo.removeEventListener("click", scene_3_display);
  select_2.addEventListener("click", scene_3_correct);
  select_1.addEventListener("click", scene_3_wrong);
  select_3.addEventListener("click", scene_3_wrong);
}

function scene_3_correct() {
  state = enumState.SCENE_3_CORRECT;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_1.style.visibility = "hidden";
  select_3.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-success");
  topInfo.innerHTML = correctText;

  resultData['result3'] = 'correct';

  select_2.removeEventListener("click", scene_3_correct);
  select_1.removeEventListener("click", scene_3_wrong);
  select_3.removeEventListener("click", scene_3_wrong);

  bottomInfo.addEventListener("click", jumpToNext);
}

function scene_3_wrong() {
  state = enumState.SCENE_3_WRONG;
  correctInfo.style.visibility = "visible";
  bottomInfo.style.visibility = "visible";
  select_1.style.visibility = "hidden";
  select_3.style.visibility = "hidden";

  topInfo.classList.replace("btn-primary", "btn-danger");
  topInfo.innerHTML = wrongText;

  resultData['result3'] = 'wrong';

  select_2.removeEventListener("click", scene_3_correct);
  select_1.removeEventListener("click", scene_3_wrong);
  select_3.removeEventListener("click", scene_3_wrong);

  bottomInfo.addEventListener("click", jumpToNext);
}

function jumpToNext() {
  var currentHref = window.location.href;
  let p=currentHref.split('?')[1]
  let params=new URLSearchParams(p)
  const resultId = params.get('id');
  if (resultId){
    resultData['result_id'] = resultId;
  }
  $.ajax({
    url: '/ARPicture/get_query_result/',
    type: 'POST',
    data: resultData,
    datatype: 'json',
    success: function(response){
      console.log(response);
      if (response['status'] == 'error'){
        alert("error!", response['errormessage']);
        return;
      }
      alert('success, click to next page...');
      url = "/ARPicture/third/"
      if (response['result_id']) {
        url += '?id=' + response['result_id']
      }
      window.location.href = url;
    }
  })
}

var synth = window.speechSynthesis;
var utterance = new SpeechSynthesisUtterance();
utterance.lang = "zh-CN";
utterance.rate = 0.85;

function speckText(str) {
  utterance.text = str;
  synth.speak(utterance);
}

//syj worte
function partitionVideo(){
  console.log("开始调用py")
  var currentHref = window.location.href;
  let p=currentHref.split('?')[1]
  let params=new URLSearchParams(p)
  const resultId = params.get('id');
  if (resultId){
    partitionData['result_id'] = resultId;
  }
  $.ajax({
    url:'/ARPicture/get_web_click/',
    type:'POST',
    data: partitionData,
    datatype: 'json',
    success:function (response) {
      console.log(response);
    }
  })
}