---
title: Tingle Gesture Detection Pilot Study App
subtitle: coordinator
layout: none
modal-id: tingle-min
categories: [webapp]
date: 2018-03-05
created-by: [curt-white, jon-clucas]
updated:
  latest:
    by: [jon-clucas]
    date: 2018-03-05
permalink: tingle/tingle-min.html
people: [curt-white, jon-clucas]
projects: [tingle]
glyph: wearable.png
---
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">

    <title>Tingle Gesture Detection Pilot Study App</title>

    <link type="text/css" rel="stylesheet" href="../css/web-bluetooth.css">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <!-- library for realtime streaming data visualization -->
    <script type="text/javascript" src="../js/smoothie.js"></script>

     <!-- get data from device -->
    <script type="text/javascript" src="../js/sensor-web-bluetooth.js"></script>

    <!-- primary app code get web bluetooth data, collect data from model, apply to neural network -->
    <!-- ahoy, there be global vars and magic numbers galore -->
    <script type="text/javascript" src="../js/app-web-bluetooth.js"></script>

    <!-- joystick and distance sensor jig -->
  <!--  <script type="text/javascript" src="js/gamepad.js"></script> -->
  <!--  <script type="text/javascript" src="js/gamepad_visualizer.js"></script> -->
  <script src="https://www.gstatic.com/firebasejs/4.8.2/firebase-app.js"></script>
  <script src="https://www.gstatic.com/firebasejs/4.8.2/firebase-auth.js"></script>
  <script src="https://www.gstatic.com/firebasejs/4.8.2/firebase-database.js"></script>
  <script src="https://www.gstatic.com/firebasejs/4.8.2/firebase-messaging.js"></script>
	<script>
	  // Initialize Firebase
	  var config = {
	    apiKey: "AIzaSyAnyxeXYyH1t5La_qOE0u_TqXY8XFiGpFk",
	    authDomain: "tingle-pilot-collected-data.firebaseapp.com",
	    databaseURL: "https://tingle-pilot-collected-data.firebaseio.com",
	    projectId: "tingle-pilot-collected-data",
	    storageBucket: "tingle-pilot-collected-data.appspot.com",
	    messagingSenderId: "1009948604228"
	  };
	  firebase.initializeApp(config);
	</script>

    <style>
    @import url(https://fonts.googleapis.com/css?family=Noto+Sans);
  	* {
  	   font-family: 'Noto Sans', Arial;
  	}
    body{
      background-color: black;
    }
    #interface-controls{
      width: 38%;
      margin-top: 5px;
      display:inline-block;
     /* height: 400px; */
    }
    /*.master-pose-ui{
      display: inline-block;
      margin-top: 15px;
      margin-bottom: 15px;
    }*/
      #btnOne{
        z-index: 99;
        margin-top: 60px;
      }

      .range-slider {
        z-index: 99;
      margin: 18px 0 0 0;
    }

    .range-slider {
      width: 100%;
    }
    .sample-size-div{
      width: 260px;
      display: inline-block;
      margin-top: 0px;
    }
    .sample-size-div .range-slider__value{
      width: 18px;
    }
    .sample-size-div p.range-label{
      text-align: center;
    }
    .range-slider__value.master-pose{
      background-color: gray;
    }

    .range-slider p{
      margin: 0px;
      margin-bottom: -8px;
    }

    p.range-label{
      color: white;
      margin-bottom: -10px;
      font-size: 11px;
    }

    .range-slider__range {
      -webkit-appearance: none;
      width: calc(100% - (65px));
      height: 5px;
      border-radius: 5px;
      background: #d7dcdf;
      outline: none;
      padding: 0;
      margin: 0;
    }
    .range-slider__range.nn-architecture {
	    width: calc(100% - (110px));
	}

    .range-slider__range::-webkit-slider-thumb {
      -webkit-appearance: none;
              appearance: none;
  /*    width: 20px;
      height: 20px;   */
      width: 15px;
      height: 15px;
      border-radius: 50%;
  /*    background: #2c3e50;   */
      background: #dbca60;
      cursor: pointer;
      -webkit-transition: background .15s ease-in-out;
      transition: background .15s ease-in-out;
    }
    .range-slider__range.transform {  /* these sliders no longer important so make smaller */
      height: 5px;
    }
    .range-slider__range.transform::-webkit-slider-thumb {  /* these sliders no longer important so make smaller */
            width: 15px;
      height: 15px;
    }
    .range-slider__range::-webkit-slider-thumb:hover {
      background: #1abc9c;
    }
    .range-slider__range:active::-webkit-slider-thumb {
      background: #1abc9c;
    }
    .range-slider__range::-moz-range-thumb {
      width: 20px;
      height: 20px;
      border: 0;
      border-radius: 50%;
      background: #2c3e50;
      cursor: pointer;
      -webkit-transition: background .15s ease-in-out;
      transition: background .15s ease-in-out;
    }
    .range-slider__range::-moz-range-thumb:hover {
      background: #1abc9c;
    }
    .range-slider__range:active::-moz-range-thumb {
      background: #1abc9c;

    }

    .range-slider__value {
      display: inline-block;
      position: relative;
      font-size: 14px;
      color: #fff;
      line-height: 20px;
      text-align: center;
      border-radius: 3px;
      background: #d2691e;
      padding: 5px 12px;
      margin-left: 8px;
    }
    .range-slider__value:after {
      position: absolute;
      top: 8px;
      left: -7px;
      width: 0;
      height: 0;
      border-top: 7px solid transparent;
      border-right: 7px solid #d9b32a;
      border-bottom: 7px solid transparent;
      content: '';
    }

    ::-moz-range-track {
      background: #d7dcdf;
      border: 0;
    }

    input::-moz-focus-inner,
    input::-moz-focus-outer {
      border: 0;
    }

    .range-slider label {
        position: absolute;
        width: 20px;
        margin-left: 5px;
        margin-right: 5px;
        text-align: center;
        margin-top: 0px;
        color: white;
        font-size: 12px;
    }

    .sensor-data .data{
      color: white;
      width: 80px;
      display: inline-block;
      overflow: hidden;
      font-size: 12px;
    }
    .sensor-container{
      margin-top: 5px;
      height: 100px;
      margin-bottom: 15px;
    }


    .btn {
      padding: 0px;
        display: inline-block;
        padding: 4px 8px;
        margin-bottom: 0;
        font-size: 14px;
        font-weight: 500;
        line-height: 1.3;
        text-align: center;
        white-space: nowrap;
        vertical-align: middle;
        cursor: pointer;
        border: 1px solid transparent;
        border-radius: 4px;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        -o-user-select: none;
        user-select: none;
    }

    .collect.btn , #connect.btn, #print-btn.btn, #load-btn.btn, #train-btn.btn, #activate-btn, #export-btn, #train2-btn.btn, #activate2-btn, #export2-btn, #load-nn-btn{
        color: #fff;
        background-color: #3bafda;
        border-color: #3bafda;
        margin-right: 10px;
        margin-bottom: 10px;
        margin-top: 6px;
        width: 85px;
    }
    #activate-btn, #export-btn, #activate2-btn, #export2-btn{
      background-color: #6d6d6d;
      border-color: #6d6d6d;
      width: 125px;
    }
    #activate-btn.haveNN, #export-btn.haveNN, #activate2-btn.haveNN, #export2-btn.haveNN{
      background-color: green;
      border-color: green;
    }
    #activate-btn.activeNN, #activate2-btn.activeNN, #load-nn-btn.activeNN, #load-nn-btn.activatedNN{
      background-color: red;
      border-color: red;
    }

    #load-nn-btn.btn, #load-btn.btn, #print-btn.btn{
    	width: 112px;
    }

    /*   firebase  */
    form {
      margin-top: 30px;
    }
    form div{
      display: inline-block;
      margin-right: 3px;
    }
    form div input{
      width: 80px;
    }
    form .label{
      color: white;
      font-style: bold;
      font-weight: 600;
    }
    form .btn, button#back-pose, button#forward-pose, button#go-pose{
      color: #fff;
        background-color: #d9b32a;
        border-color: #d9b32a;
        margin-right: 5px;
        width: 80px;
        font-size: 14px;
        font-weight: 600;
        padding: 0px 0px;
    }
    #container{
    }
    #console{
    	width: 100%;
        padding-top: 4px;
        padding-bottom: 4px;
      	display: inline-block;
      	margin-top:0px; margin-bottom: 0px;
      	font-size: 14px;
      	color:white;
    }
    .console span{
      	color: yellow;
    }


    #basic-interface-container{
    	width: 100%;
    	display: inline-block;
    }
    .intro{
      margin-left: 0px;
      margin-bottom: 0px;
      width: 400px;
    }

