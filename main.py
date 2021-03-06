import cgitb
import sys

from gui.CaiHongPiDialog import *
from gui.MainWinUI import *
import input_parser as parser
from loggers import logger
from pdfs import pdfs
from pdfs.modes import ExtractMode, OutputMode

cgitb.enable(format='text')
_VERSION = '0.0.1'


class UnlockWorker(QThread):
    success = pyqtSignal(object)
    fail = pyqtSignal(object)

    def __init__(self, in_file_path):
        super().__init__()
        self._in_file_path = in_file_path

    def run(self) -> None:
        try:
            unlocked = pdfs.prepare_unlock(self._in_file_path)
            self.success.emit(unlocked)
        except:
            self.fail.emit(False)


class PdfWorker(QThread):
    completeSignal = pyqtSignal(object)

    def __init__(self, task):
        super().__init__()
        self._task = task

    def run(self):
        pdfs.extract_to_pdf(**self._task)
        self.completeSignal.emit(True)


class IndicatorTimer(QThread):
    sinOut: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._index = 1;
        self._interruped = False

    def run(self) -> None:
        while not self._interruped:
            self.sinOut.emit(f'{self._index}')
            self._index += 1
            self.sleep(1)

    def interrupt(self):
        self._interruped = True


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('./assets/logo.png'))

        self.actionFileSelect.triggered.connect(self.on_open_to_select_clicked)
        self.actionAboutVersion.triggered.connect(self.on_trigger_about_version)
        self.actionAboutCaiHongPi.triggered.connect(self.on_trigger_about_caihongpi)

        self.btnOpenFile.clicked.connect(self.on_open_to_select_clicked)
        self.radioPages.toggled.connect(self.on_extract_mode_toggled)
        self.radioPageStarts.toggled.connect(self.on_extract_mode_toggled)
        self.radioOddPages.toggled.connect(self.on_extract_mode_toggled)
        self.radioEvenPages.toggled.connect(self.on_extract_mode_toggled)
        self.radioSaveDiff.toggled.connect(self.on_output_mode_toggled)
        self.radioSaveMerge.toggled.connect(self.on_output_mode_toggled)
        self.btnStart.clicked.connect(self.on_start_clicked)
        self.btnOpenOutputPath.clicked.connect(self.on_open_output_path_clicked)
        self.btnOpenOutputDir.clicked.connect(self.on_open_output_dir_clicked)

    def log(self, msg: str):
        self.statusbar.showMessage(msg)
        logger.info(msg)

    def get_extract_mode(self):
        if self.radioPages.isChecked():
            return ExtractMode.Pages
        elif self.radioPageStarts.isChecked():
            return ExtractMode.PageStarts
        elif self.radioOddPages.isChecked():
            return ExtractMode.OddPages
        elif self.radioEvenPages.isChecked():
            return ExtractMode.EvenPages

    def get_output_mode(self):
        if self.radioSaveDiff.isChecked():
            return OutputMode.Diff
        elif self.radioSaveMerge.isChecked():
            return OutputMode.Merge

    def get_page_collections(self):
        if self.radioPages.isChecked():
            return parser.parse_pages(self.editPages.text())
        elif self.radioPageStarts.isChecked():
            return parser.parse_starts(self.editPageStarts.text())
        else:
            return None

    def on_trigger_about_version(self):
        QMessageBox.information(None, '??????', f'????????????{_VERSION}')

    def on_trigger_about_caihongpi(self):
        dialog = CaiHongPiDialog(self)
        dialog.show()

    def on_open_to_select_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "?????? PDF ??????", "C:/", filter="*.pdf")
        self.editOpenedFile.setText(file_path)

    def on_open_output_path_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "???????????????", filter="*.pdf")
        self.editOutputPath.setText(file_path)

    def on_open_output_dir_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, "??????????????????")
        self.editOutputDir.setText(dir_path)

    def on_extract_mode_toggled(self, checked: bool):
        if self.sender() == self.radioPages:
            self.editPages.setEnabled(checked)
        elif self.sender() == self.radioPageStarts:
            self.editPageStarts.setEnabled(checked)

    def on_output_mode_toggled(self, checked: bool):
        if checked:
            if self.sender() == self.radioSaveDiff:
                self.stackedOutout.setCurrentIndex(0)
            elif self.sender() == self.radioSaveMerge:
                self.stackedOutout.setCurrentIndex(1)

    def resetStartAction(self):
        self.lcd_timer.interrupt()
        self.btnStart.setEnabled(True)
        self.btnStart.setText('??????')

    def on_unlocked_successful(self, **kwargs):
        self.log('decrypt:finish...')
        self.log('process:start')
        self.pdfWorker = PdfWorker(kwargs)
        self.pdfWorker.completeSignal.connect(self.on_process_completed)
        self.pdfWorker.start()

    def on_unlocked_fail(self, **kwargs):
        self.resetStartAction()
        QMessageBox.information(None, '??????', '??????[unlock]?????????')

    def on_process_completed(self, result):
        self.resetStartAction()
        if result:
            self.log('process:success...')
            QMessageBox.information(None, '??????', '???????????????')
        else:
            self.log('process:fail...')
            QMessageBox.information(None, '??????', '???????????????')

    def on_timer_tick(self, sec):
        self.btnStart.setText(f'????????????...{sec}')

    def on_start_clicked(self):
        opened_file_path = self.editOpenedFile.text()
        if len(opened_file_path) == 0:
            QMessageBox.information(None, '??????', '??????????????????????????????')
            return

        output_mode = self.get_output_mode()
        output_dir = None
        output_path = None
        if output_mode == OutputMode.Diff:
            output_dir = self.editOutputDir.text()
            if len(output_dir) == 0:
                QMessageBox.information(None, '??????', '????????????????????????')
                return
        elif output_mode == OutputMode.Merge:
            output_path = self.editOutputPath.text()
            if len(output_path) == 0:
                QMessageBox.information(None, '??????', '?????????????????????')
                return

        self.btnStart.setEnabled(False)
        self.lcd_timer = IndicatorTimer()
        self.lcd_timer.sinOut.connect(self.on_timer_tick)
        self.lcd_timer.start()

        extract_mode = self.get_extract_mode()
        page_collections = self.get_page_collections()

        self.unlockWorker = UnlockWorker(opened_file_path)
        self.unlockWorker.success.connect(lambda final_in_file_path: self.on_unlocked_successful(
            in_path=final_in_file_path,
            extract_mode=extract_mode,
            pages=page_collections,
            output_mode=output_mode,
            out_path=output_path,
            out_dir=output_dir))
        self.unlockWorker.fail.connect(self.on_unlocked_fail)
        self.log('decrypt:start...')
        self.unlockWorker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    screen = QDesktopWidget().screenGeometry()
    win.move(int((screen.width() - win.width()) / 2), int((screen.height() - win.height()) / 2))
    win.show()
    sys.exit(app.exec_())
