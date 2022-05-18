import sys

from MainWin import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnOpenFile.clicked.connect(self.openFile)

    # @pyqtSlot
    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选取 PDF 文件", "C:/")
        print(file_path)
        self.editOpenedFile.setText(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec_())
