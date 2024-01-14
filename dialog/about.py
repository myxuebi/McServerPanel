import sys

from PySide2 import QtCore
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import *

class about_app(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))

    def initUI(self):
        self.setFixedSize(250,150)
        self.setWindowTitle("关于软件")

        self.container = QVBoxLayout()

        self.logo_path = 'image/Conditional_Repeating_Command_Block.gif'
        self.pixmap = QPixmap(self.logo_path)
        self.scaled_pixmap = self.pixmap.scaledToWidth(100)
        self.label_logo = QLabel()
        self.label_logo.setPixmap(self.scaled_pixmap)
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)

        self.label_author = QLabel("作者：@myxuebi")
        self.label_gh = QLabel("Github:myxuebi/McServerPanel")

        self.container.addWidget(self.label_logo)
        self.container.addWidget(self.label_author)
        self.container.addWidget(self.label_gh)
        self.setLayout(self.container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = about_app()
    w.show()
    app.exec_()