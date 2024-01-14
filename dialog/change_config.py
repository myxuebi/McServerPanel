import sys
import json
import os
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtGui import QCloseEvent, QIcon, QShowEvent

class config_server(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
        
    def initUI(self):
        self.setWindowTitle("配置文件修改帮助")
        
        self.html = QWebEngineView()
        self.html.load("https://minecraft.fandom.com/zh/wiki/Server.properties")
        
        self.container = QVBoxLayout()
        self.container.addWidget(self.html)
        
        self.setLayout(self.container)

class config_m_win(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
        
    def initUI(self):
        self.resize(450, 300) 
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("修改服务端启动配置")
        
        self.container = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setTitle("配置服务端设置")

        self.qlabel_javaxms = QLabel(self.groupbox)
        self.qlabel_javaxms.setText("Javac初始内存设置(单位：MB):")
        self.qlabel_javaxms.setGeometry(20,40,200,20)

        self.text_java_javaxms = QTextEdit(self.groupbox)
        self.text_java_javaxms.setGeometry(300,40,100,25)
        
        self.qlabel_javaxmx = QLabel(self.groupbox)
        self.qlabel_javaxmx.setText("Java最大内存限制(单位：MB):")
        self.qlabel_javaxmx.setGeometry(20,80,200,20)

        self.text_java_javaxmx = QTextEdit(self.groupbox)
        self.text_java_javaxmx.setGeometry(300,80,100,25)

        self.auto_java_xm = QCheckBox(self.groupbox)
        self.auto_java_xm.setText("自动分配内存")
        self.auto_java_xm.setGeometry(20,120,100,25)
        self.auto_java_xm.stateChanged.connect(self.check_auto)

        self.mcgui = QCheckBox(self.groupbox)
        self.mcgui.setText("启用 Minecraft Server Gui 界面（不建议）")
        self.mcgui.setGeometry(20,160,200,25)
        
        self.save = QPushButton(self.groupbox)
        self.save.setText("保存")
        self.save.setGeometry(60,210,100,40)
        self.save.clicked.connect(self.check)
        
        self.cancel = QPushButton(self.groupbox)
        self.cancel.setText("取消")
        self.cancel.setGeometry(270,210,100,40)
        self.cancel.clicked.connect(self.cancel_close)
        
        self.container.addWidget(self.groupbox)
        self.setLayout(self.container)
    
    def cancel_close(self):
        self.close()
        
    def check_auto(self,state):
        if state == 2:
            self.text_java_javaxms.setPlainText("auto")
            self.text_java_javaxmx.setPlainText("auto")
            self.text_java_javaxms.setReadOnly(True)
            self.text_java_javaxmx.setReadOnly(True)
        else:
            self.text_java_javaxms.setPlainText("")
            self.text_java_javaxmx.setPlainText("")
            self.text_java_javaxms.setReadOnly(False)
            self.text_java_javaxmx.setReadOnly(False)
        
    def showEvent(self, event: QShowEvent) -> None:
        try:
            with open("tmp/load","r") as r:
                self.path = r.read()
            with open(f"server/{self.path}/config_m.json","r") as r:
                file = r.read()
            self.data = json.loads(file)
        except FileNotFoundError:
            QMessageBox.critical(self,"找不到文件",f"找不到名为{self.path}的服务器")
            return
        except Exception as e:
            QMessageBox.critical(None,"ERROR",str(e))
            return
        if self.data['java_xms'] == "auto" or self.data['java_xmx'] == "auto":
            self.auto_java_xm.setChecked(True)
        else:
            self.text_java_javaxms.setPlainText(self.data['java_xms'])
            self.text_java_javaxmx.setPlainText(self.data['java_xmx'])
        if self.data['gui'] == True:
            self.mcgui.setChecked(True)
        
    def check(self):
        mc_gui = self.mcgui.isChecked()
        self.data['gui'] = mc_gui
        if self.auto_java_xm.isChecked() == True:
            self.data['java_xms'] = "auto"
            self.data['java_xmx'] = "auto"
            try:
                with open(f"server/{self.data['name']}/config_m.json","w") as w:
                    json.dump(self.data,w,indent=4)
                self.close()
            except Exception as e:
                QMessageBox.critical(None,"ERROR",str(e))
        else:
            xms = self.text_java_javaxms.toPlainText()
            xmx = self.text_java_javaxmx.toPlainText()
            if xms.isdigit() == True and xmx.isdigit() == True:
                xmss = int(xms)
                xmxx = int(xmx)
                if xmxx > xmss:
                    self.data['java_xms'] = xms
                    self.data['java_xmx'] = xmx
                    try:
                        with open(f"server/{self.data['name']}/config_m.json","w") as w:
                            json.dump(self.data,w,indent=4)
                        self.close()
                    except Exception as e:
                        QMessageBox.critical(None,"ERROR",str(e))
                else:
                        QMessageBox.warning(None,"警告","最大内存必须大于最小内存")    
            else:
                QMessageBox.warning(None,"警告","内存设置只能输入数字！")

class change_config_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
        
    def initUI(self):
        self.setWindowTitle("修改配置文件")
        self.resize(400,300)
        
        self.container = QHBoxLayout()
        self.th1 = QWidget()
        self.th1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.th2 = QWidget()
        self.th2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.hcontainer = QVBoxLayout()
        self.change_config_m = QPushButton()
        self.change_config_m.setText("修改启动配置")
        self.change_config_server = QPushButton()
        self.change_config_server.setText("修改服务器配置")
        
        self.change_config_m.clicked.connect(self.cc_m)
        self.change_config_server.clicked.connect(self.cc_server)
        
        self.change_config_m.setMinimumHeight(50)
        self.change_config_server.setMinimumHeight(50)
        
        self.hcontainer.addWidget(self.change_config_m)
        self.hcontainer.addWidget(self.change_config_server)
        
        self.container.addWidget(self.th1)
        self.container.addLayout(self.hcontainer)
        self.container.addWidget(self.th2)
        
        self.setLayout(self.container)
    
    def cc_server(self):
        try:
            with open("tmp/load","r") as r:
                self.path = r.read()
        except FileNotFoundError:
            QMessageBox.critical(self,"找不到文件",f"找不到名为{self.path}的服务器")
            return
        except Exception as e:
            QMessageBox.critical(None,"ERROR",str(e))
            return
        os.popen(f"notepad server/{self.path}/server.properties") 
        self.windoww = config_server()
        self.windoww.show()
    
    def cc_m(self):
        self.window1 = config_m_win()
        self.window1.show()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.window1:
            self.window1.close()
        if self.windoww:
            self.windoww.close()
        
if __name__ == '__main__':
    app =  QApplication(sys.argv)
    win = change_config_window()
    win.show()
    app.exec_()