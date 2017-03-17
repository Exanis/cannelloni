# -*- coding: utf8 -*-

"Channels routing"

from channels.routing import route_class
from backend import websocket

channel_routing = [
    route_class(websocket.Handler)
]
