import asyncio
from queue import Queue
from threading import Thread
import time
import sys
import backend_gui
import socket_io_client


def gui(sio_in, gui_out):
    app = backend_gui.QApplication(sys.argv)
    ex = backend_gui.SelectionModeWindow(sio_in, gui_out)
    sys.exit(app.exec_())


def socket_io(sio_out, gui_in):
    URL = "http://localhost:8008"
    args = sys.argv
    c = 0
    while c < len(args):
        if args[c] == "--e" or args[c] == "--E":
            URL = args[c + 1]
            c += 1
            print(URL)
        c += 1
    asyncio.run(socket_io_client.start_server(URL, sio_out, gui_in))


# Create the shared queue and launch both threads
q_sio = Queue()
q_gui = Queue()
t1 = Thread(target=socket_io, args=(q_sio, q_gui,))
t2 = Thread(target=gui, args=(q_sio, q_gui,))
t1.start()
t2.start()
