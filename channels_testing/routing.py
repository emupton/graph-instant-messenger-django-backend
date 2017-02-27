from channels.routing import route
from channels_testing.consumers import ws_connect, ws_disconnect, ws_message
channel_routing = [
    #route("http.request", "channels_testing.consumers.http_consumer"),
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
