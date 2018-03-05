
  /*******************************************************************************************************************
  ************************************************ MISC SCRIPTS ******************************************************
  ********************************************************************************************************************/

  //document ready is faster than window onload
  $( document ).ready(function() {

    if( $(document).width() > 375){
      //inject Arno youtube video
      $(".youtube-wrapper").html('<iframe width="320" height="240" src="https://www.youtube.com/embed/JpkarDe8HjI" controls="0" modestbranding="1" rel="0" frameborder="0" gesture="media" allow="encrypted-media" allowtransparency="true" allowfullscreen></iframe>');
    } else {
      //inject Arno youtube video
      $(".youtube-wrapper").html('<iframe width="280" height="210" src="https://www.youtube.com/embed/JpkarDe8HjI" controls="0" modestbranding="1" rel="0" frameborder="0" gesture="media" allow="encrypted-media" allowtransparency="true" allowfullscreen></iframe>');
    }

  });


  window.onload = function(){
    //slideshow swiping
    $(".carousel").swipe({
      swipe: function(event, direction, distance, duration, fingerCount, fingerData) {
        if (direction == 'left') $(this).carousel('next');
        if (direction == 'right') $(this).carousel('prev');
      },
      allowPageScroll:"vertical"
    });

    //html5 video
    $("#thermo-device").html('<video id="thermo-vid" class="feature-video" tabindex="0" autobuffer="autobuffer"  playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/thermo_clip.MP4"><source src="assets/vid/thermo_clip.webm" type="video/webm;"></source></source><source src="assets/vid/thermo_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/thermo-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#tingle-device").html('<video id="tingle-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/tingle_clip.MP4"></source><source src="assets/vid/tingle_clip.webm" type="video/webm;" ></source><source src="assets/vid/tingle_clip.ogv" type="video/ogv;" ></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/tingle-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    //$("comparison-study-device")

    $("#bibliometric-study-informatics").html('<video id="biblio-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/biblio_clip.MP4"></source><source src="assets/vid/biblio_clip.webm" type="video/webm;" ></source><source src="assets/vid/biblio_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/bibliometrics-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#questionnaire-study-informatics").html('<video id="questionnaire-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/questionnaire_clip.mp4"></source><source src="assets/vid/questionnaire_clip.webm" type="video/webm;" ></source><source src="assets/vid/questionnaire_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/questionnaire-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#taction-app").html('<video id="taction-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/taction_clip.mp4"></source><source src="assets/vid/taction_clip.webm" type="video/webm;" ></source><source src="assets/vid/taction_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/taction-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#token-tower-app").html('<video id="token-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/token_clip.mp4"></source><source src="assets/vid/token_clip.webm" type="video/webm;" ></source><source src="assets/vid/token_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/token-tower-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#ab2cd-app").html('<video id="ab2cd-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/ab2cd_clip.mp4"></source><source src="assets/vid/ab2cd_clip.webm" type="video/webm;" ></source><source src="assets/vid/ab2cd_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/ab2cd-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');

    $("#hbn-voice-data-voice").html('<video id="voice-vid" class="feature-video" tabindex="0" autobuffer="autobuffer" playsinline="playsinline" preload="preload" muted="muted"><source type="video/mp4;" src="assets/vid/voice_clip.mp4"></source><source src="assets/vid/voice_clip.webm" type="video/webm;" ></source><source src="assets/vid/voice_clip.ogv" type="video/ogv"></source><p>Sorry, your browser does not support the &lt;video&gt; element.</p></video><img src="assets/img/projects/voice-thumbnail.jpg" class="img-responsive img-centered" alt="" style="opacity:0;">');




// Using VisSense DOM visibility monitoring utility
if(document.getElementById('thermo-vid')!=undefined){
    var thermo_device_video = $('#thermo-vid');
  //  var thermo_visibility = VisSense(thermo_device_video[0], { fullyvisible: 0.75 });
    var thermo_visibility = VisSense(thermo_device_video[0], { fullyvisible: 0.85 });

    var thermo_visibility_monitor = thermo_visibility.monitor({
      fullyvisible: function() {
        thermo_device_video[0].play();
      },
      hidden: function() {
        thermo_device_video[0].pause();
      }
    }).start();
}

if(document.getElementById('tingle-vid')!=undefined){
    var tingle_device_video = $('#tingle-vid');
  //  var tingle_visibility = VisSense(tingle_device_video[0], { fullyvisible: 0.75 });
    var tingle_visibility = VisSense(tingle_device_video[0], { fullyvisible: 0.85 });

    var tingle_visibility_monitor = tingle_visibility.monitor({
      fullyvisible: function() {
        tingle_device_video[0].play();
      },
      hidden: function() {
        tingle_device_video[0].pause();
      }
    }).start();
}

if(document.getElementById('biblio-vid')!=undefined){
    var biblio_video = $('#biblio-vid');
    var biblio_visibility = VisSense(biblio_video[0], { fullyvisible: 0.85 });

    var biblio_visibility_monitor = biblio_visibility.monitor({
      fullyvisible: function() {
        biblio_video[0].play();
      },
      hidden: function() {
        biblio_video[0].pause();
      }
    }).start();
}

if(document.getElementById('questionnaire-vid')!=undefined){
    var questionnaire_video = $('#questionnaire-vid');
    var questionnaire_visibility = VisSense(questionnaire_video[0], { fullyvisible: 0.85 });

    var questionnaire_visibility_monitor = questionnaire_visibility.monitor({
      fullyvisible: function() {
        questionnaire_video[0].play();
      },
      hidden: function() {
        questionnaire_video[0].pause();
      }
    }).start();
}

if(document.getElementById('taction-vid')!=undefined){
    var taction_app_video = $('#taction-vid');
    var taction_visibility = VisSense(taction_app_video[0], { fullyvisible: 0.85 });

    var taction_visibility_monitor = taction_visibility.monitor({
      fullyvisible: function() {
        taction_app_video[0].play();
      },
      hidden: function() {
        taction_app_video[0].pause();
      }
    }).start();
}

if(document.getElementById('token-vid')!=undefined){
    var token_app_video = $('#token-vid');
    var token_visibility = VisSense(token_app_video[0], { fullyvisible: 0.85 });

    var token_visibility_monitor = token_visibility.monitor({
      fullyvisible: function() {
        token_app_video[0].play();
      },
      hidden: function() {
        token_app_video[0].pause();
      }
    }).start();
}

if(document.getElementById('ab2cd-vid')!=undefined){
    var ab2cd_app_video = $('#ab2cd-vid');
    var ab2cd_visibility = VisSense(ab2cd_app_video[0], { fullyvisible: 0.85 });

    var ab2cd_visibility_monitor = ab2cd_visibility.monitor({
      fullyvisible: function() {
        ab2cd_app_video[0].play();
      },
      hidden: function() {
        ab2cd_app_video[0].pause();
      }
    }).start();
}

if(document.getElementById('voice-vid')!=undefined){
    var voice_video = $('#voice-vid');
    var voice_visibility = VisSense(voice_video[0], { fullyvisible: 1 });

    var voice_visibility_monitor = voice_visibility.monitor({
      fullyvisible: function() {
        voice_video[0].play();
      },
      hidden: function() {
        voice_video[0].pause();
      }
    }).start();
}

if(document.getElementById('bibliometric-study-vid')!=undefined){
    var biblio_circle_video = $('#bibliometric-study-vid');
    var biblio_circle_visibility = VisSense(biblio_circle_video[0], { fullyvisible: 0.85 });

    var biblio_circle_visibility_monitor = biblio_circle_visibility.monitor({
      fullyvisible: function() {
        biblio_circle_video[0].play();
      },
      hidden: function() {
        biblio_circle_video[0].pause();
      }
    }).start();

  }
}




  /*
    https://github.com/paulirish/matchMedia.js
  */

  window.matchMedia = window.matchMedia || (function( doc ) {

    'use strict';

    var bool,
        docElem = doc.documentElement,
        refNode = docElem.firstElementChild || docElem.firstChild,
        // fakeBody required for <FF4 when executed in <head>
        fakeBody = doc.createElement( 'body' ),
        div = doc.createElement( 'div' );

    div.id = 'mq-test-1';
    div.style.cssText = 'position:absolute;top:-100em';
    fakeBody.style.background = 'none';
    fakeBody.appendChild(div);

    return function (q) {

      div.innerHTML = '&shy;<style media="' + q + '"> #mq-test-1 { width: 42px; }</style>';

      docElem.insertBefore( fakeBody, refNode );
      bool = div.offsetWidth === 42;
      docElem.removeChild( fakeBody );

      return {
        matches: bool,
        media: q
      };

    };

  }( document ));