.circle-button {
  position: absolute;
  top: 1.5em;
  right: 1.5em;
  width: 40px;
  height: 40px;
  font-size: 1.5em;
  color: #fff;
  background: #fff;
  border: none;
  border-radius: 50%;
  -webkit-box-shadow: 0 3px 6px rgba(200, 200, 200, 0.275);
          box-shadow: 0 3px 6px rgba(200, 200, 200, 0.275);
  outline: none;
  cursor: pointer;
  -webkit-transition: all 300ms ease;
  transition: all 300ms ease;
}
.circle-button .close {
  -webkit-transition: -webkit-transform 400ms ease;
  transition: -webkit-transform 400ms ease;
  transition: transform 400ms ease;
  transition: transform 400ms ease, -webkit-transform 400ms ease;
}
.circle-button:hover {
  -webkit-box-shadow: 0 6px 12px rgba(200, 200, 200, 0.975);
          box-shadow: 0 6px 12px rgba(200, 200, 200, 0.975);
}

.closeRotate {
  -webkit-transform: rotate(45deg);
          transform: rotate(45deg);
}
#data-message{
  width: 100%;
  display: block;
  color: white;
  font-size: 0.95em;
}
.data-message-value{
  color: yellow;
}
.message-nn1-score, .message-nn2-score{
  font-size: 1.4em;
  font-weight: 600;
}
.message-nn1-score{
  color: rgb(72, 244, 68);
}
.message-nn2-score{
  color: rgb(244, 66, 66);
}

