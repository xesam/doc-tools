import sys
import cgitb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pdfs.modes import ExtractMode, OutputMode
from pdfs.pages import RangePages, parse_fragments
from MainWin import *

cgitb.enable(format='text')


def parse_page(pagination: str):
    pages = [int(i) for i in pagination.split('-')]
    return RangePages(pages[0], pages[-1])


def parse_pages(paginations: str):
    pages = [parse_page(i) for i in paginations.split(',')]
    return pages


def get_starts(paginations: str):
    return [int(i) for i in paginations.split(',')]


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

    def on_open_to_select_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选取 PDF 文件", "C:/")
        self.editOpenedFile.setText(file_path)

    def on_extract_mode_toggled(self, checked: bool):
        print(self.sender().text(), checked)
        if self.sender() == self.radioPages:
            self.editPages.setEnabled(checked)
        elif self.sender() == self.radioPageStarts:
            self.editPageStarts.setEnabled(checked)

    def on_output_mode_toggled(self, checked: bool):
        print(self.sender().text(), checked)

    def on_start_clicked(self):
        print(self.get_extract_mode())
        print(self.editPages.text())
        print(parse_pages(self.editPages.text()))
        print(self.editPageStarts.text())
        print(get_starts(self.editPageStarts.text()))
        print(self.get_output_mode())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    screen = QDesktopWidget().screenGeometry()
    win.move(int((screen.width() - win.width()) / 2), int((screen.height() - win.height()) / 2))
    win.show()
    sys.exit(app.exec_())
