import sys
import os
import shutil

from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QShowEvent
from dialog.list.ban_player import ban_player_mange
from dialog.list.ban_ip import ban_ip_mange
from dialog.list.op import op_mange
class manage_server_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
    
    def initUI(self):
        self.setWindowTitle("管理服务器")
        self.resize(400,300)
        
        self.container = QHBoxLayout()
        self.th1 = QWidget()
        self.th1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.th2 = QWidget()
        self.th2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.hcontainer = QVBoxLayout()
        
        self.ban_player = QPushButton()
        self.ban_player.setText("封禁玩家管理")
        self.ban_ip = QPushButton()
        self.ban_ip.setText("封禁IP管理")
        self.op_list = QPushButton()
        self.op_list.setText("OP(管理员)管理")
        self.open_explorer = QPushButton()
        self.open_explorer.setText("在资源管理器中打开")
        self.delete = QPushButton()
        self.delete.setText("删除服务器")
        self.delete.setStyleSheet("QPushButton{color:red;}")
        
        self.ban_player.clicked.connect(self.banp)
        self.ban_ip.clicked.connect(self.bani)
        self.op_list.clicked.connect(self.op)
        self.open_explorer.clicked.connect(self.show_explorer)
        self.delete.clicked.connect(self.del_server)
    
        self.ban_player.setMinimumSize(200,30)
        self.ban_ip.setMinimumSize(200,30)
        self.op_list.setMinimumSize(200,30)
        self.open_explorer.setMinimumSize(200,30)
        self.open_explorer.setMinimumSize(200,30)
        self.delete.setMinimumSize(200,30)
        
        self.hcontainer.addWidget(self.ban_player)
        self.hcontainer.addWidget(self.ban_ip)
        self.hcontainer.addWidget(self.op_list)
        self.hcontainer.addWidget(self.open_explorer)
        self.hcontainer.addWidget(self.delete)
        
        self.container.addWidget(self.th1)
        self.container.addLayout(self.hcontainer)
        self.container.addWidget(self.th2)
        
        self.setLayout(self.container)
        
    def showEvent(self, event: QShowEvent) -> None:
        try:
            with open("tmp/load","r") as r:
                self.path = r.read()
        except FileNotFoundError:
            QMessageBox.critical(self,"找不到文件",f"找不到名为{self.path}的服务器")
            return
        except Exception as e:
            QMessageBox.critical(self,"ERROR",str(e))
            return

    def bani(self):
        self.w = ban_ip_mange()
        self.w.show()

    def banp(self):
        self.w = ban_player_mange()
        self.w.show()

    def op(self):
        self.w = op_mange()
        self.w.show()
        
    def show_explorer(self):
        os.startfile(f'server\/{self.path}\/')
        
    def del_server(self):
        check = QMessageBox.question(self,"删除？","真的要删除吗？找回来可就麻烦咯！",QMessageBox.Yes | QMessageBox.No)
        if check == QMessageBox.Yes:
            try:
                shutil.rmtree(f'server/{self.path}/')
            except FileNotFoundError:
                QMessageBox.critical(self,"找不到文件",f"找不到名为{self.path}的服务器")
            except Exception as e:
                QMessageBox.critical(self,"ERROR",str(e))

    def closeEvent(self, event):
        if self.w:
            self.w.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = manage_server_window()
    win.show()
    app.exec_()