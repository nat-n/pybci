from tornado import websocket
import json


Links = {
    "clients": [],
    "pipeline_node": None
}

class WebSocketHandler(websocket.WebSocketHandler):
    """
    - sending and recieving of config
    - sending of channel_data
    - sending processed data
    """

    def open(self):
        if self not in Links["clients"]:
            Links["clients"].append(self)

    def on_message(self, message):
        if Links["pipeline_node"] is not None:
            data = json.loads(message)
            Links["pipeline_node"]._on_message(data)

    def on_close(self):
        if self in Links["clients"]:
            Links["clients"].remove(self)
