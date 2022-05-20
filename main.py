import cgitb
import sys

from MainWin import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.modes import ExtractMode, OutputMode
from pdfs.pages import RangePageCollection, OddPageCollection, EvenPageCollection
from gui import parser
from pdfs import pdfs

cgitb.enable(format='text')


class UnlockWorker(QThread):
    unlockSignal = pyqtSignal(object)

    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        pass

    def start(self, priority=None):
        pass


class PdfWorker(QThread):
    completeSignal = pyqtSignal(object)

    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        pass

    def start(self, priority=None):
        pass


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
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
        elif self.radioOddPages.isChecked():
            return OddPageCollection()
        elif self.radioEvenPages.isChecked():
            return OddPageCollection()

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

    def on_start_clicked(self):

        page_collections = self.get_page_collections()
        print(page_collections)

        opened_file_path = self.editOpenedFile.text()
        if len(opened_file_path) == 0:
            QMessageBox.information(None, '提示', '请先选择要处理的文件')
            return

        output_mode = self.get_output_mode()
        if output_mode == OutputMode.Diff:
            if len(self.editOutputDir.text()) == 0:
                QMessageBox.information(None, '提示', '请选择输出文件夹')
                return
        elif output_mode == OutputMode.Merge:
            if len(self.editOutputPath.text()) == 0:
                QMessageBox.information(None, '提示', '请选择输出文件')
                return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    screen = QDesktopWidget().screenGeometry()
    win.move(int((screen.width() - win.width()) / 2), int((screen.height() - win.height()) / 2))
    win.show()
    sys.exit(app.exec_())
