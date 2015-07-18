from os import path
from tornado import web, ioloop
from tornado.options import options, define
from .dashboard import Dashboard
from .websockets import WebSocketHandler, Links


DIRECTORY_ROOT = path.dirname(__file__)
TEMPLATE_PATH = path.abspath(path.join(DIRECTORY_ROOT, '../../client/templates/'))

routes = []

class WebService(web.Application):
    def __init__(self):

        web.Application.__init__(self,
                                 routes,
                                 template_path=TEMPLATE_PATH)


def create(port=8910, dashboard=True):
    routes.append((r'/channels', WebSocketHandler))

    if dashboard:
        routes.append((r'/(.*)', Dashboard))

    app = web.Application(routes)

    def start_server():
        app.listen(port)
        ioloop.IOLoop.instance().start()

    return start_server
