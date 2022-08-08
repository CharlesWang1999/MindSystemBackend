document.addEventListener("DOMContentLoaded", function () {
  const sceneEl = document.querySelector("a-scene");
  // const arSystem = sceneEl.systems["mindar-image-system"];
  sceneEl.addEventListener("arReady", (event) => {
      speckText("小头爸爸和大头儿子被剔了理发光头，是什么心情？点击按钮帮助大头儿子做出选择");
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

function scene_1_display() {
  topInfo.innerHTML =
    "小头爸爸和大头儿子理发被剔了光头，是什么心情？<br/>点击按钮做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;害怕&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;开心&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;惊讶&nbsp;&nbsp;&nbsp;&nbsp;";
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
    "动画中围裙妈妈因为大头儿子小头爸爸无法参加宴会，表现了什么心情？<br/>点击按钮帮助大头儿子做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;生气&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;开心&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;害怕&nbsp;&nbsp;&nbsp;&nbsp;";
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
    "小头爸爸和大头儿子长出新头发，心情是怎么样的<br/>点击按钮帮助大头儿子做出选择";
  select_1.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;难过&nbsp;&nbsp;&nbsp;&nbsp;";
  select_2.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;高兴&nbsp;&nbsp;&nbsp;&nbsp;";
  select_3.innerHTML =
    "&nbsp;&nbsp;&nbsp;&nbsp;害怕&nbsp;&nbsp;&nbsp;&nbsp;";
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

  select_2.removeEventListener("click", scene_3_correct);
  select_1.removeEventListener("click", scene_3_wrong);
  select_3.removeEventListener("click", scene_3_wrong);

  bottomInfo.addEventListener("click", jumpToNext);
}

function jumpToNext() {
  window.location.href = "/ARPicture/fourth";
}

var synth = window.speechSynthesis;
var utterance = new SpeechSynthesisUtterance();
utterance.lang = "zh-CN";
utterance.rate = 0.85;

function speckText(str) {
  utterance.text = str;
  synth.speak(utterance);
}