.collect.btn{
  width: 118px;
  margin-left: 0px;
  margin-right: 6px;
}
.collect.btn.true{
 background-color: #00cc66;
 border-color: #00cc66;
}
.collect.btn.false{
 background-color: #ff6666;
 border-color: #ff6666;
}

.clear.btn{
  background-color: #8600b3;
  color: white;
  padding: 4px 7px;
}
.btn.clear.true{
	margin-right: 5px;
}
#nn-slide-controls{
  width: 100%;
  margin-top: 40px;
}
.nn-architecture-div{
  display: inline-block;
  width: 60%;
  padding-right: 15px;
  padding-left: 5px;
  margin-bottom: 10px;
  position: relative;
  margin-top: 5px;
}
.range-slider.nn-architecture p.range-label{
  margin-bottom: -5px;
  font-size: 16px;
}
.range-slider.nn-architecture label {
  margin-top: 25px;
  font-size: 14px;
}
input[type="range" i] {

}
input[type="text"]:-ms-input-placeholder {
  color: #aaa;
  font-weight: 300;
}

.g {
    opacity: 1;
}
.clean-slide {
  display: inline-block;
  width: 100px;
  padding: 5px 0 5px 25px;
  margin-left: 40px;
  font-family: "Open Sans", sans;
  font-weight: 400;
  font-size: 16px;
  color: #377D6A;
  background: #efefef;
  border: 0;
  border-radius: 5px;
  outline: 0;
  transition: all .3s ease-in-out;
}
#rate-input{
	padding-left: 20px;
	width: 35px;
}
#iterations-input{
	padding-left: 65px;
	width: 38px;
}
#error-input{
	padding-left: 30px;
	width: 35px;
}
#error-input{
  padding-left: 30px;
  width: 35px;
}
#file-name-input{
  padding-left: 50px;
  width: 90px;
}
.clean-slide + label {
  display: inline-block;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  padding: 5px 10px;
  font-size: 14px;
  line-height: 17px;
  text-shadow: 0 1px 0 rgba(19, 74, 70, 0.4);
  background: #3bafda;
  color: white;
  transition: all .3s ease-in-out;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
}

.clean-slide:focus,
.clean-slide:active {
  color: #377D6A;
  background: #fff;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.clean-slide:focus + label,
.clean-slide:active + label {
  transform: translateX(-10%);
}
span.text-input-span {
    position: relative;
    display: inline-block;
    margin-right: 6px;
}

#record-buttons-container{
    width: 150px;
    height: 45px;
    padding-right: 8px;
    padding-top: 15px;
    display: inline-block;
}

