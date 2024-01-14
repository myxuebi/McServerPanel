import sys
import os

from PySide2.QtGui import QShowEvent, QIcon
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal

class load_server_window(QWidget):
    value = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))

    def initUI(self):
        self.resize(300,400)
        
        self.setWindowTitle("加载服务器")
        
        self.container = QVBoxLayout()
        self.load_text = QLabel()
        self.load_text.setText("请选择你要加载的服务器：")
        self.container.addWidget(self.load_text)
        
        self.list = QListWidget()
        self.container.addWidget(self.list)
        
        self.ok = QPushButton()
        self.ok.setText("加载")
        self.container.addWidget(self.ok)
        self.ok.clicked.connect(self.load_server)

        self.setLayout(self.container)
    
    def showEvent(self, event: QShowEvent) -> None:
        all_file = os.listdir("server/")
        for i in all_file:
            if os.path.isdir(f"server/{i}") == True:
                self.list.addItem(i)
        if self.list.count() == 0:
            self.list.addItem(" （未检测到任何服务器） ")
    
    def load_server(self):
        name = self.list.selectedItems()
        for i in name:
            if os.path.isfile(f"server/{i.text()}/config_m.json") == True:
                if i.text() != " （未检测到任何服务器） ":
                    try:
                        with open("tmp/load","w") as w:
                            w.write(i.text())
                        self.value.emit(i.text())
                        self.close()
                    except Exception as e:
                        QMessageBox.critical(self,"ERROR",str(e))
            else:
                QMessageBox.critical(self,"错误","加载配置文件失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = load_server_window()
    win.show()
    app.exec_()