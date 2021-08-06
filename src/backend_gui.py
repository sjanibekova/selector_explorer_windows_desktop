import sys
import threading
from pynput import mouse
from PyQt5.QtWidgets import (QWidget, QDesktopWidget,
                             QToolTip, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class MousePopupWindow(QWidget):
    def __init__(self, title="", message=""):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.85)

        self.mouseMoveListenerThread = None
        self.titleLabel = self.createLabel(title, 16)
        self.messageLabel = self.createLabel(message, 14)

        self.initUI()
        self.initUIStyles()

    # method for creating a label instance
    def createLabel(self, text="Label", fontSize=14):
        label = QLabel(text)
        label.setFont(QFont('Roboto', fontSize))
        label.setAlignment(Qt.AlignCenter)

        return label

    def mouseMoveListener(self):

        def on_move(x, y):
            size = self.sizeHint()
            width = size.width()
            height = size.height()

            fx = (x - width)
            fy = (y - height)

            dx = 0
            dy = 0

            if fx <= 0 and fy >= 0:
                dx = x + 15
                dy = y - (height + 5)
            if fy <= 0 and fx >= 0:
                dx = x - (width + 5)
                dy = y + 15
            if fx <= 0 and fy <= 0:
                dx = x + 15
                dy = y + 15
            if fx >= 0 and fy >= 0:
                dx = x - (width + 5)
                dy = y - (height + 5)

            self.move(dx, dy)
            print(x - width, y - height)

        listener = mouse.Listener(on_move=on_move)
        listener.start()

    def updateTitleText(self, title="title"):
        self.titleLabel.setText(title)

    def updateMessageText(self, message="message"):
        self.messageLabel.setText(message)

    # hide and clear title, message
    # you can use it for hide window and clear text data
    def hideAndClear(self):
        self.hide()
        self.updateTitleText("")
        self.updateMessageText("")

    # show and set title, message
    def showAndSetText(self, title, message):
        self.updateTitleText(title)
        self.updateMessageText(message)
        self.show()

    # init window and child ui elements
    def initUI(self):
        self.setWindowTitle('Tooltips')

        layout = QVBoxLayout()

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.messageLabel)

        self.setLayout(layout)

        self.show()

        self.mouseMoveListenerThread = StoppableThread(
            target=self.mouseMoveListener, args=())

        self.mouseMoveListenerThread.start()

    # Init basic styles for window

    def initUIStyles(self):
        QToolTip.setFont(QFont('Roboto', 14))

        self.setToolTip('')
        self.setStyleSheet(
            """QWidget {
                    background: #2F2F3B;
                    opacity: 0.95;
                    border: 1px solid #2F2F3B;
                    border-radius: 4px;
                }

                QLabel {
                    font-family: Roboto;
                    font-style: normal;
                    font-weight: normal;
                    color: #EBEBEB;
                }
                """)


class SelectionModeWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.85)

        self.oldPos = None
        self.selectionMode = "UIA"
        self.buttonsList = [
            self.createButton(
                0, "UIA", "UIA", "UIA mode is suitable for modern programs", self.buttonsCallback),
            self.createButton(
                1, "WIN32", "WIN32", "WIN32 mode is suitable for legacy programs", self.buttonsCallback)
        ]

        self.initUIStyles()
        self.initUI()
        self.centerOnScreen()

        self.popupMouseWindow = MousePopupWindow()

    # method for creating a label instance
    def createLabel(self, text="Label"):
        label = QLabel(text)

        return label

    # method for creating a button instance
    def createButton(self, index, modeId, text="button", tipMessage="tip message", callback=lambda: print("button")):
        btn = QPushButton(text, self)
        btn.setToolTip(tipMessage)
        btn.setCheckable(True)
        btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

        if modeId == self.selectionMode:
            btn.toggle()

        def cbWrapper(self):
            callback(index, modeId)

        btn.clicked.connect(cbWrapper)
        return btn

    # called when the button click event is triggered
    def buttonsCallback(self, index, modeId):
        for idx, button in enumerate(self.buttonsList):
            if idx == index:
                if self.selectionMode != modeId:
                    self.selectionMode = modeId

                if not button.isChecked():
                    button.toggle()
            else:
                if button.isChecked():
                    button.toggle()

    # init window and child ui elements
    def initUI(self):
        self.setWindowTitle('Selection Mode')

        layout = QHBoxLayout()

        layout.addWidget(self.createLabel('Selection Mode:'))

        for idx, button in enumerate(self.buttonsList):
            layout.addWidget(button)

        self.setLayout(layout)

        self.show()

    # called when the mouse button is pressed
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.pos()

    # called when the mouse button is released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None

    # called whenever the mouse moves
    def mouseMoveEvent(self, event):
        if not self.oldPos:
            return
        delta = event.pos() - self.oldPos
        self.move(self.pos() + delta)

    # called when you need to center the window
    def centerOnScreen(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    # called when the mouse cursor hovers over the window
    def enterEvent(self, event):
        self.setWindowOpacity(1)
        self.popupMouseWindow.hide()

    # called when the mouse cursor leaves the window
    def leaveEvent(self, event):
        self.setWindowOpacity(0.85)
        self.popupMouseWindow.show()

    # Init basic styles for window
    def initUIStyles(self):
        QToolTip.setFont(QFont('Roboto', 14))

        self.setToolTip('')
        self.setStyleSheet(
            """QWidget {
                    background: #2F2F3B;
                    opacity: 0.95;
                    border: 1px solid #2F2F3B;
                    border-radius: 4px;
                }

                QToolTip {
                    background: rgba(59, 59, 69, 30%);
                    border: 1px solid rgba(59, 59, 69, 0.3);

                    font-family: Roboto;
                    font-style: normal;
                    font-weight: normal;
                    font-size: 14px;
                    line-height: 21px;

                    color: #EBEBEB;
                }

                QLabel {
                    font-family: Roboto;
                    font-style: normal;
                    font-weight: normal;
                    font-size: 18px;
                    line-height: 21px;
                    color: #EBEBEB;
                }

                QPushButton {
                    background: rgba(59, 59, 69, 30%);
                    border: 1px solid rgba(59, 59, 69, 0.3);
                    border-radius: 4px;

                    font-family: Roboto;
                    font-style: normal;
                    font-weight: normal;
                    font-size: 18px;
                    line-height: 21px;

                    color: #EBEBEB;
                    padding: 10px 28px;
                }

                QPushButton:hover {
                    background: #51515C;
                }

                QPushButton:checked {
                    background: #51515C;
                }
                """)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SelectionModeWindow()
#
#     sys.exit(app.exec_())