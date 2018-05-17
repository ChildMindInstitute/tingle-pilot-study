/*
​x=r sin(φ)cos(θ)
​y=r sin(φ)sin(θ)
​z=r cos(φ)
*/

/* DATA SAMPLE TEMPLATE
{
  Thermo1 Object Temp,
  Thermo2 Object Temp,
  Thermo3 Object Temp,
  Thermo4 Object Temp,
  Distance,
  Pitch,
  Roll,
  Acc X,
  Acc Y,
  Acc Z,
  Thermo Ave. Device Temp,
  Time Stamp,
  Hand,
  Target,
  on/off Target Observed
}*/

/* NN selection configuration codes
0: none
1: mouth
2: front head
3: top head
4: back head
5: right head
6: left head
left hand: 0
right hand 1
example - right hand, back head: 14
*/ 



  /*******************************************************************************************************************
  *********************************************** INITIALIZE *********************************************************
  ********************************************************************************************************************/


window.onload = function(){

  let button = document.getElementById("connect");
  let message = document.getElementById("message");

  if ( 'bluetooth' in navigator === false ) {
      button.style.display = 'none';
      message.innerHTML = 'This browser doesn\'t support the <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API" target="_blank">Web Bluetooth API</a> :(';
  }


  let accelerometerData, objectTempData, proximityData, ambientTempData, heartRateData;

  var timeStamp = new Date().getTime();

  //default active hand is left
  var activeHand = "L"; 
  //single target
  var activeTarget = "none"; 

  //is device observed to be on target
  onTarget = false;

  //record data each time a sensor data sample is received
  recordFlag = false;

  //sensor array sample data
  var sensorDataArray = new Array(18).fill(0); 

  //sensor array sample data FOR CUSTOM TRAINING
  var NN1TrueDataArray = new Array; 
  var NN1FalseDataArray = new Array; 
  var NN2TrueDataArray = new Array; 
  var NN2FalseDataArray = new Array; 

  var NN1Architecture = 'none';
  var NN2Architecture = 'none';

  var NN1NumInputs = 5;
  var NN2NumInputs = 5;

  //master session data array of arrays
  var sensorDataSession = [];

  //which samples in the session data array are part of a particular sample set
  var sessionSampleSetIndex = [];

  //track number of sets
  var numSets = 0; 

  var getSamplesFlag = 0;
  var getSamplesTypeFlag = 0; //0=none 1=NN1T 2=NN1F 3=NN2T 4=NN2F

  //do we have a trained NN to apply to live sensor data?
  var haveNNFlag1 = false;
  var trainNNFlag1 = false;
  var activeNNFlag1 = false;

  var haveNNFlag2 = false;
  var trainNNFlag2 = false;
  var activeNNFlag2 = false;

  //load NN exported activation functions and weights
  var loadNNFlag = false;

  //NN scores
  var scoreArray = new Array(1).fill(0);

	var initialised = false;
	var timeout = null;
  
  //Get JSON for pilot script
  //var pilotScriptJsonUrl = 'https://okgab.com/trichpilot/js/tinglePilotAppScript.json'; 
  var pilotScriptJsonUrl = 'https://github.com/ChildMindInstitute/tingle-gesture-recognition-pilot-toolkit/blob/master/js/tinglePilotAppScript.json?raw=true'; 
  var pilotScriptJsonData = {};
  $.ajax({
      type: 'GET',
      url: pilotScriptJsonUrl,
      async: false,
      contentType: "application/json",
      dataType: 'json',
      success: function (data) {
       //   alert('success');
          console.log(data);
          pilotScriptJsonData = data;
      },
      error: function (e) {
      //    alert('error');
          console.log(e);

      }
  });
  var scriptStepCount = 1;
  rotateScript(scriptStepCount);
  
  $('#script-rotate-right').click(function(){
       if(scriptStepCount < pilotScriptJsonData.length - 2 ){
          scriptStepCount++;
          rotateScript(scriptStepCount);
      }
  });

  $('#script-rotate-left').click(function(){
      if(scriptStepCount > 1 ){
          scriptStepCount--;
          rotateScript(scriptStepCount);
      }
  });

  function rotateScript(currentStepIndex){ 
      $("#script-last-step").html(pilotScriptJsonData[currentStepIndex - 1].message);
      $("#this-step-text").html(pilotScriptJsonData[currentStepIndex].message);
      $("#script-next-step").html(pilotScriptJsonData[currentStepIndex + 1].message);
  }


  //default file name
  $("#file-name-input").val("data_" + timeStamp + "_" + activeHand + "_" + activeTarget);

//add smoothie.js time series streaming data chart
 // var chartHeight =  $(window).height() / 3;
  var chartHeight =  100;
  var chartWidth = $(window).width();

  $("#streaming-data-chart").html('<canvas id="chart-canvas" width="' + chartWidth + '" height="' + chartHeight + '"></canvas>');

  var streamingChart = new SmoothieChart({
  /*  grid: { strokeStyle:'rgb(125, 0, 0)', fillStyle:'rgb(60, 0, 0)',
            lineWidth: 1, millisPerLine: 250, verticalSections: 6, },
    labels: { fillStyle:'rgb(60, 0, 0)' } */
  });

  /*******************************************************************************************************************
  **************************************** STREAMING SENSOR DATA CHART ***********************************************
  ********************************************************************************************************************/


  streamingChart.streamTo(document.getElementById("chart-canvas"), 350 /*delay*/);
  var lineThermo1   = new TimeSeries();
  var lineThermo2   = new TimeSeries();
  var lineThermo3   = new TimeSeries();
  var lineThermo4   = new TimeSeries();
  var linePitch     = new TimeSeries();
  var lineRoll      = new TimeSeries();
  var lineProximity = new TimeSeries();
  var lineNN1 = new TimeSeries();
  var lineNN2 = new TimeSeries();
  streamingChart.addTimeSeries(lineThermo1,
  { strokeStyle:'rgb(133, 87, 35)', lineWidth:3 });
  streamingChart.addTimeSeries(lineThermo2,
  { strokeStyle:'rgb(185, 156, 107)', lineWidth:3 });
  streamingChart.addTimeSeries(lineThermo3,
  { strokeStyle:'rgb(143, 59, 27)', lineWidth:3 });
  streamingChart.addTimeSeries(lineThermo4,
  { strokeStyle:'rgb(213, 117, 0)', lineWidth:3 });
  streamingChart.addTimeSeries(linePitch,
  { strokeStyle:'rgb(128, 128, 128)', lineWidth:3 });
  streamingChart.addTimeSeries(lineRoll,
  { strokeStyle:'rgb(240, 240, 240)', lineWidth:3 });
  streamingChart.addTimeSeries(lineProximity,
  { strokeStyle:'rgb(128, 128, 255)', lineWidth:3 });
  streamingChart.addTimeSeries(lineNN1,
  { strokeStyle:'rgb(72, 244, 68)', lineWidth:4 });
  streamingChart.addTimeSeries(lineNN2,
  { strokeStyle:'rgb(244, 66, 66)', lineWidth:4 });

  //min/max streaming chart button
  $('#circleDrop').click(function(){

      $('.card-middle').slideToggle();
      $('.close').toggleClass('closeRotate');

      var chartHeight =  $(window).height() / 1.2;
      var chartWidth = $(window).width();

      if( $("#chart-size-button").hasClass('closeRotate') ){
            $("#streaming-data-chart").html('<canvas id="chart-canvas" width="' + chartWidth + '" height="' + chartHeight + '"></canvas>');
      } else {
          $("#streaming-data-chart").html('<canvas id="chart-canvas" width="' + chartWidth + '" height="' + 100 + '"></canvas>');
      }

      streamingChart.streamTo(document.getElementById("chart-canvas"), 350 /*delay*/);

      //hide controls
      $("#basic-interface-container, #hand-head-ui-container, #nn-slide-controls, .console, #interface-controls, #dump-print, #record-controls").toggleClass("hide-for-chart");

  });

  /*******************************************************************************************************************
  **************************************** TARGET SELECTION UI *******************************************************
  ********************************************************************************************************************/

  //Rotate target selection head graphic
  $("#head-rotate-left").click(function() {
      var $head = $("#head-image-container");

      if( $head.hasClass("front-active") ){
          $head.toggleClass("front-active");
          $head.toggleClass("right-active");

      } else if( $head.hasClass("right-active") ){
          $head.toggleClass("right-active");
          $head.toggleClass("back-active");

      } else if( $head.hasClass("back-active") ){
          $head.toggleClass("back-active");
          $head.toggleClass("left-active");

      } else if( $head.hasClass("left-active") ){
          $head.toggleClass("left-active");
          $head.toggleClass("front-active");
          
      } 
  });

  $("#head-rotate-right").click(function() {
      var $head = $("#head-image-container");

      if( $head.hasClass("front-active") ){
          $head.toggleClass("front-active");
          $head.toggleClass("left-active");

      } else if( $head.hasClass("left-active") ){
          $head.toggleClass("left-active");
          $head.toggleClass("back-active");

      } else if( $head.hasClass("back-active") ){
          $head.toggleClass("back-active");
          $head.toggleClass("right-active");

      } else if( $head.hasClass("right-active") ){
          $head.toggleClass("right-active");
          $head.toggleClass("front-active");
          
      } 
  });

  //handle hand selction toggle button
  $("#hand-btn").click(function() {
    if( $(this).hasClass("left-active") ){
        activeHand = "R";
    } else { activeHand = "L"; }

      $(this).toggleClass("left-active");
      $(this).toggleClass("right-active");
  });

  //handle target selection UI
  $(".target-selector").click(function() {
      var newTarget = $(this).attr("target");
      console.log("target selected: " + newTarget);
      $(".target-selector").removeClass("target-active");

      if(newTarget == activeTarget){
          activeTarget = "none";
      } else {
          activeTarget = newTarget;
          $(this).addClass("target-active");
      } 
      $("#selected-targets").html("Target: " + activeTarget);
      $("#selected-targets").attr("target" , activeTarget);
  });

  // display target names on hover in target selection UI
  $(".target-selector").hover(function() {
      var displayTarget = $(this).attr("target");
      $("#target-hover-label").html(displayTarget);
      $("#target-hover-label").css("display", "block");
  });
  $(".target-selector").mouseout(function(){
      $("#target-hover-label").css("display", "none");
  });

  // indicate on target when button is pressed
  $("#script-this-step").mousedown(function() {
      onTarget = true;
      $("#script-this-step").addClass("on-target");
      $("#script-this-step-toggle").html("ON TARGET");
  }).mouseup(function() {
      onTarget = false;
      $("#script-this-step").removeClass("on-target");
      $("#script-this-step-toggle").html("OFF TARGET"); 
  });

  /*******************************************************************************************************************
  *********************************************** WEB BLUETOOTH ******************************************************
  ********************************************************************************************************************/


//Web Bluetooth connection button and ongoing device data update function
  button.onclick = function(e){
    var sensorController = new ControllerWebBluetooth("ChildMind");
    sensorController.connect();

    //ON SENSOR DATA UPDATE
    var bluetoothDataFlag = false;
    sensorController.onStateChange(function(state){ bluetoothDataFlag = true; });
 //   sensorController.onStateChange(function(state){

    //check for new data every X milliseconds - this is to decouple execution from Web Bluetooth actions
    setInterval(function(){ if(bluetoothDataFlag == true){ 
  /*    objectTempData = state.objectTemp;
      proximityData = state.proximityData;
      accelerometerData = state.accelerometer;
      ambientTempData = state.ambientTemp;
      heartRateData = state.heartRate; */
      timeStamp = new Date().getTime();

      //load data into global array
      sensorDataArray = new Array(12).fill(0); 

      sensorDataArray[0] = state.objectTemp.a.toFixed(1);
      sensorDataArray[1] = state.objectTemp.b.toFixed(1); 
      sensorDataArray[2] = state.objectTemp.c.toFixed(1);
      sensorDataArray[3] = state.objectTemp.d.toFixed(1);  

      sensorDataArray[4] = state.proximityData.a.toFixed(1);

      sensorDataArray[5] = state.accelerometer.pitch.toFixed(1);
      sensorDataArray[6] = state.accelerometer.roll.toFixed(1);
      sensorDataArray[7] = state.accelerometer.x.toFixed(2);
      sensorDataArray[8] = state.accelerometer.y.toFixed(2);
      sensorDataArray[9] = state.accelerometer.z.toFixed(2);

      sensorDataArray[10] = state.ambientTemp.a.toFixed(2);

      sensorDataArray[11] = timeStamp;
      sensorDataArray[12] = activeHand;
      sensorDataArray[13] = activeTarget;
      //observed presence of device on target
      sensorDataArray[14] = onTarget;


      //update time series chart
      var rawThermo1Chart = ( (sensorDataArray[0] - 76) / 24 );
      var rawThermo2Chart = ( (sensorDataArray[1] - 76) / 24 );
      var rawThermo3Chart = ( (sensorDataArray[2] - 76) / 24 );
      var rawThermo4Chart = ( (sensorDataArray[3] - 76) / 24 );
      var rawPitchChart = ( sensorDataArray[5] / 400 );
      var rawRollChart = ( sensorDataArray[6] / 400 );
      var rawProximityChart = ( sensorDataArray[4] / 270 );

      //sensor values in bottom 2/3 of chart , 1/10 height each
      rawThermo1Chart = (rawThermo1Chart / 4.5) + 7 * 0.1; 
      rawThermo2Chart = (rawThermo2Chart / 4.5) + 6 * 0.1;
      rawThermo3Chart = (rawThermo3Chart / 4.5) + 5 * 0.1;
      rawThermo4Chart = (rawThermo4Chart / 4.5) + 4 * 0.1;
      rawPitchChart = (rawPitchChart / 7) + 3 * 0.1;
      rawRollChart = (rawRollChart / 7) + 2 * 0.1;
      rawProximityChart = (rawProximityChart / 10) + 1 * 0.1;

      lineThermo1.append(timeStamp, rawThermo1Chart );
      lineThermo2.append(timeStamp, rawThermo2Chart );
      lineThermo3.append(timeStamp, rawThermo3Chart );
      lineThermo4.append(timeStamp, rawThermo4Chart );
      linePitch.append(timeStamp, rawPitchChart );
      lineRoll.append(timeStamp, rawRollChart );
      lineProximity.append(timeStamp, rawProximityChart );


      //if data sample collection has been flagged
    //  getSensorData();
      if(getSamplesFlag > 0){
          collectData();
      } else if (trainNNFlag1 || trainNNFlag2){
          //don't do anything
      } else {
          if(haveNNFlag1 && activeNNFlag1){  //we have a NN and we want to apply to current sensor data
              getNNScore(1);
          }  else if(loadNNFlag){  // !!! NOPE DISABLE FIRST LOADED NN
              getNNScore(1);
          } 
          if(haveNNFlag2 && activeNNFlag2){  //we have a NN and we want to apply to current sensor data
              getNNScore(2);
          } else if(loadNNFlag){
              getNNScore(2);
          }

      }

	    console.log("loadNNFlag in main loop: " + loadNNFlag);

      displayData();
      bluetoothDataFlag = false; } }, 100);
 //   });
  }

  

  function displayData(){

      var objectTempElement1 = document.getElementsByClassName('object-temp-1-data')[0];
      objectTempElement1.innerHTML = sensorDataArray[0];

      var objectTempElement2 = document.getElementsByClassName('object-temp-2-data')[0];
      objectTempElement2.innerHTML = sensorDataArray[1];

      var objectTempElement3 = document.getElementsByClassName('object-temp-3-data')[0];
      objectTempElement3.innerHTML = sensorDataArray[2];

      var objectTempElement4 = document.getElementsByClassName('object-temp-4-data')[0];
      objectTempElement4.innerHTML = sensorDataArray[3];

      var proximityElement = document.getElementsByClassName('proximity-data')[0];
      proximityElement.innerHTML = sensorDataArray[4];

      var accelerometerPitchDiv = document.getElementsByClassName('accelerometer-pitch-data')[0];
      accelerometerPitchDiv.innerHTML = sensorDataArray[5];

      var accelerometerRollDiv = document.getElementsByClassName('accelerometer-roll-data')[0];
      accelerometerRollDiv.innerHTML = sensorDataArray[6];

      var accelerometerXElement = document.getElementsByClassName('accelerometer-x-data')[0];
      accelerometerXElement.innerHTML = sensorDataArray[7];

      var accelerometerYElement = document.getElementsByClassName('accelerometer-y-data')[0];
      accelerometerYElement.innerHTML = sensorDataArray[8];

      var accelerometerZElement = document.getElementsByClassName('accelerometer-z-data')[0];
      accelerometerZElement.innerHTML = sensorDataArray[9];

      var ambientTempAverageElement = document.getElementsByClassName('ambient-temp-average-data')[0];
      ambientTempAverageElement.innerHTML = sensorDataArray[10];

    //  var rawHeartRateData = document.getElementsByClassName('raw-ppg-heart-data')[0];
    //  rawHeartRateData.innerHTML = heartRateData.a;

  }

  function getSensorData(){

    if(objectTempData){
	    sensorDataArray[0] = objectTempData.a.toFixed(2);
	    sensorDataArray[1] = objectTempData.b.toFixed(2); 
	    sensorDataArray[2] = objectTempData.c.toFixed(2);
	    sensorDataArray[3] = objectTempData.d.toFixed(2);  

      sensorDataArray[4] = proximityData.a.toFixed(2);

      sensorDataArray[5] = accelerometerData.pitch.toFixed(2);
      sensorDataArray[6] = accelerometerData.roll.toFixed(2);
      sensorDataArray[7] = accelerometerData.x.toFixed(2);
      sensorDataArray[8] = accelerometerData.y.toFixed(2);
      sensorDataArray[9] = accelerometerData.z.toFixed(2);
    }

    if(ambientTempData){
      	sensorDataArray[10] = ambientTempData.a.toFixed(2);
    } 

  } //end code executed after new sensor data

  function collectData(){

      var collectedDataArray =  new Array(12).fill(0);  //12 device 
      collectedDataArray = sensorDataArray;
    //  var positionNumber = $('#master-pose-input').val() - 1;

      console.log("web bluetooth sensor data:");

      console.dir(collectedDataArray);

      //add sample to set
      sensorDataSession.push(collectedDataArray);

      //minimum distance value for true data
     // if( (getSamplesTypeFlag == 1 || getSamplesTypeFlag == 3 ) && collectedDataArray[4] < 100){ collectedDataArray[4] = 100; }

      if(getSamplesTypeFlag == 1){ NN1TrueDataArray.push(collectedDataArray); $('.message-nn1-true').html(NN1TrueDataArray.length); }
      else if(getSamplesTypeFlag == 2){ NN1FalseDataArray.push(collectedDataArray); $('.message-nn1-false').html(NN1FalseDataArray.length); }
      else if(getSamplesTypeFlag == 3){ NN2TrueDataArray.push(collectedDataArray); $('.message-nn2-true').html(NN2TrueDataArray.length); }
      else if(getSamplesTypeFlag == 4){ NN2FalseDataArray.push(collectedDataArray); $('.message-nn2-false').html(NN2FalseDataArray.length); }

      sessionSampleSetIndex.push(numSets);

      console.log("Set Index: "); 
      console.dir(sessionSampleSetIndex);

      getSamplesFlag = getSamplesFlag - 1;

      if(getSamplesFlag > 0){
          //console messages
        var consoleSamples = document.getElementsByClassName('console-samples')[0];
        consoleSamples.innerHTML = sensorDataSession.length;
    }

      if(getSamplesFlag == 0){
          //console messages
      //    var consoleSamples = document.getElementsByClassName('console-samples')[0];
      //    consoleSamples.innerHTML = sensorDataSession.length;

          var consoleSamples = document.getElementsByClassName('console-sets')[0];
          consoleSamples.innerHTML = numSets;
      }

  }

  /*******************************************************************************************************************
  ********************************** COLLECT, PRINT, LOAD BUTTON ACTIONS *********************************************
  ********************************************************************************************************************/

  /*************** COLLECT SAMPLE - SONSOR AND MODEL DATA - STORE IN GSHEET AND ADD TO NN TRAINING OBJECT *****************/
  $('#collect-true-1').click(function() {
      //how many samples for this set?
      //this flag is applied in the bluetooth data notification function
      getSamplesFlag = $('input.sample-size').val();
      getSamplesTypeFlag = 1;
      console.log("Collect btn NN1T #samples flag: " + getSamplesFlag);
      
      numSets = numSets + 1;
  }); 

   $('#collect-false-1').click(function() {
      //how many samples for this set?
      //this flag is applied in the bluetooth data notification function
      getSamplesFlag = $('input.sample-size').val();
      getSamplesTypeFlag = 2;
      console.log("Collect btn NN1F #samples flag: " + getSamplesFlag);
      
      numSets = numSets + 1;
  }); 

   $('#collect-true-2').click(function() {
      //how many samples for this set?
      //this flag is applied in the bluetooth data notification function
      getSamplesFlag = $('input.sample-size').val();
      getSamplesTypeFlag = 3;
      console.log("Collect btn NN2T #samples flag: " + getSamplesFlag);
      
      numSets = numSets + 1;
  }); 

   $('#collect-false-2').click(function() {
      //how many samples for this set?
      //this flag is applied in the bluetooth data notification function
      getSamplesFlag = $('input.sample-size').val();
      getSamplesTypeFlag = 4;
      console.log("Collect btn NN2F #samples flag: " + getSamplesFlag);
      
      numSets = numSets + 1;
  }); 

  $('#clear-true-1').click(function() {
  	  NN1TrueDataArray = new Array; 
      sensorDataArray = new Array(18).fill(0); 
      sensorDataSession =new Array;  
  	  updateSampleCountDisplay();
      $("#dump-print").html("");
      console.log("Clear NN1TrueDataArray");
  }); 
  $('#clear-false-1').click(function() {
  	  NN1FalseDataArray = new Array; 
      sensorDataArray = new Array(18).fill(0); 
      sensorDataSession =new Array;  
  	  updateSampleCountDisplay();
      $("#dump-print").html("");
      console.log("Clear NN1FalseDataArray");
  }); 
  $('#clear-true-2').click(function() {
  	  NN2TrueDataArray = new Array; 
      sensorDataArray = new Array(18).fill(0); 
      sensorDataSession =new Array;  
  	  updateSampleCountDisplay();
      $("#dump-print").html("");
      console.log("Clear NN2TrueDataArray");
  }); 
  $('#clear-false-2').click(function() {
  	  NN2FalseDataArray = new Array; 
      sensorDataArray = new Array(18).fill(0); 
      sensorDataSession =new Array;  
  	  updateSampleCountDisplay();
      $("#dump-print").html("");
      console.log("Clear NN2FalseDataArray");
  }); 

  //print sensor data to browser at bottom of app screen
  $('#print-btn').click(function() {
      console.log("print button"); 

      $("#dump-print").html( JSON.stringify(sensorDataSession) );
      $("#dump-print").addClass("active-print");
      console.log("SENSOR SESSIONS DATA: " + sensorDataSession);
  }); 

  //load data from js file (JSON or JS object) into sensor session data
  $('#load-btn').click(function() {
      console.log("load button"); 
    //  sensorDataSession = exportedSensorData;
      NN1TrueDataArray = importedTrueData; 
      NN1FalseDataArray = importedFalseData; 
  }); 

  /*******************************************************************************************************************
  ************************************** DATA RECORD AND FILE NAMES **************************************************
  ********************************************************************************************************************/

  //set flag so data is recorded each time a sample is recieved
  $("#record-btn").click(function() {
    if( $(this).hasClass("active-data-ui") ){
        recordFlag = !recordFlag;
        $("#record-btn").toggleClass("active-data-ui");
        $("#pause-btn").toggleClass("active-data-ui");
    }
  }); 

  //set flag so data is not recorded each time a sample is recieved
  $("#pause-btn").click(function() {
    if( $(this).hasClass("active-data-ui") ){
        recordFlag = !recordFlag;
        $("#record-btn").toggleClass("active-data-ui");
        $("#pause-btn").toggleClass("active-data-ui");
    }
  }); 
   

  function updateSampleCountDisplay(){
  	$('.message-nn1-true').html(NN1TrueDataArray.length);
  	$('.message-nn1-false').html(NN1FalseDataArray.length);
  	$('.message-nn2-true').html(NN2TrueDataArray.length);
  	$('.message-nn2-false').html(NN2FalseDataArray.length);
  }




  /*******************************************************************************************************************
  *********************************************** NEURAL NETWORKS ****************************************************
  ********************************************************************************************************************/
    /**
   * Attach synaptic neural net components to app object
   */
  var nnRate = $("#rate-input").val();
  var nnIterations = $("#iterations-input").val();
  var nnError = $("#error-input").val();

   // ************** NEURAL NET #1
  var Neuron = synaptic.Neuron;
  var Layer = synaptic.Layer;
  var Network = synaptic.Network;
  var Trainer = synaptic.Trainer;
  var Architect = synaptic.Architect;
  //var neuralNet = new Architect.LSTM(19, 75, 75);
  var neuralNet = new Architect.LSTM(7, 5, 2, 1);
  var trainer = new Trainer(neuralNet);
  var trainingData;

  $('#train-btn').click(function() {
      console.log("train button 1"); 
      trainNNFlag1 = true;
      trainNN(1);
  });

  $('#activate-btn').click(function() {
      console.log("activate button"); 
      activeNNFlag1 = true;
      $('#activate-btn').toggleClass("activatedNN");

      //if loaded NN, turn off
      if(loadNNFlag){
          loadNNFlag = false;
          $('#load-nn-btn').toggleClass("activatedNN");
      }
  });

    // ************* NEURAL NET #2
  var Neuron2 = synaptic.Neuron;
  var Layer2 = synaptic.Layer;
  var Network2 = synaptic.Network;
  var Trainer2 = synaptic.Trainer;
  var Architect2 = synaptic.Architect;
  //var neuralNet = new Architect.LSTM(19, 75, 75);
  var neuralNet2 = new Architect2.LSTM(5, 5, 2, 1);
  var trainer2 = new Trainer2(neuralNet2);
  var trainingData2;

  $('#train2-btn').click(function() {
      console.log("train button 2"); 
      trainNNFlag2 = true;
      trainNN(2);
  });

  $('#activate2-btn').click(function() {
      console.log("activate button"); 
      activeNNFlag2 = true;
      $('#activate2-btn').toggleClass("activatedNN");

      //if leaded NN, turn off
      if(loadNNFlag){
          loadNNFlag = false;
          $('#load-nn-btn').toggleClass("activatedNN");
      }
  });


  // ************* LOAD TWO EXPORTED NEURAL NET ACTIVATION FUNCTIONS AND WEIGHTS
  $('#load-nn-btn').click(function() {
      console.log("load exported NN button"); 
      loadNNFlag = true;
      $('#load-nn-btn').toggleClass("activatedNN");
  });



function getNNScore(selectNN){

  var scoreArray = new Array(1).fill(0);
  var timeStamp = new Date().getTime();
  var displayScore;

    if(selectNN == 1){
        if(NN1NumInputs == 5){ var feedArray = new Array(5).fill(0); } else if(NN1NumInputs == 7){var feedArray = new Array(7).fill(0); } else if(NN1NumInputs == 2){var feedArray = new Array(2).fill(0); }
            if(NN1NumInputs == 5 || NN1NumInputs == 7){
             feedArray[0] = sensorDataArray[0] / 101;
             feedArray[1] = sensorDataArray[1] / 101;
             feedArray[2] = sensorDataArray[2] / 101;
             feedArray[3] = sensorDataArray[3] / 101;

            feedArray[4] = sensorDataArray[4] / 250;
        //     feedArray[4] = sensorDataArray[4] / 450;
            }

            if(NN1NumInputs == 7){
             feedArray[5] = sensorDataArray[5] / 360;
             feedArray[6] = sensorDataArray[6] / 360;
            }

            if(NN1NumInputs == 2){
             feedArray[0] = sensorDataArray[5] / 360;
             feedArray[1] = sensorDataArray[6] / 360;
            }

        // use trained NN or loaded NN
        if(haveNNFlag1 && activeNNFlag1){ 
            scoreArray = neuralNet.activate(feedArray);
        } else if(loadNNFlag){
            scoreArray = neuralNetwork1(feedArray);
        }
        console.log("NN1 FEED ARRAY: " + feedArray);
        console.log("NN1 SCORE ARRAY: " + scoreArray);

        displayScore = scoreArray[0].toFixed(4) * 100;
        displayScore = displayScore.toFixed(2);
        $(".message-nn1-score").html( displayScore + '%' );
        var rawLineNN1Chart = scoreArray[0].toFixed(4);
        rawLineNN1Chart = (rawLineNN1Chart / 3) + 0.8;
        lineNN1.append(timeStamp, rawLineNN1Chart );

    } else if(selectNN == 2){
        if(NN2NumInputs == 5){ var feedArray = new Array(5).fill(0); } else if(NN2NumInputs == 7){var feedArray = new Array(7).fill(0); } else if(NN2mInputs == 2){var feedArray = new Array(2).fill(0); }
            if(NN2NumInputs == 5 || NN2NumInputs == 7){
             feedArray[0] = sensorDataArray[0] / 101;
             feedArray[1] = sensorDataArray[1] / 101;
             feedArray[2] = sensorDataArray[2] / 101;
             feedArray[3] = sensorDataArray[3] / 101;

            feedArray[4] = sensorDataArray[4] / 250;
           //  feedArray[4] = sensorDataArray[4] / 450;
            }

            if(NN2NumInputs == 7){
             feedArray[5] = sensorDataArray[5] / 360;
             feedArray[6] = sensorDataArray[6] / 360;
            }

            if(NN2NumInputs == 2){
             feedArray[0] = sensorDataArray[5] / 360;
             feedArray[1] = sensorDataArray[6] / 360;
            }

        if(haveNNFlag2 && activeNNFlag2){ 
            scoreArray = neuralNet2.activate(feedArray);
        } else if(loadNNFlag){
            scoreArray = neuralNetwork2(feedArray);
        }

        console.log("NN2 FEED ARRAY: " + feedArray);
        console.log("NN2 SCORE ARRAY: " + scoreArray);

        displayScore = scoreArray[0].toFixed(4) * 100;
        displayScore = displayScore.toFixed(2);
        $(".message-nn2-score").html( displayScore + '%' );
        var rawLineNN2Chart = scoreArray[0].toFixed(4);
        rawLineNN2Chart = (rawLineNN2Chart / 3) + 0.8;
        lineNN2.append(timeStamp, rawLineNN2Chart );
    } 
    
}

  $('#export-btn').click(function() {
      console.log("export1 NN button"); 
      //clear everything but key values from stored NN
      neuralNet.clear();

      //export optimized weights and activation function
      var standalone = neuralNet.standalone();

      //convert to string for parsing
      standalone = standalone.toString();

      console.log(standalone);
      $("#dump-print").html(standalone);
      $("#dump-print").addClass("active-print");
  });

  $('#export2-btn').click(function() {
      console.log("export2 NN button"); 
      //clear everything but key values from stored NN
      neuralNet2.clear();

      //export optimized weights and activation function
      var standalone = neuralNet2.standalone();

      //convert to string for parsing
      standalone = standalone.toString();

      console.log(standalone);
      $("#dump-print").html(standalone);
      $("#dump-print").addClass("active-print");
  });

//Send target configuration for pre-trained neural networks on device
  $('#configure-device').click(function() {
    sendCommandFlag = true;
  }); 


/**************************** TRAIN NN ******************************/
function trainNN(selectNN){
//'5:2:1', '5:5:1', '5:5:2:1', '5:5:5:1', '7:2:1', '7:7:1', '7:7:2:1', '7:7:7:1'
  //  var processedDataSession = sensorDataSession;
    var processedDataSession = new Array;
    var falseDataArray = new Array; 
    var trueDataArray = new Array;

    trainingData = new Array;

    var rawNNArchitecture = $(".range-slider__value.nn-architecture").html();
    var numInputs = parseInt( rawNNArchitecture.charAt(0) );

    nnRate = $("#rate-input").val();
    nnIterations = $("#iterations-input").val();
    nnError = $("#error-input").val();

    if(selectNN == 1){
      trueDataArray = NN1TrueDataArray;
      falseDataArray = NN1FalseDataArray;
    } else if(selectNN == 2){
      trueDataArray = NN2TrueDataArray;
      falseDataArray = NN2FalseDataArray;     
    }

    //combine true and false data
    var addSample = new Array(13).fill(0);;

    for(var j=0; j<trueDataArray.length; j++){
        addSample = trueDataArray[j];
        addSample[12] = 1; //true
        processedDataSession.push(addSample);
    }
    for(var k=0; k<falseDataArray.length; k++){
        addSample = falseDataArray[k];
        addSample[12] = 0; //false
        processedDataSession.push(addSample);
    }


 //   console.log("raw NN architecture: " + rawNNArchitecture);

    if(selectNN == 1){ NN1Architecture = rawNNArchitecture; } else { NN2Architecture = rawNNArchitecture; }

    if(rawNNArchitecture == '5:2:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(5, 2, 1); } else { neuralNet2 = new Architect2.LSTM(5, 2, 1); }
    } else if(rawNNArchitecture == '5:5:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(5, 5, 1); } else { neuralNet2 = new Architect2.LSTM(5, 5, 1); }
    } else if(rawNNArchitecture == '5:5:2:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(5, 5, 2, 1); } else { neuralNet2 = new Architect2.LSTM(5, 5, 2, 1); }
    } else if(rawNNArchitecture == '5:5:5:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(5, 5, 5, 1); } else { neuralNet2 = new Architect2.LSTM(5, 5, 5, 1); }
    } else if(rawNNArchitecture == '7:7:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(7, 7, 1); } else { neuralNet2 = new Architect2.LSTM(7, 7, 1); }
    } else if(rawNNArchitecture == '7:5:2:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(7, 5, 2, 1); } else { neuralNet2 = new Architect2.LSTM(7, 5, 2, 1); }
    } else if(rawNNArchitecture == '7:7:2:1'){
      if(selectNN == 1){ neuralNet = new Architect.LSTM(7, 7, 2, 1); } else { neuralNet2 = new Architect2.LSTM(7, 7, 2, 1); }
    } else if(rawNNArchitecture == '7:7:7:1'){
    	if(selectNN == 1){ neuralNet = new Architect.LSTM(7, 7, 7, 1); } else { neuralNet2 = new Architect2.LSTM(7, 7, 7, 1); }
    } else if(rawNNArchitecture == '2:2:2:1'){
      if(selectNN == 1){ neuralNet = new Architect.LSTM(2, 2, 2, 1); } else { neuralNet2 = new Architect2.LSTM(2, 2, 2, 1); }
    }

    if(selectNN == 1){ 
    	NN1Architecture = rawNNArchitecture; 
      NN1NumInputs = numInputs;
    	trainer = new Trainer(neuralNet);
    } else { 
    	NN2Architecture = rawNNArchitecture; 
      NN2NumInputs = numInputs;
    	trainer2 = new Trainer2(neuralNet2);
    }

   // var minMaxAreaSize = processedDataSession.length * 0.01; //sample edge size for average min or max over that area
  //  console.log("SIZE OF UNPROCESSED SESSION DATA: " + processedDataSession.length);


    for(var i=0; i<processedDataSession.length; i++){

        var currentSample = processedDataSession[i];
        var outputArray = new Array(1).fill(0);      

        outputArray[0] = currentSample[12]; //true or false

         if(numInputs == 5){
         	
            var inputArray = new Array(5).fill(0);
            inputArray[0] = currentSample[0] / 101;
            inputArray[1] = currentSample[1] / 101;
            inputArray[2] = currentSample[2] / 101;
            inputArray[3] = currentSample[3] / 101;
            inputArray[4] = currentSample[4] / 250;

        } else if(numInputs == 7){

            var inputArray = new Array(7).fill(0);
            inputArray[0] = currentSample[0] / 101;
            inputArray[1] = currentSample[1] / 101;
            inputArray[2] = currentSample[2] / 101;
            inputArray[3] = currentSample[3] / 101;
            inputArray[4] = currentSample[4] / 250;
            inputArray[5] = currentSample[5] / 360;
            inputArray[6] = currentSample[6] / 360;

        } else if(numInputs == 2){

            var inputArray = new Array(2).fill(0);
            inputArray[0] = currentSample[5] / 360;
            inputArray[1] = currentSample[6] / 360;
        }

  
        trainingData.push({
            input:  inputArray, 
            output: outputArray
        });

        console.log(currentSample + " TRAINING INPUT: " + inputArray + "  --> NN# " + selectNN);
        console.log(currentSample + " TRAINING OUTPUT: " + outputArray + "  --> NN# " + selectNN);
    }


    if(selectNN == 1){
      console.log("TRAINING ON selectNN1 --> interations:" + nnIterations + "  error:" + nnError + "  rate:" + nnRate + "  arch:" + rawNNArchitecture + "  inputs:" + numInputs);

        trainer.train(trainingData, {
            rate: nnRate,
         //   iterations: 15000,
            iterations: nnIterations,
            error: nnError,
            shuffle: true,
         //   log: 1000,
            log: 5,
            cost: Trainer.cost.CROSS_ENTROPY
        });

        //we have a trained NN to use
        haveNNFlag1 = true;
        trainNNFlag1 = false;
        $('#activate-btn').addClass("haveNN");
        $('#export-btn').addClass("haveNN");

    } else if(selectNN == 2){
      console.log("TRAINING ON selectNN2");

          trainer2.train(trainingData, {
            rate: nnRate,
         //   iterations: 15000,
            iterations: nnIterations,
            error: nnError,
            shuffle: true,
         //   log: 1000,
            log: 5,
            cost: Trainer2.cost.CROSS_ENTROPY
        });

        //we have a trained NN to use
        haveNNFlag2 = true;
        trainNNFlag2 = false;
        $('#activate2-btn').addClass("haveNN");
        $('#export2-btn').addClass("haveNN");
    }

}

//end window on load
}



  /*******************************************************************************************************************
  ************************************** SIGN IN FOR FIREBASE ********************************************************
  ********************************************************************************************************************/

