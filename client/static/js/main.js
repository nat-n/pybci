
window.Bci = (window.Bci || {});


window.Bci.Ws.connect();
var unlisten = window.Bci.Ws.listen(function (packet) {
  Bci.Plotter.plotSamples(packet.channel_data.map(function (x) { return parseInt(x / -900, 10); }));
  // verifySampleOrder(packet);
});

// TODO:
// - server and/or client side, verify sample rate and packet fidelity


var latestOrdinal;
function verifySampleOrder(sample) {
  if (latestOrdinal == 255) {
    latestOrdinal = -1;
  }
  var newOrdinal = sample.ordernal_or_whatever;
  if (newOrdinal != latestOrdinal + 1) {
    console.log(Date.now(), latestOrdinal, newOrdinal);
  }
  latestOrdinal = newOrdinal;
};

// -- * == * -- * == * -- * == * -- * == * -- * == * -- * == * -- * == * -- * ==


// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,1]);}, 0);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,10]);}, 100);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,11]);}, 200);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,12]);}, 300);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,19]);}, 400);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,10]);}, 500);
// setTimeout(function() { window.Bci.Plotter.plotSamples([-101,-10,-1]);}, 600);
// setTimeout(function() { window.Bci.Plotter.plotSamples([101,-10,1]);}, 700);
// setTimeout(function() { window.Bci.Plotter.plotSamples([105,-10,1]);}, 800);
// setTimeout(function() { window.Bci.Plotter.plotSamples([111,-10,1]);}, 900);
// setTimeout(function() { window.Bci.Plotter.plotSamples([11,-10,1]);}, 1000);

