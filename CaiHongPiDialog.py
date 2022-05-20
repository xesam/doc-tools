import PyQt5.QtGui
from CaiHongPi import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CaiHongPiDialog(QDialog, Ui_CaiHongPiDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cai_hong_pi = CaiHongPi()
        self.dialogLayout.addWidget(self.cai_hong_pi)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.cai_hong_pi.unload()
        event.accept()


class CaiHongPi(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.frames = 0
        self.eye_height = 30
        self.mouth_width = 50

        self.simple_frame = SimpleFrame()
        self.simple_frame.signal.connect(self.do_update)
        self.simple_frame.start()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painer = QPainter(self)
        painer.begin(self)
        pen = QPen()
        pen.setWidth(4)
        pen.setStyle(Qt.PenStyle.SolidLine)
        painer.setPen(pen)
        if self.frames >= 0:
            print('第一个眼睛')
            painer.drawLine(150, 100, 150, 100 + min(self.eye_height, int(self.eye_height * self.frames / _FPS)))
        if self.frames >= _FPS:
            print('第二个眼睛')
            painer.drawLine(200, 100, 200, 100 + min(self.eye_height, int(self.eye_height * (self.frames - _FPS) / _FPS)))
        if self.frames >= _FPS * 2:
            print('嘴巴')
            painer.drawLine(150, 180, 150 + min(self.mouth_width, int(self.mouth_width * (self.frames - _FPS * 2) / _FPS)), 180)
        if self.frames >= _FPS * 3:
            print('头')
        if self.frames >= _FPS * 4:
            print('身体')
        if self.frames >= _FPS * 5:
            print('左脚')
        if self.frames >= _FPS * 6:
            print('右脚')
        if self.frames >= _FPS * 7:
            print('左手')
        if self.frames >= _FPS * 8:
            print('右手')
        painer.drawText(100, 100, str(self.frames))
        painer.end()

    def do_update(self):
        self.frames += 1
        self.update()

    def unload(self) -> None:
        self.simple_frame.interrupt()


_FPS = 30


class SimpleFrame(QThread):
    signal = pyqtSignal(object)

    def __init__(self, *args):
        super().__init__(*args)
        self.interrupted = False

    def run(self) -> None:
        while not self.interrupted:
            self.signal.emit(True)
            self.msleep(int(1000 / _FPS))

    def interrupt(self) -> bool:
        self.interrupted = True