var listeningFirebaseRefs = [];



/**
 * Creates a new post for the current user.
 */
function newPostForCurrentUser(title, text) {
  // [START single_value_read]
  var userId = firebase.auth().currentUser.uid;
  return firebase.database().ref('/users/' + userId).once('value').then(function(snapshot) {
    var username = (snapshot.val() && snapshot.val().username) || 'Anonymous';
    // [START_EXCLUDE]
    return writeNewPost(firebase.auth().currentUser.uid, username,
        firebase.auth().currentUser.photoURL,
        title, text);
    // [END_EXCLUDE]
  });
  // [END single_value_read]
}

function newSampleForCurrentUser(t1, t2, t3, t4, distance, pitch, roll) {
  // [START single_value_read]
  var userId = firebase.auth().currentUser.uid;
  return firebase.database().ref('/users/' + userId).once('value').then(function(snapshot) {
    var username = (snapshot.val() && snapshot.val().username) || 'Anonymous';
    // [START_EXCLUDE]
    return writeSampleData(firebase.auth().currentUser.uid, username, t1, t2, t3, t4, distance, pitch, roll);
    // [END_EXCLUDE]
  });
  // [END single_value_read]
}

/**
 * Saves a new post to the Firebase DB.
 */
// [START write_fan_out]
function writeNewPost(uid, username, picture, title, body) {
  // A post entry.
  var postData = {
    author: username,
    uid: uid,
    body: body,
    title: title,
    starCount: 0,
    authorPic: picture
  };

  // Get a key for a new Post.
  var newPostKey = firebase.database().ref().child('posts').push().key;

  // Write the new post's data simultaneously in the posts list and the user's post list.
  var updates = {};
  updates['/posts/' + newPostKey] = postData;

  return firebase.database().ref().update(updates);
}
// [END write_fan_out]

