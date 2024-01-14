import json
import os
import shutil
import sys
import time

from PySide2.QtCore import QUrl, Qt, Signal
from PySide2.QtGui import QDesktopServices,QIcon
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtCore import QCoreApplication

data = """
{
    "name":"",
    "java":"",
    "server":"",
    "java_xms":"",
    "java_xmx":"",
    "gui":""
}
"""
data = json.loads(data)

class setup_copyserver(QWidget):
    
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(650,250)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("导入")
        
        self.container = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setTitle("导入服务器")
        self.textedit = QTextEdit(self.groupbox)
        self.textedit.setPlaceholderText("选择服务端文件夹")
        self.textedit.setGeometry(20, 40, 450, 25)
        self.choose_file = QPushButton(self.groupbox)
        self.choose_file.setText("选择文件夹...")
        self.choose_file.setGeometry(500,40,100,25)
        self.choose_file.clicked.connect(self.choose_dir)
        
        self.textedit_jar = QTextEdit(self.groupbox)
        self.textedit_jar.setPlaceholderText("选择服务端主jar文件")
        self.textedit_jar.setGeometry(20, 80, 450, 25)
        self.choose_jar = QPushButton(self.groupbox)
        self.choose_jar.setText("选择文件...")
        self.choose_jar.setGeometry(500,80,100,25)
        self.choose_jar.clicked.connect(self.choose_jar_path)
        
        self.yes = QPushButton(self.groupbox)
        self.yes.setText("确定")
        self.yes.setGeometry(100,150,100,50)
        self.yes.clicked.connect(self.ok)
        
        self.no = QPushButton(self.groupbox)
        self.no.setText("取消")
        self.no.setGeometry(400,150,100,50)
        self.no.clicked.connect(self.cancel)

        self.container.addWidget(self.groupbox)
        self.setLayout(self.container)
        
    def choose_dir(self):
        dir = QFileDialog.getExistingDirectory(self,"选择服务端文件夹","")
        if dir:
            self.textedit.setPlainText(dir)
        else:
            QMessageBox.critical(self,"错误",'路径不能为空')
            
    def choose_jar_path(self):
        if self.textedit.toPlainText():
            file_path = QFileDialog.getOpenFileName(self,"选择Jar服务端",self.textedit.toPlainText(),"Java Jar files (*.jar)")
            if file_path:
                self.textedit_jar.setPlainText(file_path[0].split("/")[-1])
            else:
                QMessageBox.critical(self,"错误",'文件名不可为空')
        else:
            QMessageBox.critical(self,"错误",'请先选择文件夹后再试')
            
    def cancel(self):
        self.close()
        
    def ok(self):
        if self.textedit.toPlainText() == "" or self.textedit_jar.toPlainText() == "":
            QMessageBox.critical(self,"错误",'文件夹或jar名称为空')
        else:
            try:
                self.setCursor(Qt.WaitCursor)
                self.yes.setEnabled(False)
                self.no.setEnabled(False)
                shutil.rmtree(f"server/{data['name']}/")
                shutil.copytree(self.textedit.toPlainText(),f"server/{data['name']}")
                time.sleep(5)
                times = 0
                while True:
                    times += 1
                    time.sleep(1)
                    if os.path.exists(f"server/{data['name']}/{self.textedit_jar.toPlainText()}"):
                        data['server'] = self.textedit_jar.toPlainText()
                        self.setCursor(Qt.ArrowCursor)
                        self.yes.setEnabled(True)
                        self.no.setEnabled(True)
                        self.status.emit("ok")
                        break
                    else:
                        if times == 10:
                            QMessageBox.critical(self,"错误","复制超时或未检测到jar文件")
                            self.yes.setEnabled(True)
                            self.no.setEnabled(True)
                            self.setCursor(Qt.ArrowCursor)
                            shutil.rmtree(f"server/{data['name']}/")
                            os.makedirs(f"server/{data['name']}/")
                            self.close()
                            break
            except Exception as e:
                QMessageBox.critical(self,"ERROR",str(e))

class setup_1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.container = QVBoxLayout()
        self.groupBox = QGroupBox()
        self.groupBox.setTitle("新建服务器名")
        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setPlaceholderText("请输入你要创建的服务器名称，不能有空格和特殊符号")
        self.textEdit.setGeometry(30,30,550,25)
        self.container.addWidget(self.groupBox)
        self.setLayout(self.container)