#record-btn, #pause-btn{
    width: 50px;
    height: 50px;
    padding: 0px;
    margin: 3px;
    background: transparent;
    background-repeat: no-repeat;
    background-size: cover;
    outline: none !important;
}
#record-btn.active-data-ui{
    background-image: url("images/record_button.png");
}
#pause-btn.active-data-ui{
    background-image: url("images/pause_button.png");
}
#record-btn{
    background-image: url("images/record_button_gray.png");
}
#pause-btn{
    background-image: url("images/pause_button_gray.png");
}

.external-config-btn{
    color: #fff;
    width: 175px;
    background-color: #3bafda;
    border-color: #3bafda;
    margin-bottom: 6px;
}

#hand-head-ui-container{
    width: 100%;
    left: 70px;
    display: inline-block;
    position: relative;
}
div.hand-face-ui{
    display: inline-block;
    position: relative;
}
#hand-head-ui-container .hand-face-img.left-hand-back, #hand-head-ui-container .hand-face-img.right-hand-back{
  display: none;
}
img.hand-face-img{
}

#hand-container{
	margin-left: 3px;
}
#front-head, #side-head{
	margin-left: 25px;
}
#hand-container, #hand-container img, #hand-display{
	width: 140px;
	height: 140px;
}
#front-head, #front-head img, #side-head, #side-head img, #front-head-display, #side-head-display{
	width: 200px;
	height: 200px;
}

#hand-display{
	background-repeat: no-repeat;
    background-size: cover;
    position: absolute;
    top: 0;
}



#side-head.active-hand{
	-moz-transform: scaleX(-1);
    -o-transform: scaleX(-1);
    -webkit-transform: scaleX(-1);
    transform: scaleX(-1);
    filter: FlipH;
    -ms-filter: "FlipH";
}
#hand-head-button-container{
  width: 100%;
  margin-right: 160px;
  display: inline-block;
  float: left;
}
#hand-head-button-container .btn.hand-head-button, #stepwise-ui-container .script-step{
  width: 150px;
  height: 50px;
  color: #fff;
  border: 1px solid;
  border-radius: 5px;
  padding-left: 12px; padding-right: 8px;
  padding-top: 8px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.1;
  text-align: left;
  background-color: #3bafda;
  border-color: #3bafda;
  margin-right: 10px;
}
#hand-head-button-container #hand-btn{
  background-repeat: no-repeat;
  background-position: bottom 50% right 10%;
  background-size: 90% auto;
}
#stepwise-ui-container{
  display: inline-block;
  position: relative;
  width: 90%;
  max-width: 600px;
  height: 120px;
  margin-top: 25px;
}
#stepwise-ui-container .script-step, #stepwise-ui-container #last-label, #stepwise-ui-container #next-label{
  width: 86%;
  height: 105px;
  display: inline-block;
  position:absolute;
  color: white;
}
#script-last-step{
	left: 0px;
}
#script-this-step{
	left: 5%;
}
#script-next-step{
	right: 0px;
	margin-right: 0px;
}
#last-label{
	left: 0px;
}
#next-label{
	right: 0px;
	margin-right: 15px;
}
#stepwise-ui-container #last-label, #stepwise-ui-container #next-label{
	top: 75px;
	text-align: center;
    height: 20px;
    width: 25%;
    z-index: 3;
    opacity: 0.8;
}

#stepwise-ui-container .script-step-hint{
  width: 24%;
  height: 90px;
  top: 5px;
  background-color: gray;
  color: white;
  border-color: gray;
  border-radius: 0px;
  opacity: 0.7;
  margin-bottom: 10px;
  padding: 5px 10px;
  text-align: center;
  font-size: 12px;
}

#stepwise-ui-container #script-this-step #script-this-step-toggle{
  position: absolute;
  bottom: 3px;
  background: transparent;
  font-size: 20px;
  font-weight: 600;
  line-height: 45px;
  margin-left: 55px;
}
#stepwise-ui-container #script-this-step #script-this-step-num{
  position: absolute;
  bottom: 3px;
  background: transparent;
  font-size: 12px;
  right: 10px;
}

