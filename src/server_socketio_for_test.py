import asyncio
import json
import sys
from pprint import pprint

import aioconsole

from aiohttp import web

import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


async def background_task():
    stdin, stdout = await aioconsole.get_standard_streams()
    async for line in stdin:
        stdout.write(line)
        print(str(line).replace("b'", "").replace("'", "").replace("\\n", "").split())
        commands = str(line).replace("b'", "").replace("'", "").replace("\\n", "").split()
        if commands[0] == "start_selector":
            await sio.emit('run_start_selector', {'command': "start_selector"})
        elif commands[0] == "stop":
            await sio.emit('stop_robot', {})


@sio.event
async def info(sid, message):
    pprint(json.loads(message))



@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

    await sio.emit('set_backend', {"backend": "uia", "uuid": sid})


@sio.event
def disconnect(sid):
    print("========================")
    print('Client disconnected:', sid)


# app.router.add_static('/static', 'static')
# app.router.add_get('/', index)


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app, port=8008)