class setup_2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.container = QVBoxLayout()
        self.groupBox = QGroupBox()
        self.groupBox.setTitle("选择Java环境")

        self.radio1 = QRadioButton(self.groupBox)
        # self.radio1.setChecked(True)
        self.radio1.setText("自动检测Java")
        self.radio1.setGeometry(30,30,200,25)
        self.radio1.toggled.connect(self.auto_java)

        self.radio2 = QRadioButton(self.groupBox)
        self.radio2.setText("手动选择Java路径")
        self.radio2.setGeometry(30,70,200,25)
        self.radio2.toggled.connect(self.java_file)

        self.choose_java = QPushButton(self.groupBox)
        self.choose_java.setText("浏览文件...")
        self.choose_java.setGeometry(30,100,100,25)
        self.choose_java.setEnabled(False)
        self.choose_java.clicked.connect(self.choose_java_file)

        self.show_java = QLabel(self.groupBox)
        self.show_java.setText("Java环境：[未选择]")
        self.show_java.setGeometry(30,150,1000,100)

        self.download_java = QPushButton(self.groupBox)
        self.download_java.setText("下载Java...")
        self.download_java.setGeometry(30,250,200,50)
        self.download_java.clicked.connect(self.down_java)

        self.how_download_java = QPushButton(self.groupBox)
        self.how_download_java.setText("我应该选择什么版本的Java？")
        self.how_download_java.setGeometry(30, 350, 200, 50)
        self.how_download_java.clicked.connect(self.how_down_java)

        self.container.addWidget(self.groupBox)
        self.setLayout(self.container)

    def how_down_java(self):
        os.system("notepad txt/Java版本对照.txt")
    def down_java(self):
        QDesktopServices.openUrl(QUrl("https://www.oracle.com/cn/java/technologies/downloads/"))

    def java_file(self):
        self.choose_java.setEnabled(True)
        self.show_java.setText("Java环境：[未选择]")

    def choose_java_file(self):
        java_path = QFileDialog.getOpenFileName(self,"选择Java主程序","C:","可执行文件 (*.exe)")
        if java_path[0]:
            java_ver = os.popen(f""""{java_path[0]}" -version""").read()
            if "java" in str(java_ver):
                self.show_java.setText(f"Java环境：{java_ver}\nJava路径：{java_path[0]}")
            else:
                QMessageBox.critical(self, "错误", "未检测到Java版本信息")
                self.show_java.setText("Java环境：[未选择]")
        else:
            QMessageBox.critical(self, "错误", "路径不可为空")
            self.show_java.setText("Java环境：[未选择]")

    def auto_java(self):
        self.show_java.setText("Java环境：[未选择]")
        self.choose_java.setEnabled(False)
        java_ver = os.popen("java --version")
        # print(str(java_ver.read()))
        java_output = java_ver.read()
        if "java" in str(java_output):
            self.show_java.setText(f"Java环境：{java_output}")
        else:
            self.show_java.setText(f"Java环境：[未检测到]")