#stepwise-ui-container #script-this-step{
  color: white;
  text-align: center;
  border-color: #ff6666;
  background-color: #ff6666;
  margin-bottom: 10px;
  padding: 5px 10px;
}
#stepwise-ui-container #script-this-step #this-step-text{
	height: 30px;
}
#stepwise-ui-container #script-this-step:hover{
  border-color: rgb(244, 66, 66);
  background-color: rgb(244, 66, 66);
}
#stepwise-ui-container #script-this-step.on-target{
  border-color: #00cc66;
  background-color: #00cc66;
}
#hand-head-button-container #hand-btn.left-active{
  background-image: url("images/hand-left-button.png");
}
#hand-head-button-container #hand-btn.right-active{
  background-image: url("images/hand-right-button.png");
}
#hand-head-button-container #hand-btn.left-active:hover{

}
#hand-head-button-container #hand-btn.right-active:hover{

}
#hand-head-button-container #selected-targets{
  height: 35px;
  color: yellow;
  padding: 5px 0px;
  margin-top: 10px;
  font-size: 18px;
}
.head-arrow img, .head-arrow, .script-arrow img, .script-arrow{
  width: 50px;
  height: 50px;
}
#stepwise-ui-container .script-arrow{
  position: absolute;
  top: 30px;
  background-repeat: no-repeat;
  background-size: cover;
}

#head-ui-container .head-arrow{
  position: absolute;
  top: 75px;
  background-repeat: no-repeat;
  background-size: cover;
}
#head-ui-container .head-arrow img:hover, #stepwise-ui-container .script-arrow img:hover{
  opacity: 0.1;
}
#head-ui-container #head-rotate-left, #stepwise-ui-container #script-rotate-left{
  left: -60px;
  background-image: url("images/left-arrow-dark.png");
}
#head-ui-container #head-rotate-right, #stepwise-ui-container #script-rotate-right{
  right: -60px;
  background-image: url("images/right-arrow-dark.png");
}
#head-ui-container #head-image-container img.head-image{
  display: none;
}

#head-ui-container #head-image-container.front-active img.front-image,
#head-ui-container #head-image-container.left-active img.left-image,
#head-ui-container #head-image-container.right-active img.right-image,
#head-ui-container #head-image-container.back-active img.back-image{
  display: block;
}

#head-ui-container .target-selector{
  position: absolute;
}
#target-hover-label{
  position: absolute;
  color: white;
  top: 101%;
  left: 40%;
  font-size: 14px;
}

#head-ui-container .target-selector img.yellow-circle,
#head-ui-container .target-selector img.green-circle{
  width: 30px;
  height: 30px;
  opacity: 0.5;
}
#head-ui-container .target-selector .yellow-circle:hover,
#head-ui-container .target-selector .green-circle:hover{
  opacity: 0.9;
}

#head-ui-container .target-selector img.green-circle{
  display: none;
}
#head-ui-container .target-selector.target-active img.green-circle{
  display: block;
}
#head-ui-container .target-selector.target-active img.yellow-circle{
  display: none;
}


.front-active #mouth-target, .front-active #front-target, .front-active #top-target{
  left: 44%;
}
.front-active #mouth-target{
  top: 72%;
}
.front-active #front-target{
  top: 30%;
}
.front-active #top-target{
  top: 5%;
}
.front-active #back-target{
  display: none;
}
.front-active #right-target, .front-active #left-target{
  top: 35%;
}
.front-active #right-target{
  left: 7%;
}
.front-active #left-target{
  left: 76%;
}

.back-active #back-target, .back-active #top-target{
  left: 44%;
}
.back-active #mouth-target, .back-active #front-target{
  display: none;
}
.back-active #top-target{
  top: 5%;
}
.back-active #back-target{
  top: 30%;
}
.back-active #right-target, .back-active #left-target{
  top: 32%;
}
.back-active #right-target{
  left: 77%;
}
.back-active #left-target{
  left: 5%;
}


.left-active #right-target{
  display: none;
}
.left-active #top-target{
  top: 2%;
}
.left-active #left-target, .left-active #front-target, .left-active #back-target{
  top: 27%;
}
.left-active #mouth-target{
  top: 78%;
}
.left-active #front-target{
  left: 5%;
}
.left-active #mouth-target{
  left: 15%;
}
.left-active #left-target, .left-active #top-target{
  left: 40%;
}
.left-active #back-target{
  left: 77%;
}

.right-active #left-target{
  display: none;
}
.right-active #top-target{
  top: 2%;
}
.right-active #right-target, .right-active #front-target, .right-active #back-target{
  top: 27%;
}
.right-active #mouth-target{
  top: 78%;
}
.right-active #front-target{
  right: 5%;
}
.right-active #mouth-target{
  right: 15%;
}
.right-active #right-target, .right-active #top-target{
  right: 40%;
}
.right-active #back-target{
  right: 77%;
}

