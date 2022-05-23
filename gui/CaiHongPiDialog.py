from gui.CaiHongPiUI import *
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
        self.eye_height = 50
        self.mouth_width = 50

        self.simple_frame = SimpleFrame()
        self.simple_frame.signal.connect(self.do_update)
        self.simple_frame.start()

    def animDrawLine(self, _from, to, percent, painer):
        from_x, from_y = _from
        to_x, to_y = to
        max_delta_x = to_x - from_x
        max_delta_y = to_y - from_y

        current_x = from_x + int(max_delta_x * min(1, percent))
        current_y = from_y + int(max_delta_y * min(1, percent))
        painer.drawLine(from_x, from_y, current_x, current_y)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painer = QPainter(self)
        painer.begin(self)
        pen = QPen()
        pen.setWidth(4)
        pen.setStyle(Qt.PenStyle.SolidLine)
        painer.setPen(pen)
        if self.frames >= 0:
            stage_percent = (self.frames - _FPS * 0) / _FPS
            self.animDrawLine((100, 75), (100, 125), stage_percent, painer)
        if self.frames >= _FPS:
            stage_percent = (self.frames - _FPS * 1) / _FPS
            self.animDrawLine((150, 75), (150, 125), stage_percent, painer)
        if self.frames >= _FPS * 2:
            stage_percent = (self.frames - _FPS * 2) / _FPS
            self.animDrawLine((100, 150), (150, 150), stage_percent, painer)
        if self.frames >= _FPS * 3:
            stage_frames = self.frames - _FPS * 3
            stage_percent = (self.frames - _FPS * 1) / _FPS
            degrees = min(360, stage_frames / _FPS * 360)
            painer.drawArc(QRect(50, 30, 150, 150), 0, degrees * 16)
        if self.frames >= _FPS * 4:
            stage_percent = (self.frames - _FPS * 4) / _FPS
            self.animDrawLine((125, 180), (125, 280), stage_percent, painer)
        if self.frames >= _FPS * 5:
            stage_percent = (self.frames - _FPS * 5) / _FPS
            self.animDrawLine((125, 280), (50, 380), stage_percent, painer)
        if self.frames >= _FPS * 6:
            stage_percent = (self.frames - _FPS * 6) / _FPS
            self.animDrawLine((125, 280), (200, 280), stage_percent, painer)
        if self.frames >= _FPS * 7:
            stage_percent = (self.frames - _FPS * 7) / _FPS
            self.animDrawLine((200, 280), (200, 380), stage_percent, painer)
        if self.frames >= _FPS * 8:
            stage_percent = (self.frames - _FPS * 8) / _FPS
            self.animDrawLine((125, 220), (240, 220), stage_percent, painer)
        if self.frames >= _FPS * 9:
            stage_percent = (self.frames - _FPS * 9) / _FPS
            self.animDrawLine((240, 220), (240, 200), stage_percent, painer)
        if self.frames >= _FPS * 10:
            stage_percent = (self.frames - _FPS * 10) / _FPS
            self.animDrawLine((125, 240), (240, 240), stage_percent, painer)
        if self.frames >= _FPS * 11:
            stage_percent = (self.frames - _FPS * 11) / _FPS
            self.animDrawLine((240, 240), (240, 260), stage_percent, painer)
        if self.frames >= _FPS * 12:
            stage_percent = (self.frames - _FPS * 12) / _FPS
            lovePath = QPainterPath()
            lovePathA1 = QPoint(280, 200)
            lovePathA2 = QPoint(350, 200)
            lovePathA3 = QPoint(420, 200)
            lovePathA4 = QPoint(350, 310)

            lovePath.moveTo(lovePathA2)
            lovePath.cubicTo(lovePathA2, QPoint(315, 150), lovePathA1)
            lovePath.cubicTo(lovePathA1, QPoint(250, 250), lovePathA4)
            lovePath.moveTo(lovePathA2)
            lovePath.cubicTo(lovePathA2, QPoint(385, 150), lovePathA3)
            lovePath.cubicTo(lovePathA3, QPoint(450, 250), lovePathA4)

            brush = QBrush(Qt.SolidPattern)
            color = QColor(255, 0, 0, int(255 * min(1, stage_percent)))
            brush.setColor(color)
            painer.fillPath(lovePath, brush)
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
            self.msleep(int(500 / _FPS))

    def interrupt(self) -> bool:
        self.interrupted = True
