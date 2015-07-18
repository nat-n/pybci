
window.Bci = (window.Bci || {});


// TODO: make scrollspeed depend on time (pixels per second) rather than plot speed


window.Bci.Plotter = (function () {
  'use strict';

  var displayCnvs = document.getElementById('display');
  var displayCtx = displayCnvs.getContext('2d');

  var displayWidth = displayCnvs.width;
  var displayHeight = displayCnvs.height;

  var tapeWidth = displayWidth * 2;
  var tapeHeight = displayHeight;
  var tapeScratchWidth = displayWidth * 2;
  var tapeScratchHeight = displayHeight;

  // var tapeCnvs = document.getElementById('tapeCnvs');
  var tapeCnvs = document.createElement('canvas');
  tapeCnvs.width = tapeWidth;
  tapeCnvs.height = tapeHeight;
  var tapeCtx = tapeCnvs.getContext('2d');

  // var tapeScratchCnvs = document.getElementById('tapeScratchCnvs');
  var tapeScratchCnvs = document.createElement('canvas');
  tapeScratchCnvs.width = tapeScratchWidth;
  tapeScratchCnvs.height = tapeScratchHeight;
  var tapeScratchCtx = tapeScratchCnvs.getContext('2d');

  var animationOn = true;
  var tapeUpdated = false;
  var tapeOffset = 0;

  var pallete = [
    [222, 222, 222],
    [255, 0,   0],
    [255, 255, 0],
    [0,   255, 0],
    [0,   255, 255],
    [0,   0,   255],
    [255, 0,   255],
    [200, 200, 200]
  ];

  var previousSamples = [0, 0, 0, 0, 0, 0, 0, 0];

  function traceFromPrevious(y1, y2, color, pixels) {
    // y1 is the previous point, y2 is the present
    var y, i;
    if (y1 < y2) {
      y1 += 1;
    } else if (y1 > y2) {
      y1 -= 1;
      y = y1;
      y1 = y2;
      y2 = y;
    }
    for (y = y1; y <= y2; y++) {
      i = (displayHeight / 2 - y) * 4;
      pixels.data[i]   = color[0];
      pixels.data[i+1] = color[1];
      pixels.data[i+2] = color[2];
      pixels.data[i+3] = 255;
    }
  }

  function plotSamples(samples) {
    var pixels = new ImageData(1, displayHeight);
    for (var ch = 0; ch < samples.length; ch++) {
      traceFromPrevious(previousSamples[ch], samples[ch], pallete[ch], pixels);
      previousSamples[ch] = samples[ch];
    }
    tapeCtx.putImageData(pixels, tapeOffset, 0);
    tapeUpdated = true;

    tapeOffset += 1;
    scrollTape();
  }

  function updateDisplay() {
    if (!animationOn) return;
    if (tapeUpdated) {
      displayCtx.clearRect(0, 0, displayWidth, displayHeight);
      var copyOffset = Math.max(0, tapeOffset - displayWidth);
      displayCtx.drawImage(tapeCnvs, -copyOffset, 0);
      tapeUpdated = false;
    }
    requestAnimationFrame(updateDisplay);
  }

  function scrollTape() {
    var scrollDelta;
    if (tapeOffset > displayWidth * 1.5) {
      scrollDelta = tapeOffset - displayWidth;
      tapeScratchCtx.clearRect(0, 0, tapeScratchWidth, tapeScratchHeight);
      tapeScratchCtx.drawImage(tapeCnvs, -scrollDelta, 0);
      tapeCtx.clearRect(0, 0, tapeWidth, tapeHeight);
      tapeCtx.drawImage(tapeScratchCnvs, 0, 0);
      tapeOffset = displayWidth;
    }
  }

  function setAnimationOn(on) {
    animationOn = !!on;
    if (animationOn) {
       requestAnimationFrame(updateDisplay);
    }
  }

  setAnimationOn(true);

  return Object.freeze({
    plotSamples: plotSamples,
    setAnimationOn: setAnimationOn
  });
})();
