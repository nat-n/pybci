
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

  var tapeCnvs = document.createElement('canvas');
  tapeCnvs.width = tapeWidth;
  tapeCnvs.height = tapeHeight;
  var tapeCtx = tapeCnvs.getContext('2d');

  var tapeScratchCnvs = document.createElement('canvas');
  tapeScratchCnvs.width = tapeScratchWidth;
  tapeScratchCnvs.height = tapeScratchHeight;
  var tapeScratchCtx = tapeScratchCnvs.getContext('2d');

  var animationOn = true;
  var tapeUpdated = false;
  var tapeOffset = 0;

  var COLORS = [
    [129, 129, 129],
    [124, 75,  141],
    [54,  87,  158],
    [49,  113, 89],
    [221, 178, 13],
    [253, 94,  52],
    [224, 56,  45],
    [162, 82,  49]
  ];

  var NUM_CHANNELS = 8;
  var previousSamples = new Array(NUM_CHANNELS);
  var zeroPoints = new Array(NUM_CHANNELS);
  for (var i = 0; i < NUM_CHANNELS; i++) {
    previousSamples[i] = 0;
    // Calculate the zeropoint of each channel so they're evenly spaced along
    // the y axis of the canvas.
    zeroPoints[i] = (displayHeight / NUM_CHANNELS + 1 ) * (ch + 1);
  };

  function traceFromPrevious(y1, y2, color, pixels, zeroPoint) {
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
      i = (zeroPoint - y) * 4;
      pixels.data[i]   = color[0];
      pixels.data[i+1] = color[1];
      pixels.data[i+2] = color[2];
      pixels.data[i+3] = 255;
    }
  }

  function plotSamples(samples, scale) {
    var scaled_sample, pixels = new ImageData(1, displayHeight);
    for (var ch = 0; ch < samples.length; ch++) {
      scaled_sample = parseInt(samples[ch] / -90, 10);
      traceFromPrevious(previousSamples[ch], scaled_sample, COLORS[ch], pixels, zeroPoints[ch]);
      previousSamples[ch] = scaled_sample;
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
