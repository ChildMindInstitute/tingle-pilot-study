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

/*******************************************************************************************************************
 *********************************************** INITIALIZE *********************************************************
 ********************************************************************************************************************/
let accelerometerData, objectTempData, proximityData, ambientTempData, heartRateData;

var timeStamp = new Date().getTime();



//is device observed to be on target
onTarget = false;

//record data each time a sensor data sample is received
recordFlag = false;

var databaseConnected = false;
var batchedData = new Array;
var lastSample = {contents: "empty"}; //last collected data

//sensor array sample data
var sensorDataArray = new Array(18).fill(0);


//master session data array of arrays
var sensorDataSession = [];

//which samples in the session data array are part of a particular sample set
var sessionSampleSetIndex = [];

//track number of sets
var numSets = 0;

var getSamplesFlag = 0;
var getSamplesTypeFlag = 0; //0=none 1=NN1T 2=NN1F 3=NN2T 4=NN2F


var initialised = false;
var timeout = null;

var disconnectedCounter = 0; //allow a few disconnects before giving up connection

//window.onload = function(){
$(document).ready(function() {


    /*******************************************************************************************************************
     *********************************************** WEB BLUETOOTH ******************************************************
     ********************************************************************************************************************/

    //Web Bluetooth connection button and ongoing device data update function
    button.onclick = function(e) {
        //var sensorController = new ControllerWebBluetooth("Tingle");
        //sensorController.connect();

        //ON SENSOR DATA UPDATE
        //sensorController.onStateChange(function(state) {
        //    bluetoothDataFlag = true;
        //});
        $('#connect').html("Connected");

        //check for new data every X milliseconds - this is to decouple execution from Web Bluetooth actions
        setInterval(function() {
            //     bluetoothDataFlag = getBluetoothDataFlag();

            //display time pressed for record button
            buttonTimer();
            timeStamp = new Date().getTime();
            if (bluetoothDataFlag == true) {

                if( !$("#connect").hasClass("connected") ){
                    $("#connect").addClass("connected");
                    $("#console").html("Connected");
                    disconnectedCounter = 0;
                }

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
                var rawThermo1Chart = ((sensorDataArray[0] - 76) / 24);
                var rawThermo2Chart = ((sensorDataArray[1] - 76) / 24);
                var rawThermo3Chart = ((sensorDataArray[2] - 76) / 24);
                var rawThermo4Chart = ((sensorDataArray[3] - 76) / 24);
                var rawPitchChart = (sensorDataArray[5] / 400);
                var rawRollChart = (sensorDataArray[6] / 400);
                var rawProximityChart = (sensorDataArray[4] / 270);

                //sensor values in bottom 2/3 of chart , 1/10 height each
                rawThermo1Chart = (rawThermo1Chart / 4.5) + 7 * 0.1;
                rawThermo2Chart = (rawThermo2Chart / 4.5) + 6 * 0.1;
                rawThermo3Chart = (rawThermo3Chart / 4.5) + 5 * 0.1;
                rawThermo4Chart = (rawThermo4Chart / 4.5) + 4 * 0.1;
                rawPitchChart = (rawPitchChart / 7) + 3 * 0.1;
                rawRollChart = (rawRollChart / 7) + 2 * 0.1;
                rawProximityChart = (rawProximityChart / 10) + 1 * 0.1;

                lineThermo1.append(timeStamp, rawThermo1Chart);
                lineThermo2.append(timeStamp, rawThermo2Chart);
                lineThermo3.append(timeStamp, rawThermo3Chart);
                lineThermo4.append(timeStamp, rawThermo4Chart);
                linePitch.append(timeStamp, rawPitchChart);
                lineRoll.append(timeStamp, rawRollChart);
                lineProximity.append(timeStamp, rawProximityChart);


                //if data sample collection has been flagged
                //  getSensorData();
                if (getSamplesFlag > 0) {
                    collectData();
                }
              //  console.log("databaseConnected: " + databaseConnected + " sendDatabaseFlag: " + sendDatabaseFlag + "recordFlag: " + recordFlag);

                //SEND DATA TO FIREBASE

                displayData();

                $("#connect").html(speed.toFixed(2) + 'Hz');

                bluetoothDataFlag = false;

            } else {  //if not connected to Bluetooth
                disconnectedCounter++;
                if( $("#connect").hasClass("connected") && disconnectedCounter > 15){
                    disconnectedCounter = 0;
                    $("#connect").removeClass("connected");
                    $("#console").html("Disconnected");
                    $("#connect").html("Connect");
                }
            }
            if (databaseConnected && sendDatabaseFlag && recordFlag) {
                var newData = {};
                if (bluetoothDataFlag == true) {
                  newData.thermopile1 = sensorDataArray[0];
                  newData.thermopile2 = sensorDataArray[1];
                  newData.thermopile3 = sensorDataArray[2];
                  newData.thermopile4 = sensorDataArray[3];
                  newData.distance = sensorDataArray[4];
                  newData.pitch = sensorDataArray[5];
                  newData.roll = sensorDataArray[6];
                } else {
                  newData.thermopile1 = false;
                  newData.thermopile2 = false;
                  newData.thermopile3 = false;
                  newData.thermopile4 = false;
                  newData.distance = false;
                  newData.pitch = false;
                  newData.roll = false;
                }
                newData.timestamp = timeStamp;
                newData.ontarget = onTarget;
                newData.question = pilotScriptJsonData[scriptStepCount].message;
                newData.section = pilotScriptJsonData[scriptStepCount].section;
                newData.step = pilotScriptJsonData[scriptStepCount].number;
                newData.hand = activeHand;
                newData.target = activeTarget;

                lastSample = newData;

                batchedData.push(newData);

                if (batchedData.length >= 10) {
                    //send batched data
                    batchedDataSend(batchedData, timeStamp);
                    batchedData = new Array; //empty batch
                }

                //SECOND TIMER FOR DATABASE BATCH WRITES
                //SECOND TIMER FOR DATABASE BATCH WRITES
                var thisTime2 = new Date().getTime();
                var sumTime2 = 0;
                var timeCount2 = 0;
                for(var t=0; t < (lastTimes2.length - 1); t++){
                    lastTimes2[t] = lastTimes2[t+1];
                }
                lastTimes2[lastTimes2.length] = thisTime2;

                if(lastTimes2[0] !== 0){ //if we have enough samples
                    for(var s=0; s < (lastTimes2.length - 1); s++){
                        sumTime2 = sumTime2 + ( lastTimes2[s+1] - lastTimes2[s] );
                        timeCount2++;
                    }
                    speed2 = 1000 / (sumTime2 / timeCount2 );
                    console.log("Data batching speed: " + speed2);
                }
                //END SECOND TIMER FOR DATABASE BATCH WRITES
              }

        }, 200); //200 = 5Hz limit
    }



    /*******************************************************************************************************************
     ******************************************* PILOT STUDY SCRIPT ******************************************************
     ********************************************************************************************************************/

    //Get JSON for pilot script
    var pilotScriptJsonUrl = '../js/tinglePilotAppScript.json';
    // var pilotScriptJsonUrl = 'https://github.com/ChildMindInstitute/matter-website/blob/gh-pages/tingle/tinglePilotAppScript.json?raw=true';

    var pilotScriptJsonData = {};
    $.ajax({
        type: 'GET',
        url: pilotScriptJsonUrl,
        async: false,
        contentType: "application/json",
        dataType: 'json',
        success: function(data) {
            //   alert('success');
            console.log(data);
            pilotScriptJsonData = data;
        },
        error: function(e) {
            //    alert('error');
            console.log(e);

        }
    });

    var scriptStepCount = 1;
    rotateScript(scriptStepCount);
    faceAutoSelect(scriptStepCount);

    $('#script-rotate-right').click(function() {
        if (scriptStepCount < pilotScriptJsonData.length - 2) {
            scriptStepCount++;
            rotateScript(scriptStepCount);
            faceAutoSelect(scriptStepCount);
        }
    });

    $('#script-rotate-left').click(function() {
        if (scriptStepCount > 1) {
            scriptStepCount--;
            rotateScript(scriptStepCount);
            faceAutoSelect(scriptStepCount);
        }
    });

    function rotateScript(currentStepIndex) {
        $("#script-last-step").html(pilotScriptJsonData[currentStepIndex - 1].message);
        $("#this-step-text").html(pilotScriptJsonData[currentStepIndex].message);
        $("#script-next-step").html(pilotScriptJsonData[currentStepIndex + 1].message);
        $("#script-this-step-num").html(scriptStepCount + "/" + (pilotScriptJsonData.length - 2));
    }

    function faceAutoSelect(currentStepIndex) {
    	var currentStepObject = pilotScriptJsonData[currentStepIndex];
    	console.log("currentStepObject: " + currentStepObject);

    	var currentTarget = pilotScriptJsonData[currentStepIndex].target;
    	console.log("currentTarget: " + currentTarget);
    	//make all targets inactive
    	$(".target-selector").removeClass("target-active");


    	$("#selected-targets").html("Target: " + currentTarget);
    	activeTarget = currentTarget;

    }


    //add smoothie.js time series streaming data chart
    // var chartHeight =  $(window).height() / 3;
    var chartHeight = 100;
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


    streamingChart.streamTo(document.getElementById("chart-canvas"), 350 /*delay*/ );
    var lineThermo1 = new TimeSeries();
    var lineThermo2 = new TimeSeries();
    var lineThermo3 = new TimeSeries();
    var lineThermo4 = new TimeSeries();
    var linePitch = new TimeSeries();
    var lineRoll = new TimeSeries();
    var lineProximity = new TimeSeries();
    var lineNN1 = new TimeSeries();
    var lineNN2 = new TimeSeries();
    streamingChart.addTimeSeries(lineThermo1, {
        strokeStyle: 'rgb(133, 87, 35)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineThermo2, {
        strokeStyle: 'rgb(185, 156, 107)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineThermo3, {
        strokeStyle: 'rgb(143, 59, 27)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineThermo4, {
        strokeStyle: 'rgb(213, 117, 0)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(linePitch, {
        strokeStyle: 'rgb(128, 128, 128)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineRoll, {
        strokeStyle: 'rgb(240, 240, 240)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineProximity, {
        strokeStyle: 'rgb(128, 128, 255)',
        lineWidth: 3
    });
    streamingChart.addTimeSeries(lineNN1, {
        strokeStyle: 'rgb(72, 244, 68)',
        lineWidth: 4
    });
    streamingChart.addTimeSeries(lineNN2, {
        strokeStyle: 'rgb(244, 66, 66)',
        lineWidth: 4
    });

    //min/max streaming chart button
    $('#circleDrop').click(function() {

        $('.card-middle').slideToggle();
        $('.close').toggleClass('closeRotate');

        var chartHeight = $(window).height() / 1.2;
        var chartWidth = $(window).width();

        if ($("#chart-size-button").hasClass('closeRotate')) {
            $("#streaming-data-chart").html('<canvas id="chart-canvas" width="' + chartWidth + '" height="' + chartHeight + '"></canvas>');
        } else {
            $("#streaming-data-chart").html('<canvas id="chart-canvas" width="' + chartWidth + '" height="' + 100 + '"></canvas>');
        }

        streamingChart.streamTo(document.getElementById("chart-canvas"), 350 /*delay*/ );

        //hide controls
        $("#basic-interface-container, #hand-head-ui-container, #nn-slide-controls, .console, #interface-controls, #dump-print, #record-controls").toggleClass("hide-for-chart");

    });




    function displayData() {

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

        var batteryDataElement = document.getElementsByClassName('battery-data')[0];
        batteryDataElement.innerHTML = batteryVoltage;

    }

    function getSensorData() {

        if (objectTempData) {
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

        if (ambientTempData) {
            sensorDataArray[10] = ambientTempData.a.toFixed(2);
        }

    } //end code executed after new sensor data

    function collectData() {

        var collectedDataArray = new Array(12).fill(0); //12 device
        collectedDataArray = sensorDataArray;
        //  var positionNumber = $('#master-pose-input').val() - 1;

        console.log("web bluetooth sensor data:");

        console.dir(collectedDataArray);

        //add sample to set
        sensorDataSession.push(collectedDataArray);

        //minimum distance value for true data
        // if( (getSamplesTypeFlag == 1 || getSamplesTypeFlag == 3 ) && collectedDataArray[4] < 100){ collectedDataArray[4] = 100; }

        if (getSamplesTypeFlag == 1) {
            NN1TrueDataArray.push(collectedDataArray);
            $('.message-nn1-true').html(NN1TrueDataArray.length);
        } else if (getSamplesTypeFlag == 2) {
            NN1FalseDataArray.push(collectedDataArray);
            $('.message-nn1-false').html(NN1FalseDataArray.length);
        } else if (getSamplesTypeFlag == 3) {
            NN2TrueDataArray.push(collectedDataArray);
            $('.message-nn2-true').html(NN2TrueDataArray.length);
        } else if (getSamplesTypeFlag == 4) {
            NN2FalseDataArray.push(collectedDataArray);
            $('.message-nn2-false').html(NN2FalseDataArray.length);
        }

        sessionSampleSetIndex.push(numSets);

        console.log("Set Index: ");
        console.dir(sessionSampleSetIndex);

        getSamplesFlag = getSamplesFlag - 1;

        if (getSamplesFlag > 0) {
            //console messages
            var consoleSamples = document.getElementsByClassName('console-samples')[0];
            consoleSamples.innerHTML = sensorDataSession.length;
        }

        if (getSamplesFlag == 0) {
            //console messages
            //    var consoleSamples = document.getElementsByClassName('console-samples')[0];
            //    consoleSamples.innerHTML = sensorDataSession.length;

            var consoleSamples = document.getElementsByClassName('console-sets')[0];
            consoleSamples.innerHTML = numSets;
        }

    }



    /*******************************************************************************************************************
     ************************************** DATA RECORD AND FILE NAMES **************************************************
     ********************************************************************************************************************/

    function updateSampleCountDisplay() {
        $('.message-nn1-true').html(NN1TrueDataArray.length);
        $('.message-nn1-false').html(NN1FalseDataArray.length);
        $('.message-nn2-true').html(NN2TrueDataArray.length);
        $('.message-nn2-false').html(NN2FalseDataArray.length);
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

    function batchedDataSend(batchedData, timeStamp) {
        console.log("");
        // [START single_value_read]
        var userId = firebase.auth().currentUser.uid;
        return firebase.database().ref('/users/' + userId).once('value').then(function(snapshot) {
            var username = (snapshot.val() && snapshot.val().username) || 'Anonymous';
            // [START_EXCLUDE]
            return writeSampleData(firebase.auth().currentUser.uid, username, batchedData, timeStamp);
            // [END_EXCLUDE]
        });
        // [END single_value_read]
    }

    function notesDataSend(timeStamp, notes, lastSample){
        console.log("");
        // [START single_value_read]
        var userId = firebase.auth().currentUser.uid;
        return firebase.database().ref('/users/' + userId).once('value').then(function(snapshot) {
            var username = (snapshot.val() && snapshot.val().username) || 'Anonymous';
            // [START_EXCLUDE]
            return writeNotesData(firebase.auth().currentUser.uid, username, timeStamp, notes, lastSample);
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
            profile_picture: imageUrl
        });
    }
    // [END basic_write]

    function writeSampleData(userId, name, batchedData, timeStamp) {
        console.log("writeSampleData");
        firebase.database().ref('samples/' + userId + "/" + timeStamp).set({
            username: name,
            batchedData: batchedData
        });
    }

    function writeNotesData(userId, name, timeStamp, notes, lastSample) {
        console.log("writeNotesData");
        firebase.database().ref('notes/' + userId + "/" + timeStamp).set({
            username: name,
            notes: notes,
            lastsample: lastSample
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
        //  newSampleForCurrentUser(85, 84, 83, 92, 120, 90, 180);
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




    //$( document ).ready(function() { //on load.
    //window.onload = function(){

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
            $('#sign-in-button').html("Signed in: " + user.displayName.split(" ")[0]);
            newPostForCurrentUser("TEST TITLE", "test message");
            databaseConnected = true;
            // ...
        }).catch(function(error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            // The email of the user's account used.
            var email = error.email;
            // The firebase.auth.AuthCredential type that was used.
            var credential = error.credential;
            databaseConnected = false;
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

    //});

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




    /*******************************************************************************************************************
     **************************************** TARGET SELECTION UI *******************************************************
     ********************************************************************************************************************/


    //handle hand selction toggle button
    $("#hand-btn").click(function() {
        if ($(this).hasClass("left-active")) {
            $(this).removeClass("left-active").addClass("right-active");
            activeHand = "R";

            $("#head-image-container").removeClass("disable-right").addClass("disable-left");

        } else {
            $(this).removeClass("right-active").addClass("left-active");
            activeHand = "L";
            $("#head-image-container").removeClass("disable-left").addClass("disable-right");

        }
    });

    //handle target selection UI
    $(".target-selector").click(function() {
        var newTarget = $(this).attr("target");
        console.log("target selected: " + newTarget);
        $(".target-selector").removeClass("target-active");

        if (newTarget == activeTarget) {
            activeTarget = "none";
        } else {
            activeTarget = newTarget;
            $(this).addClass("target-active");
        }
        $("#selected-targets").html("Target: " + pilotScriptJsonData[currentStepIndex].target);
        $("#selected-targets").attr("target", activeTarget);
    });

    // display target names on hover in target selection UI
    $(".target-selector").hover(function() {
        var displayTarget = $(this).attr("target");
        $("#target-hover-label").html(displayTarget);
        $("#target-hover-label").css("display", "block");
    });
    $(".target-selector").mouseout(function() {
        $("#target-hover-label").css("display", "none");
    });

    // indicate on target when button is pressed
    var scriptTimer = 0;
    function buttonTimer(){
        if(onTarget){
            if(scriptTimer == 0) scriptTimer = new Date().getTime();
            var currentScriptTime = new Date().getTime();
            var displayScriptTime = (currentScriptTime - scriptTimer) / 1000;
            displayScriptTime = displayScriptTime.toFixed(1);
            $("#script-clock").html(displayScriptTime + "s");
        }
    }

    $("#script-this-step").mousedown(function() {
        onTarget = true;

        //   sendDatabaseFlag =  true;
        $("#script-this-step").addClass("on-target");
        $("#script-this-step-toggle").html("ON TARGET");

    }).mouseup(function() {
        onTarget = false;

        scriptTimer = 0;
        $("#script-clock").html(" ");
        //   sendDatabaseFlag = false;
        $("#script-this-step").removeClass("on-target");
        $("#script-this-step-toggle").html("OFF TARGET");
    });




    /*******************************************************************************************************************
     ************************************ DATA RECORD BUTTONS *********************************************
     ********************************************************************************************************************/
    //set flag so data is recorded each time a sample is recieved
    $("#record-btn").click(function() {
        if ($(this).hasClass("active-data-ui")) {
            recordFlag = true;
            $("#record-btn").removeClass("active-data-ui");
            $("#pause-btn").addClass("active-data-ui");
        }
        console.log("Change record flag: " + recordFlag);
    });

    //set flag so data is not recorded each time a sample is recieved
    $("#pause-btn").click(function() {
        if ($(this).hasClass("active-data-ui")) {
            recordFlag = false;
            $("#record-btn").addClass("active-data-ui");
            $("#pause-btn").removeClass("active-data-ui");
        }
        console.log("Change record flag: " + recordFlag);
    });

    $("#submit-notes-btn").click(function() {
        var notes = $("#submit-notes-text").val();
        var noteTime = new Date().getTime();
        notesDataSend(noteTime, notes, lastSample);
        $("#submit-notes-text").html(" ");
        $("#submit-notes-text").val(" ");
        console.log("Notes sent...");
    });

    //Send target configuration for pre-trained neural networks on device
  /*  $('#configure-device').click(function() {
        sendCommandFlag = true;
    }); */

}); // end on document load
//}