/***************** PILOT TARGET STYLES *******************/
.disable-right .right-side, .disable-left .left-side{
	display: none;

}
.front-active #back-target, .back-active #back-target, .right-active #back-target, .left-active #back-target,
.front-active #front-target, .back-active #front-target, .right-active #front-target, .left-active #front-target,
.front-active #top-target, .back-active #top-target, .right-active #top-target, .left-active #top-target{
	display: none;
}

.front-active #eyebrow-left-target{
  	top: 37%;
  	right: 25%;
}
.front-active #eyebrow-right-target{
    top: 39%;
    left: 27%;
}
.front-active #nose-left-target{
  	top: 56%;
  	right: 36%;
}
.front-active #nose-right-target{
  	top: 56%;
  	left: 36%;
}
.front-active #cheek-left-target{
    top: 68%;
    right: 22%;
}
.front-active #cheek-right-target{
    top: 68%;
    left: 24%;
}
.front-active #back-left-target, .front-active #back-right-target{
  display: none;
}

.back-active #back-left-target{
	top: 40%;
    left: 22%;
}
.back-active #back-right-target{
	top: 40%;
    right: 22%;
}
.back-active #eyebrow-left-target, .back-active #eyebrow-right-target, .back-active #nose-left-target, .back-active #nose-right-target, .back-active #cheek-left-target, .back-active #cheek-right-target, .back-active #right-target, .back-active #left-target{
  	display: none;
}


.left-active  #back-left-target{
	top: 40%;
    right: 22%;
}
.left-active #left-target{
	top: 27%;
  right: 40%;
}
.left-active #eyebrow-left-target{
    top: 46%;
    right: 76%;
}
.left-active #nose-left-target{
    top: 64%;
    right: 75%;
}
.left-active #cheek-left-target{
	top: 68%;
    right: 58%;
}
.left-active #cheek-right-target{
  display:none;
}
.left-active .right-side{
	display: none;
}

.right-active  #back-right-target{
	top: 40%;
  left: 22%;
}
.right-active #right-target{
	top: 27%;
  	right: 40%;
}
.right-active #eyebrow-right-target{
    top: 46%;
    left: 76%;
}
.right-active #nose-right-target{
    top: 64%;
    left: 75%;
}
.right-active #cheek-right-target{
	top: 68%;
    left: 58%;
}
.right-active #cheek-left-target{
  display:none;
}
.right-active .left-side{
	display: none;
}



#dump-print{
  background-color: white;
  width: 100%;
  height: auto;
  display: none;
}
#dump-print.active-print{
  display: block;
}


    body .btn:hover, button.btn:hover  {
        border-color: white !important;
        border: 1px solid !important;
    }
    .hide-for-chart{
    	display: none !important;
    }

.object-temp-1-key{ background-color: rgb(133, 87, 35); }
.object-temp-2-key{ background-color: rgb(185, 156, 107); }
.object-temp-3-key{ background-color: rgb(143, 59, 27); }
.object-temp-4-key{ background-color: rgb(213, 117, 0); }
.proximity-key{ background-color: rgb(128, 128, 255); }
.pitch-key{ background-color: rgb(128, 128, 128); }
.roll-key{ background-color: rgb(240, 240, 240); }
.nn1-score-label{ color: rgb(72, 244, 68); font-weight: 600; }
.nn2-score-label{ color: rgb(244, 66, 66); font-weight: 600; }

@media (max-width: 1185px) {
  #hand-head-button-container {
    width: 250px;
    margin-right: 60px;
  }
  #hand-head-ui-container {
    width: 60%;
    float: none;
    margin-top: 15px;
  }
}

#device-configuration-container{
	display: inline-block;
}
#script-clock{
	position: absolute;
    top: 5px;
    left: 5px;
    font-size: 1.5rem;
    font-style: normal;
}
#notes{
	position:relative;
	width: 100%;
}
#notes textarea {
    padding: 8px 10px;
    width: 47%;
    color: #444444;
    font-size: 12px;
    margin: 5px 2px;
    background-color: #fdfdfd;
    border: 1px solid #c2c2c2;
}

#notes textarea:hover {
    border: 1px solid #a2a2a2;
    outline: none;

    box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
    -moz-box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
    -webkit-box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
}

