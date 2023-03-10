from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.responses import Response

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

import uvicorn
import logging
import json
import time


logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory='templates')


class Echo(WebSocketEndpoint):
    encoding = "text"

    print('Entered WebsocketEndpoint')

    async def on_receive(self, websocket, data):
        ws = websocket
        #print('Websocket is :', ws)
        #print('Websocket header is :', ws.headers['sec-websocket-version'])

        datajson = json.loads(data)
        try:
            datajson['expression'] == True
            await websocket.send_json({"expression": datajson['expression']})
        except Exception as e:
            status = 10
            for i in range(10):
                await websocket.send_json({"setAttribute": [{"selector": "#progress-bar", "name": "style", "value": f"width:{status}%"}]})
                status += 10


class Cable(WebSocketEndpoint):
    #encoding = "text"

    #async def on_connect(self, websocket) -> None:
        #print('Connected')
        #print('Websocket is:', websocket.headers)
        #pass

    async def on_receive(self, websocket, data):

        datajson = json.loads(data)
        try:
            datajson['expression'] == True
            await websocket.send_json({"expression": datajson['expression']})
        except Exception as e:
            status = 10
            for i in range(10):
                await websocket.send_json({"setAttribute": [{"selector": "#progress-bar", "name": "style", "value": f"width:{status}%"}]})
                status += 10


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response


middleware = [
    Middleware(CustomHeaderMiddleware),
]

routes = [
    WebSocketRoute("/ws", Echo),
    WebSocketRoute("/cable", Cable),
]

app = Starlette(routes=routes, middleware=middleware)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.route('/')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
