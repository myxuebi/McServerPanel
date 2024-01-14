import signal
import subprocess
import json
import sys
import os
import time
from PySide2.QtCore import Qt,Signal
from PySide2.QtGui import QCloseEvent,QIcon
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QWidget
from threading import Thread

class commTextedit(QTextEdit):
    def __init__(self, mc_cmd_instance):
        super().__init__()
        self.mc_cmd = mc_cmd_instance
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.mc_cmd.send_comm()
        else:
            super().keyPressEvent(event)

class mc_cmd(QWidget):
    
    log_signal = Signal(str)
    mcserver_status = Signal(str)
    comm_info = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
        
    def initUI(self):
        self.resize(800,500)
        self.setWindowTitle("服务器命令行")
        
        self.main_container = QHBoxLayout()
        self.send_comm_container = QHBoxLayout()
        self.text_container = QVBoxLayout()
        self.menu_container = QVBoxLayout()
        
        self.status = QLabel()
        self.status.setText("状态：已停止")
        self.status.setMaximumHeight(25)
        
        self.kong = QLabel()
        
        self.start = QPushButton()
        self.start.setText("启动")
        self.start.clicked.connect(self.start_mc)
        
        self.stop = QPushButton()
        self.stop.setText("停止")
        self.stop.clicked.connect(self.stop_mc)
        
        # self.command_helper = QPushButton()
        # self.command_helper.setText("命令助手")
        # self.command_helper.setEnabled(False)
        
        self.menu_container.addWidget(self.status)
        self.menu_container.addWidget(self.kong)
        self.menu_container.addWidget(self.start)
        self.menu_container.addWidget(self.stop)
        # self.menu_container.addWidget(self.command_helper)
        
        self.cmd_send = commTextedit(self)
        self.cmd_send.setPlaceholderText("输入你要执行的指令")
        self.cmd_send.setMaximumHeight(25)
        
        self.send_btn = QPushButton()
        self.send_btn.setText("执行")
        self.send_btn.setMaximumWidth(100)
        self.send_btn.clicked.connect(self.send_comm)
        
        # self.send_comm_container.addStretch(3)
        self.send_comm_container.addWidget(self.cmd_send)
        # self.send_comm_container.addStretch(1)
        self.send_comm_container.addWidget(self.send_btn)
        
        self.cmd_textview = QTextBrowser()
        
        self.text_container.addWidget(self.cmd_textview)
        self.text_container.addLayout(self.send_comm_container)
        
        # self.main_container.addStretch(1)
        self.main_container.addLayout(self.menu_container)
        # self.main_container.addStretch(4)
        self.main_container.addLayout(self.text_container)
        
        self.setLayout(self.main_container)
        
        self.log_signal.connect(self.log_update)
        self.mcserver_status.connect(self.status_update)
        self.comm_info.connect(self.comm_solve)
    
    def send_comm(self):
        if self.status.text() == "状态：运行中":
            command = self.cmd_send.toPlainText()
            if command:
                self.mcserver.stdin.write(command + '\n')
                self.mcserver.stdin.flush()
                log = str(self.cmd_textview.toPlainText()) + "Input > " + str(command) + "\n"
                self.log_signal.emit(log)
                self.cmd_send.setPlainText("")
    
    def stop_mc(self):
        if self.status.text() == "状态：运行中":
            self.mcserver.stdin.write("stop\n")
            self.mcserver.stdin.flush()
        
    def start_mc(self):
        if self.status.text() == "状态：已停止":
            try:
                with open("tmp/load","r") as r:
                    self.path = r.read()
                with open(f"server/{self.path}/config_m.json","r") as r:
                    file = r.read()
                config = json.loads(file)
            except FileNotFoundError:
                QMessageBox.critical(self,"找不到文件",f"找不到名为{self.path}的服务器")
            except Exception as e:
                QMessageBox.critical(self,"ERROR",str(e))
            
            for i,j in config.items():
                if i != 'name' and i != 'java' and i != 'server' and i != 'java_xms' and i != 'java_xmx' and i != 'gui':
                    QMessageBox.critical(self,"ERROR","配置文件读取错误")
                if j == "":
                    QMessageBox.critical(self,"ERROR","配置文件读取错误")
    
            start_shell = []
            # start_shell.append("cmd.exe")
            # start_shell.append("/c")
            if config['java'] == "auto":
                start_shell.append("java")
            else:
                start_shell.append(config['java'])
            if config['java_xms'] != "auto":
                start_shell.append(f'-Xms{config["java_xms"]}m')
            if config['java_xmx'] != "auto":
                start_shell.append(f'-Xmx{config["java_xmx"]}m')
            start_shell.append("-jar")
            # start_shell.append(f"""'server\{(path)}\{config["server"]}'""")
            start_shell.append(config['server'])
            if config['gui'] == False:
                start_shell.append("nogui")
            
            os.chdir(f"server/{self.path}")
            self.mcserver = subprocess.Popen(start_shell,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    text=True,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            log_output_t = Thread(target=self.log_output)
            log_output_t.start()
            self.status.setText("状态：运行中")
            status_t = Thread(target=self.status_mcserver)
            status_t.start()
        
    def log_output(self):
        while True:
            output = self.mcserver.stdout.readline()
            # print(output)
            if not output:
                break
            if "You need to agree to the EULA in order to run the server" in str(output):
                # self.comm_solve("eula_false")
                self.comm_info.emit("eula_false")
            log = str(self.cmd_textview.toPlainText()) + str(output)
            # self.cmd_textview.setText(log)
            self.log_signal.emit(log)
            
    def comm_solve(self,command):
        if command == "eula_false":
            eula = QMessageBox()
            eula.setWindowTitle("提示")
            eula.setText("你尚未同意协议（https://aka.ms/MinecraftEULA）需要同意后服务器才能继续运行，是否同意？\n PS:同意后需手动启动服务器")
            eula.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            btny = eula.button(QMessageBox.Yes)
            btny.setText("同意")
            btnn = eula.button(QMessageBox.No)
            btnn.setText("不同意")
            eula.exec_()
            if eula.clickedButton() == btny:
                try:
                    with open(f"server/{self.path}/eula.txt",'w') as w:
                        w.write("eula=true")
                except Exception as e:
                    QMessageBox.critical(self,"ERROR",str(e))
            
    def status_mcserver(self):
        self.pid = self.mcserver.pid
        while True:
            time.sleep(1)
            # return_code = self.mcserver.returncode
            # print(return_code)
            # if return_code is not None:
            #     os.chdir("../../")
            #     self.mcserver_status.emit("状态：已停止")
            #     break
            res = subprocess.call(f"tasklist | findstr {self.pid}",shell=True)
            if res == 1:
                # print("stop")
                self.mcserver_status.emit("状态：已停止")
                os.chdir("../../")
                break
            
    def status_update(self,message):
        self.status.setText(message)
            
    def log_update(self,message):
        self.cmd_textview.setText(message)
        self.cmd_textview.moveCursor(self.cmd_textview.textCursor().End)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        # self.mcserver.kill()
        # print(sys.getwindowsversion())
        # os.system(f"taskkill /f /pid {self.mcserver.pid}")
        res = os.system(f"tasklist | findstr {self.pid}")
        if res == 0:
                # print("stop")
                self.mcserver.stdin.write("stop\n")
                self.mcserver.stdin.flush()
                os.kill(self.pid,signal.SIGILL)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mc_cmd()
    win.show()
    app.exec_()