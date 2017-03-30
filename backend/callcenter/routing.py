from channels.routing import route
from .consumers import ws_add, ws_message, ws_disconnect, send_message

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("send_message", send_message),
]