/**
 * Writes the user's data to the database.
 */
// [START basic_write]
function writeUserData(userId, name, email, imageUrl) {
  firebase.database().ref('users/' + userId).set({
    username: name,
    email: email,
    profile_picture : imageUrl
  });
}
// [END basic_write]

function writeSampleData(userId, name, t1, t2, t3, t4, distance, pitch, roll) {

  firebase.database().ref('samples/' + userId).set({
    username: name,
    thermopile1: t1,
    thermopile2: t2,
    thermopile3: t3,
    thermopile4: t4,
    distance: distance,
    pitch: pitch,
    roll: roll
  });
}


  /**
 * The ID of the currently signed-in User. We keep track of this to detect Auth state change events that are just
 * programmatic token refresh but not a User status change.
 */
var currentUID;

/**
 * Triggers every time there is a change in the Firebase auth state (i.e. user signed-in or user signed out).
 */
function onAuthStateChanged(user) {
  // We ignore token refresh events.
  if (user && currentUID === user.uid) {
    return;
  }

 // cleanupUi();
  if (user) {
    currentUID = user.uid;
  //  splashPage.style.display = 'none';
    writeUserData(user.uid, user.displayName, user.email, user.photoURL);
  //  startDatabaseQueries();
  } else {
    // Set currentUID to null.
    currentUID = null;
    // Display the splash page where you can sign-in.
    splashPage.style.display = '';
  }
}

