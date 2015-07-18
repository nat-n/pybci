window.Bci = (window.Bci || {});

window.Bci.Ws = (function () {
  'use strict';

  var wsEndpoint = 'ws://' + location.host + '/channels';
  var listeners = [];
  var ws;

  function connect() {
    if (ws && (ws.readyState == ws.CONNECTING || ws.readyState == ws.OPEN)) {
      return ws;
    }
    ws = new WebSocket(wsEndpoint);
    function init() {
      ws.onmessage = function(msg){
        var content = JSON.parse(msg.data);
        listeners.forEach(function (listener) { listener(content); });
      };
      ws.send('{"hello": 1}');
    }
    var waitingForConnection = setInterval(function () {
      if (ws.readyState === WebSocket.OPEN) {
        init();
        clearInterval(waitingForConnection);
      }
    }, 10);
    return ws;
  }

  function status() {
    switch (ws.readyState) {
      case ws.CLOSED:
        return "closed";
      case ws.CLOSING:
        return "closing";
      case ws.CONNECTING:
        return "connecting";
      case ws.OPEN:
        return "open";
    }
  }

  function listen(cb) {
    var n = listeners.length;
    listeners.push(cb);
    function unlisten() {
      if (n >= 0) {
        listeners.splice(n, 1);
        n = -1;
      }
    };
    return unlisten;
  }

  return Object.freeze({
    connect: connect,
    status: status,
    listen: listen
  });
})();
