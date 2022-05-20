import cgitb
import sys

from MainWin import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui import parser
from pdfs import pdfs
from pdfs.modes import ExtractMode, OutputMode

cgitb.enable(format='text')


class UnlockWorker(QThread):
    unlockSignal = pyqtSignal(str)

    def __init__(self, in_file_path):
        super().__init__()
        self._in_file_path = in_file_path

    def run(self) -> None:
        print('start')
        unlocked = pdfs.prepare_unlock(self._in_file_path)
        self.unlockSignal.emit(unlocked)


class PdfWorker(QThread):
    resultSignal = pyqtSignal(object)

    def __init__(self, in_file_path):
        super().__init__()
        self._in_file_path = in_file_path

    def run(self):
        pdfs.extract_to_pdf(self._in_file_path,
                            extract_mode=extract_mode,
                            pages=page_collections,
                            output_mode=output_mode,
                            out_path=output_path,
                            out_dir=output_dir)
        self.resultSignal.emit(True)


class LcdTimer(QThread):
    sinOut: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._index = 1;

    def run(self) -> None:
        while (True):
            self.sinOut.emit(f'{self._index}')
            self._index += 1
            self.sleep(1)


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('./assets/logo.png'))

        self.actionFileSelect.triggered.connect(self.on_open_to_select_clicked)
        self.actionAboutVersion.triggered.connect(self.on_trigger_about_version)

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

        self.lcd_timer = LcdTimer()
        self.lcd_timer.sinOut.connect(self.on_lcd_tick)
        self.lcd_timer.start()

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
        QMessageBox.information(None, '关于', '版本号：0.0.1')

    def on_open_to_select_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选取 PDF 文件", "C:/", "*.pdf")
        self.editOpenedFile.setText(file_path)

    def on_open_output_path_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存为文件", filter="*.pdf")
        self.editOutputPath.setText(file_path)

    def on_open_output_dir_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, "保存到文件夹")
        self.editOutputDir.setText(dir_path)

    def on_extract_mode_toggled(self, checked: bool):
        print(self.sender().text(), checked)
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

    def on_unlocked_successful(self, file_path):
        print(file_path)
        pass

    def on_process_completed(self, result):
        if result:
            QMessageBox.information(None, '提示', '操作成功！')
        else:
            QMessageBox.information(None, '提示', '操作失败！')

    def on_lcd_tick(self, sec):
        self.lcdRunning.display(sec)

    def on_start_clicked(self):
        opened_file_path = self.editOpenedFile.text()
        if len(opened_file_path) == 0:
            QMessageBox.information(None, '提示', '请先选择要处理的文件')
            return

        output_mode = self.get_output_mode()
        output_dir = None
        output_path = None
        if output_mode == OutputMode.Diff:
            output_dir = self.editOutputDir.text()
            if len(output_dir) == 0:
                QMessageBox.information(None, '提示', '请选择输出文件夹')
                return
        elif output_mode == OutputMode.Merge:
            output_path = self.editOutputPath.text()
            if len(output_path) == 0:
                QMessageBox.information(None, '提示', '请选择输出文件')
                return

        extract_mode = self.get_extract_mode()
        page_collections = self.get_page_collections()

        self.unlockWorker = UnlockWorker(opened_file_path)
        self.unlockWorker.unlockSignal.connect(self.on_unlocked_successful)
        self.unlockWorker.start()

        self.pdfWorker = PdfWorker(opened_file_path)
        self.pdfWorker.resultSignal.connect(self.on_process_successful)
        self.pdfWorker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    screen = QDesktopWidget().screenGeometry()
    win.move(int((screen.width() - win.width()) / 2), int((screen.height() - win.height()) / 2))
    win.show()
    sys.exit(app.exec_())