$('#configure-device').click(function() {
    console.log("test send");
  //  writeSampleData(userId, name, t1, t2, t3, t4, distance, pitch, roll)
   // newPostForCurrentUser("TEST TITLE", "test message");
    newSampleForCurrentUser(85, 84, 83, 92, 120, 90, 180);
});

$('#login-button').click(function() {
  var email = $("#email-input").val();
  var password = $("#pass-input").val();
  firebase.auth().createUserWithEmailAndPassword(email, password).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    // ...
  });
  newPostForCurrentUser("TEST TITLE", "test message");
});

$( document ).ready(function() { //on load.

  // Bind Sign in button.
 // signInButton.addEventListener('click', function() {
  $('#sign-in-button').click(function() {
    var provider = new firebase.auth.GoogleAuthProvider();
   // firebase.auth().signInWithPopup(provider);

      firebase.auth().signInWithPopup(provider).then(function(result) {
        // This gives you a Google Access Token. You can use it to access the Google API.
        var token = result.credential.accessToken;
        // The signed-in user info.
        var user = result.user;
        console.log("Signed in as: " + user.displayName + "  " + user.email);
        newPostForCurrentUser("TEST TITLE", "test message");
        // ...
      }).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // The email of the user's account used.
        var email = error.email;
        // The firebase.auth.AuthCredential type that was used.
        var credential = error.credential;
        // ...
      });
  });

  // Bind Sign out button.
 // signOutButton.addEventListener('click', function() {
  $('#sign-out-button').click(function() {
    firebase.auth().signOut();
  });


  // Listen for auth state changes
  firebase.auth().onAuthStateChanged(onAuthStateChanged);

});

  // Saves message on form submit.
 /* messageForm.onsubmit = function(e) {
    e.preventDefault();
    var text = messageInput.value;
    var title = titleInput.value;
    if (text && title) {
      newPostForCurrentUser(title, text).then(function() {
        myPostsMenuButton.click();
      });
      messageInput.value = '';
      titleInput.value = '';
    }
  }; */

  // Bind menu buttons.
 /* recentMenuButton.onclick = function() {
    showSection(recentPostsSection, recentMenuButton);
  };
  myPostsMenuButton.onclick = function() {
    showSection(userPostsSection, myPostsMenuButton);
  };
  myTopPostsMenuButton.onclick = function() {
    showSection(topUserPostsSection, myTopPostsMenuButton);
  };
  addButton.onclick = function() {
    showSection(addPost);
    messageInput.value = '';
    titleInput.value = '';
  };
  recentMenuButton.onclick(); */
//}, false);

