import asyncio
import itertools
import json
import logging
import time

import graphene
import uvicorn
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.applications import Starlette
from starlette.background import BackgroundTasks
from starlette.exceptions import HTTPException
from starlette.graphql import GraphQLApp
from starlette.responses import (HTMLResponse, JSONResponse, PlainTextResponse,
                                 RedirectResponse, StreamingResponse)
from starlette.routing import Router
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

logger = logging.getLogger(__name__)

app = Starlette(debug=True, template_directory='templates')
app.mount('/static', app=StaticFiles(directory='static'), name='static')


@app.route('/')
async def homepage(request):
    """$ http :8000"""

    content = {
        'request': request.method,
        'url': repr(request.url),
        'headers': repr(request.headers),
        'query': repr(request.query_params),
        'path': repr(request.path_params),
        'cookies': repr(request.cookies),
        'body': None,
        }
    content['body'] = repr(await request.body())
    return JSONResponse(content)


@app.route('/get/plain_text')
async def get_plain_text(request):
    """$ http :8000/get/plain_text"""

    return PlainTextResponse('spam')


@app.route('/get/json')
async def get_json(request):
    """$ http :8000/get/json"""

    return JSONResponse({'hello': 'world'})


@app.route('/get/use_template')
async def get_use_template(request):
    """$ http :8000/get/use_template"""

    template = app.get_template('use_template.html')
    content = template.render(request=request)
    return HTMLResponse(content)


@app.route('/put', methods=['PUT'])
async def put(request):
    """$ http put :8000/put spam=spamspamspam"""

    content = repr(await request.body())
    response = PlainTextResponse(content)
    return response


@app.route('/put/json', methods=['PUT'])
async def put_json(request):
    """$ http put :8000/put/json spam=spamspamspam"""

    content = await request.json()
    response = JSONResponse(content)
    return response


@app.route('/post/json', methods=['POST'])
async def post_json(request):
    """$ http post :8000/post/json spam=spamspamspam"""

    return await put_json(request)


@app.route('/post/form', methods=['POST'])
async def post_form(request):
    """$ http -f post :8000/post/form spam=spamspamspam"""

    content = await request.form()
    response = PlainTextResponse(repr(content))
    return response


@app.route('/redirect')
async def redirect(request):
    """$ http :8000/redirect"""

    return RedirectResponse(url=request.url_for('get_json'))


async def _slow_add(a, b):
    await asyncio.sleep(1)
    return a + b


async def _slow_sum(nums):
    nums = list(nums)
    yield 'slow sum {}: '.format(repr(nums))

    while len(nums) > 1:
        pair = itertools.zip_longest(*([iter(nums)] * 2), fillvalue=0)
        coroutines = [_slow_add(a, b) for a, b in pair]
        g = asyncio.gather(*coroutines)
        nums = await g
    yield str(nums[0])


@app.route('/async_stream')
async def async_stream(request):
    """$ http :8000/async_stream"""

    return StreamingResponse(_slow_sum(range(10)), media_type='text/plain')


async def _background(value):
    await asyncio.sleep(3)
    logger.info('background task: %s', value)


@app.route('/background')
async def background(request):
    """$ http :8000/background"""

    tasks = BackgroundTasks()
    tasks.add_task(_background, value='spam')
    tasks.add_task(_background, value='ham')
    tasks.add_task(_background, value='eggs')

    return JSONResponse({'background': 'logging'}, background=tasks)


@app.websocket_route('/ws')
async def ws(websocket):
    """$ wsdump.py ws://0.0.0.0:8000/ws"""

    await websocket.accept()
    try:
        while True:
            t = await websocket.receive_text()
            if t == 'close':
                break
            await websocket.send_text(t)
    except WebSocketDisconnect as d:
        if d.code == 1000:
            logger.debug('Disconnected. code %s', d.code)
        else:
            logger.info('Disconnected. code %s', d.code)
    else:
        await websocket.close()


class GraphHello(graphene.ObjectType):
    """GraphQL Application example
    {
      a: hello(name: "a")
      b: hello(name: "b")
      c: hello(name: "c")
      d: hello(name: "d")
      e: hello(name: "e")
      f: helloSync(name: "f")
      g: helloSync(name: "g")
      h: helloSync(name: "h")
    }
    """
    hello = graphene.String(name=graphene.String())
    hello_sync = graphene.String(name=graphene.String())

    async def resolve_hello(self, info, name):
        await asyncio.sleep(1)
        return 'Hello {}'.format(name)

    def resolve_hello_sync(self, info, name):
        time.sleep(1)
        return 'Hello {}'.format(name)


app.add_route('/graphql',
              GraphQLApp(schema=graphene.Schema(query=GraphHello),
                         executor_class=AsyncioExecutor,
                         ),
              )


@app.route('/raise_error')
async def raise_error(request):
    raise ValueError('spam')


@app.route('/raise_http_exception')
async def raise_http_exception(request):
    raise HTTPException(410)


app2 = Router()


@app2.route('/')
async def app2_home(request):
    return PlainTextResponse('app2_home')


app.mount('/app2', app2)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)