window.Bci = (window.Bci || {});

window.Bci.Ws.connect();

var unlisten = window.Bci.Ws.listen(function (packet) {
  var signalScale = -1/-70;
  Bci.Plotter.plotSamples(packet.channel_data, signalScale);
  verifySampleOrder(packet);
});

var latestOrdinal;
function verifySampleOrder(sample) {
  var newOrdinal = sample.packet_id;
  if (latestOrdinal == 255) {
    latestOrdinal = -1;
  }
  if (latestOrdinal !== undefined && newOrdinal != latestOrdinal + 1) {
    console.log(Date.now(), latestOrdinal, newOrdinal);
  }
  latestOrdinal = newOrdinal;
};