#notes textarea:focus {
    border: 1px solid #e7e7e7;
    outline: none;

    box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
    -moz-box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
    -webkit-box-shadow: -1px 1px 2px rgba(0,0,0,.1) inset;
}
#submit-notes-btn{
    position: absolute;
    left: 5px;
    margin-top: 40px;
}
  </style>


  </head>


  <body>



<!-- DISPLAY WEB BLUETOOTH DATA -->
    <div class="sensor-container">
<!-- display raw numerical data -->
      <div class="sensor-data">
          <div class="data"><span class="object-temp-1-key key">&nbsp;&nbsp;&nbsp;</span>OT1: <span class="object-temp-1-data"></span></div>
          <div class="data"><span class="object-temp-2-key key">&nbsp;&nbsp;&nbsp;</span>OT2: <span class="object-temp-2-data"></span></div>
          <div class="data"><span class="object-temp-3-key key">&nbsp;&nbsp;&nbsp;</span>OT3: <span class="object-temp-3-data"></span></div>
          <div class="data"><span class="object-temp-4-key key">&nbsp;&nbsp;&nbsp;</span>OT4: <span class="object-temp-4-data"></span></div>

          <div class="data"><span class="proximity-key key">&nbsp;&nbsp;&nbsp;</span>Prox: <span class="proximity-data"></span></div>

          <div class="data"><span class="pitch-key key">&nbsp;&nbsp;&nbsp;</span>Pitch: <span class="accelerometer-pitch-data"></span></div>
          <div class="data"><span class="roll-key key">&nbsp;&nbsp;&nbsp;</span>Roll: <span class="accelerometer-roll-data"></span></div>
          <div class="data">accX: <span class="accelerometer-x-data"></span></div>
          <div class="data">accY: <span class="accelerometer-y-data"></span></div>
          <div class="data">accZ: <span class="accelerometer-z-data"></span></div>

          <div class="data">ATav: <span class="ambient-temp-average-data"></span></div>

          <div class="data">Battery: <span class="battery-data"></span></div>
      </div>

<!-- container for smoothie.js timeseries streaming data chart (canvas) -->
      <div id="streaming-data-chart" class="smoothie-container"></div>

<!-- min/max streaming data chart -->
       <div class="circle-button" id="circleDrop"><img id="chart-size-button" class="close" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/324479/close.svg"/></div>

    </div>

	<!-- info about collected sensor data samples -->
    <div id="console" class="console"></div>

    <div id="basic-interface-container">
	    <div class="intro">
	        <button id="connect" class="btn">Connect</button>

	        <div id="device-configuration-container">
	          <button id="sign-in-button" class="btn external-config-btn mdl-button--raised mdl-button mdl-js-button mdl-js-ripple-effect"><i class="material-icons">
                Sign in with Google</i>
                </button>
	        </div>
	    </div>
	</div>

	<div id="hand-head-button-container">
        <div id="selected-targets">Target: none</div>
        <div id="hand-btn" class="hand-head-button btn left-active"><br/>Toggle Hand</div>
        <div id="record-buttons-container">
            <button id="record-btn" class="btn active-data-ui"></button>
            <button id="pause-btn" class="btn"></button>
        </div>
	</div>

	<div id="hand-head-ui-container">
      <div id="stepwise-ui-container">
          <div id="script-rotate-left" class="script-arrow"><img src="images/left-arrow.png" alt="arrow" ></div>
    <!--      <div id="script-last-step" class="script-step script-step-hint">Last Step Lorem ipsum dolor</div>
          <div id="last-label">LAST</div>
          <div id="next-label">NEXT</div> -->
          <div id="script-this-step" class="script-step" ><div id="this-step-text">This Step Lorem ipsum dolor</div>
          	  <div id="script-clock"></div>
              <div id="script-this-step-toggle">OFF TARGET</div>
              <div id="script-this-step-num"></div>
          </div>
        <!--  <div id="script-next-step" class="script-step script-step-hint">Next Step Lorem ipsum dolor</div> -->
          <div id="script-rotate-right" class="script-arrow"><img src="images/right-arrow.png" alt="arrow" ></div>
      </div>
	</div>


	<div id="notes">
		<textarea id="submit-notes-text" cols="30" rows="3" placeholder="Enter Notes Here...."></textarea>
		<button id="submit-notes-btn" class="btn">Submit Notes</button>
	</div>


  <div id="hidden-serial-bluetooth" style="display:none !important">
          <div id="connected-devices-header">
              <div style="float:left;">
                <h2>Connected devices</h2>
              </div>
              <div style="float:right;">
                <p style="margin-top:20px;">Mode: <select id="mode">
                    <option value="console">Console (Command all)</option>
                  </select></p>
              </div>
              <div class="clear"></div>
      </div>
      <div id="mqtt-announced-banner" class="hidden">
        <i style="margin-right:20px;" class="fa fa-exclamation-triangle"></i> MQTT topics published and subscribed to will be advertised here <span id="warn-announced">/wmq/playing</span>. Could be fun, but use "unannounced" mode if not desired.
      </div>  
      <div id="mqtt-section" class="hidden">
        <div>MQTT Broker : iot.eclipse.org</div>
      </div>
      <div id="connected-devices">
        <div>
            <table id="device-listing">
              <tr><th>Device</th><th class="mqtt hidden">Publishing on</th><th class="mqtt hidden">Subscribed to</th><th class="relay">Master</th><th class="relay">Slave</th><th class="console hidden">Console</th><th>&nbsp;</th></tr>
            </table>  
        </div>
      </div>
    </div>

  </body>


