import asyncio
import sys
import socketio
import tkinter as tk
from main import main
sio = socketio.AsyncClient()
TASK = sio.start_background_task
ROBOT_JSON = {}
ROBOT = None
UUID = None
BACKEND = None


@sio.event
async def connect():
    print('connected to server:', URL)


@sio.event
async def run_start_selector(data):
    if data["command"] == "start_selector":
        TASK(main, {"backend": BACKEND, "sio": sio})

@sio.event
async def set_backend(data):
    global UUID, BACKEND
    UUID = data["uuid"]
    BACKEND = data["backend"]


@sio.event
async def disconnect():
    print('disconnected from server')
    await sio.disconnect()


async def start_server(url):
    await sio.connect(url)
    await sio.wait()


URL = "http://localhost:8008"
if __name__ == '__main__':
    args = sys.argv
    c = 0
    while c < len(args):
        if args[c] == "--e" or args[c] == "--E":
            URL = args[c + 1]
            c += 1
            print(URL)
        # elif args[c] == "--p" or args[c] == "--P":
        #     PATH = args[c + 1]
        #     c += 1
        #     print(PATH)
        c += 1
    asyncio.run(start_server(URL))



# python socketio_start.py --e "http://localhost:8080" --p "E:\SeikoLabs\New platform\Git\PythonRPA_Studio\Core_Agent\rob_structure.json"
# "socketio_start\socketio_start.exe" --e "http://localhost:8080" --p "rob_structure.json"