class setup_3(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.container = QVBoxLayout()
        self.groupbox = QGroupBox()
        self.groupbox.setTitle("选择服务端Jar文件")
        self.textedit = QTextEdit(self.groupbox)
        self.textedit.setPlaceholderText("服务端路径")
        self.textedit.setGeometry(20, 40, 450, 25)
        self.choose_file = QPushButton(self.groupbox)
        self.choose_file.setText("选择文件...")
        self.choose_file.setGeometry(500,40,100,25)
        self.choose_file.clicked.connect(self.load_file_path)
        self.text = QLabel(self.groupbox)
        self.text.setGeometry(200,150,500,500)
        
        self.down_server = QPushButton(self.groupbox)
        self.down_server.setText("下载服务端...")
        self.down_server.setGeometry(20,100,100,30)
        self.down_server.clicked.connect(self.down_server_help)
        
        self.copy_server_btn = QPushButton(self.groupbox)
        self.copy_server_btn.setText("导入已有服务器...")
        self.copy_server_btn.setGeometry(20,150,150,30)
        self.copy_server_btn.clicked.connect(self.copy_server)

        self.container.addWidget(self.groupbox)
        self.setLayout(self.container)
        
    def copy_server(self):
        self.cs_window = setup_copyserver()
        self.cs_window.status.connect(self.copy_server_success)
        self.cs_window.show()
        
    def copy_server_success(self,message):
        if message == 'ok':
            self.text.setText("导入成功，单击下一步继续")
            self.choose_file.setEnabled(False)
        
    def down_server_help(self):
        os.system("notepad txt/服务端下载.txt")

    def load_file_path(self):
        file_path = QFileDialog.getOpenFileName(self,"选择Jar服务端","C:","Java Jar files (*.jar)")
        if file_path:
            self.textedit.setPlainText(file_path[0])
        else:
            QMessageBox.critical(self,"错误",'路径不能为空')

class setup_4(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        
        self.container.addWidget(self.groupbox)
        self.setLayout(self.container)

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


class create_server_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))

    def initUI(self):
        self.setWindowTitle("创建服务器")
        self.resize(650, 550)
        
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)  
        self.setFixedSize(self.width(), self.height())

        self.container = QVBoxLayout()

        self.stack = QStackedWidget()
        window1 = setup_1()
        window2 = setup_2()
        window3 = setup_3()
        window4 = setup_4()
        self.stack.addWidget(window1)
        self.stack.addWidget(window2)
        self.stack.addWidget(window3)
        self.stack.addWidget(window4)
        self.stack.setCurrentIndex(0)
        self.container.addWidget(self.stack)

        self.next_setup = QPushButton()
        self.next_setup.setText("下一步")
        self.next_setup.clicked.connect(self.on_next_setup)

        self.close_window = QPushButton()
        self.close_window.setText("取消")
        self.close_window.clicked.connect(self.close_win)

        self.container.addWidget(self.next_setup)
        self.container.addWidget(self.close_window)

        self.setLayout(self.container)

    def on_next_setup(self):
        global data

        current_widget = self.stack.currentWidget()
        stack_name = type(current_widget).__name__

        if stack_name == "setup_1":
            server_name = current_widget.textEdit.toPlainText()
            if server_name == "" or " " in server_name:
                QMessageBox.warning(self, '警告', '输入名称为空或含有非法字符，请重试', QMessageBox.Ok)
            else:
                if os.path.exists(f"server/{server_name}"):
                    QMessageBox.warning(self, '警告', '你要创建的服务器名称已存在，请重新输入', QMessageBox.Ok)
                else:
                    try:
                        os.mkdir(f"server/{server_name}")
                        data["name"] = server_name
                        self.stack.setCurrentIndex(1)
                    except Exception as e:
                        QMessageBox.critical(self, 'ERROR', str(e) ,QMessageBox.Ok)
                        # print(e)
        elif stack_name == "setup_2":
            java_status = current_widget.show_java.text()
            if "未选择" in java_status or "未检测到" in java_status:
                QMessageBox.warning(self, '警告','请选择Java环境')
            else:
                auto_check = current_widget.radio1.isChecked()
                if auto_check == True:
                    data["java"] = "auto"
                else:
                    java_path = str(java_status).split("路径：")[1]
                    data["java"] = java_path
                self.stack.setCurrentIndex(2)
        elif stack_name == "setup_3":
            if current_widget.text.text() == '':
                self.next_setup.setEnabled(False)
                self.close_window.setEnabled(False)
                server_jar_path = current_widget.textedit.toPlainText()
                server_jar_name = server_jar_path.split("/")[-1]
                current_widget.text.setText("正在复制jar文件中，请稍后...")
                QCoreApplication.processEvents() 
                time.sleep(1)
                try:
                    shutil.copy(server_jar_path,f"./server/{data['name']}/")
                    data["server"] = server_jar_name
                    while not os.path.exists(f"./server/{data['name']}/"):
                        time.sleep(3)
                    current_widget.text.setText("复制成功！")
                    QCoreApplication.processEvents()
                    time.sleep(1)
                    self.stack.setCurrentIndex(3)
                    self.next_setup.setEnabled(True)
                    self.close_window.setEnabled(True)
                    self.next_setup.setText("完成")
                except Exception as e:
                    QMessageBox.critical(self, 'ERROR',str(e))
                    self.next_setup.setEnabled(True)
                    self.close_window.setEnabled(True)
                    current_widget.text.setText("")
            else:
                self.stack.setCurrentIndex(3)
                self.next_setup.setText("完成")
        elif stack_name == "setup_4":
            # print(current_widget.auto_java_xm.isChecked())
            mc_gui = current_widget.mcgui.isChecked()
            data['gui'] = mc_gui
            if current_widget.auto_java_xm.isChecked() == True:
                data['java_xms'] = "auto"
                data['java_xmx'] = "auto"
                try:
                    with open(f"server/{data['name']}/config_m.json","w") as w:
                        json.dump(data,w,indent=4)
                    QMessageBox.information(self,"完成","请通过加载服务器来启动他")
                    self.close()
                except Exception as e:
                        QMessageBox.critical(self,"ERROR",str(e))
            else:
                xms = current_widget.text_java_javaxms.toPlainText()
                xmx = current_widget.text_java_javaxmx.toPlainText()
                if xms.isdigit() == True and xmx.isdigit() == True:
                    xms = int(xms)
                    xmx = int(xmx)
                    if xmx > xms:
                        data['java_xms'] = xms
                        data['java_xmx'] = xmx
                        try:
                            with open(f"server/{data['name']}/config_m.json","w") as w:
                                json.dump(data,w,indent=4)
                            self.close()
                            QMessageBox.information(self,"完成","请通过加载服务器来启动他")
                        except Exception as e:
                            QMessageBox.critical(self,"ERROR",str(e))
                    else:
                        QMessageBox.warning(self,"警告","最大内存必须大于最小内存")
                else:
                    QMessageBox.warning(self,"警告","内存设置只能输入数字！")

    def close_win(self):
        global data
        if data["name"] != "":
            shutil.rmtree(f"server/{data['name']}/")
        print(data)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = create_server_window()
    window.show()
    app.exec_()