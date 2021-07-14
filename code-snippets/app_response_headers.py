from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = Response('Hello, world!', media_type='text/plain')
    await response(scope, receive, send)