<script>
    //global sensor data object
    var state = {};
    //global connection flag
    var bluetoothDataFlag = false;
    //global database data collection flag
    var sendDatabaseFlag = true;
    //Web Bluetooth sample reseipt speed
    var speed = 10;

    var speed2 = 5;
    //for calculating speed
    var lastTimes = new Array(10).fill(0);

    var lastTimes2 = new Array(10).fill(0);

    var batteryVoltage = 0;

      var button = document.getElementById("connect");
      var message = document.getElementById("message");

$( document ).ready(function() {
      console.log( "ready!" );



            var rangeSlider = function(){
        var slider = $('.range-slider'),
            range = $('.range-slider__range'),
            value = $('.range-slider__value');

        slider.each(function(){

          value.each(function(){
            var value = $(this).prev().attr('value');
            $(this).html(value);
          });

          if( $(this).hasClass('nn-architecture') ){ $('.range-slider__value.nn-architecture').html('7:5:2:1'); }

          range.on('input', function(){
            var labels = ['5:2:1', '5:5:1', '5:5:2:1', '5:5:5:1', '7:7:1', '7:5:2:1', '7:7:2:1', '7:7:7:1', '2:2:2:1'];
            $(this).next(value).html(this.value);

            if( $(this).hasClass('nn-architecture') ){ $(this).next(value).html( labels[this.value] ); }

          });
        });
      }

      rangeSlider();

      //RANGE SLIDER EVENT HANDLER
      $( ".range-slider" ).each(function() {

        if($(this).hasClass("nn-architecture")){
          // Add labels to slider whose values
          // are specified by min, max and whose
          // step is set to 1

          // Get the options for this slider
          //var opt = $(this).data().uiSlider.options;
          // Get the number of possible values
          var $input = $(this).find("input");
          var min = parseInt($input.attr("min"));
          var max = parseInt($input.attr("max"));
          var step = parseInt($input.attr("step"));
          var increment = parseInt($input.attr("increment"));
          var vals = max - min; //opt.max - opt.min;
          //if(min < 0){ vals = max + min; }
          var labels = ['5:2:1', '5:5:1', '5:5:2:1', '5:5:5:1', '7:7:1', '7:5:2:1', '7:7:2:1', '7:7:7:1', '2:2:2:1'];

          // Space out values
          for (var i = 0; (i * increment) <= vals; i++) {
              var s = min + (i * increment);
              var el = $('<label>'+ labels[s] +'</label>').css('left',( 4 + Math.abs((s-min)/vals) *($input.width() -24)+'px'));
           //   var el = $('<label>'+ s +'</label>').css('left',( 3 + ((s-min)/vals) *($input.width() -24)+'px'));
           if(s == 0){ el = $('<label>'+ labels[s] +'</label>').css('left',( 21 + Math.abs((s-min)/vals) *($input.width() -24)+'px')); }
           if(s == vals){ el = $('<label>'+ labels[s] +'</label>').css('left',( -20 + Math.abs((s-min)/vals) *($input.width() -24)+'px')); }


           $(this).append(el);
          }
        }  
      });


  }); //end of on document load



</script>
