import asyncio
import sys

from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from asyncqt import QEventLoop

import socketio


class Client(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error_ocurred = pyqtSignal(object, name="errorOcurred")
    data_changed = pyqtSignal(str, name="dataChanged")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sio.on("connect", self._handle_connect, namespace=None)
        self.sio.on("connect_error", self._handle_connect_error, namespace=None)
        self.sio.on("disconnect", self._handle_disconnect, namespace=None)
        self.sio.on("/client_Unlock", self.client_unlock_ack, namespace=None)

    @property
    def sio(self):
        return socketio.AsyncClient(
            reconnection=True,
            reconnection_attempts=3,
            reconnection_delay=5,
            reconnection_delay_max=5,
            logger=True,
        )

    async def start(self):
        await self.sio.connect(url="http://localhost:8008")

    def _handle_connect(self):
        self.connected.emit()

    def _handle_disconnect(self):
        self.disconnect.emit()

    def _handle_connect_error(self, data):
        self.error_ocurred.emit(data)

    def client_unlock_ack(self, data):
        self.data_changed.emit(data)

    def _set_backend(self, data):
        print('Set backend')


class View(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(alignment=Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.resize(640, 480)

    def update_data(self, message):
        self.label.setText(message)


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    view = View()
    view.show()
    print('VIE')

    client = Client()
    client.data_changed.connect(view.update_data)

    with loop:
        asyncio.ensure_future(client.start(), loop=loop)
        loop.run_forever()


if __name__ == "__main__":
    main()
