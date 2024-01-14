import json
import sys
import time

from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QShowEvent
from PySide2.QtCore import Signal


class ban_ip_add(QWidget):
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))

    def initUI(self):
        self.setWindowTitle("新增封禁IP信息")

        self.container = QVBoxLayout()

        self.hbox_1 = QHBoxLayout()
        self.ip_label = QLabel("IP地址：")
        self.ip_edit = QTextEdit()
        # self.get_uuid_btn = QPushButton("获取玩家UUID...")
        # self.get_uuid_btn.clicked.connect(self.get_uuid)

        self.ip_edit.setMaximumHeight(25)

        self.hbox_1.addWidget(self.ip_label)
        self.hbox_1.addWidget(self.ip_edit)
        # self.hbox_1.addWidget(self.get_uuid_btn)

        # self.hbox_2 = QHBoxLayout()
        # self.uuid_label = QLabel("玩家UUID：")
        # self.uuid_edit = QTextEdit()
        #
        # self.uuid_edit.setMaximumHeight(25)
        #
        # self.hbox_2.addWidget(self.uuid_label)
        # self.hbox_2.addWidget(self.uuid_edit)

        self.hbox_3 = QHBoxLayout()
        self.reason_label = QLabel("封禁原因：")
        self.reason_edit = QTextEdit()

        self.reason_edit.setMaximumHeight(25)

        self.hbox_3.addWidget(self.reason_label)
        self.hbox_3.addWidget(self.reason_edit)

        self.hbox_4 = QHBoxLayout()
        self.cancel = QPushButton("取消")
        self.cancel.clicked.connect(self.close_win)
        self.add = QPushButton("添加")
        self.add.clicked.connect(self.add_ban)

        self.hbox_4.addWidget(self.cancel)
        self.hbox_4.addWidget(self.add)

        self.container.addLayout(self.hbox_1)
        # self.container.addLayout(self.hbox_2)
        self.container.addLayout(self.hbox_3)
        self.container.addLayout(self.hbox_4)
        self.setLayout(self.container)

    def add_ban(self):
        if self.ip_edit.toPlainText() == "":
            QMessageBox.critical(self, "警告", "IP不可为空")
        # elif self.uuid_edit.toPlainText() == "":
        #     QMessageBox.critical(self, "警告", "玩家UUID不可为空")
        else:
            if self.reason_edit.toPlainText() == "":
                reason = "Banned by an operator."
            else:
                reason = self.reason_edit.toPlainText()
            ip = self.ip_edit.toPlainText()
            # uuid = self.uuid_edit.toPlainText()
            timee = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            info = {}
            # info['uuid'] = str(uuid)
            info['ip'] = str(ip)
            info['created'] = str(timee) + " +0800"
            info['source'] = "Server"
            info['expires'] = "forever"
            info['reason'] = str(reason)
            for i in self.ban_list:
                if i['ip'] == info['ip']:
                    QMessageBox.warning(self, "警告", "已有此IP的封禁信息")
                    return
            self.ban_list.append(info)
            try:
                with open(f"server/{self.path}/banned-ips.json", "w") as w:
                    json.dump(self.ban_list, w, indent=2)
                self.status.emit("ok")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "ERROR", str(e))

    def showEvent(self, event):
        try:
            with open("tmp/load", "r") as r:
                self.path = r.read()
        except FileNotFoundError:
            QMessageBox.critical(self, "找不到文件", f"找不到名为{self.path}的服务器")
            return
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
            return
        try:
            with open(f"server/{self.path}/usercache.json", "r") as r:
                self.user_info = r.read()
            self.user_list = json.loads(self.user_info)
        except FileNotFoundError:
            QMessageBox.critical(self, "找不到文件", f"找不到玩家数据")
            return
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
            return
        try:
            with open(f"server/{self.path}/banned-ips.json", "r") as r:
                self.ban_info = r.read()
            self.ban_list = json.loads(self.ban_info)
        except FileNotFoundError:
            QMessageBox.critical(self, "找不到文件", f"找不到IP数据")
            return
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
            return

    # def get_uuid(self):
    #     for i in self.user_list:
    #         if i['name'] == self.name_edit.toPlainText():
    #             self.uuid_edit.setPlainText(i['uuid'])
    #             return
    #
    #     QMessageBox.warning(self, "警告", "未找到该玩家数据")

    def close_win(self):
        self.close()


class ban_ip_mange(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))

    def initUI(self):
        self.setWindowTitle("封禁IP管理")
        self.resize(400, 300)

        self.container = QVBoxLayout()

        self.containerh = QHBoxLayout()
        self.containerv = QVBoxLayout()

        self.infolist = QListWidget()

        self.add = QPushButton()
        self.add.setText("添加")
        self.containerv.addWidget(self.add)
        self.add.clicked.connect(self.btn_add)

        self.delete = QPushButton()
        self.delete.setText("删除")
        self.containerv.addWidget(self.delete)
        self.delete.clicked.connect(self.btn_del)

        self.refresh = QPushButton()
        self.refresh.setText("刷新")
        self.containerv.addWidget(self.refresh)
        self.refresh.clicked.connect(self.btn_refresh)

        self.kong = QLabel()
        self.containerv.addWidget(self.kong)

        self.info = QLabel("PS:需要重启服务器修改才能生效")

        self.containerh.addWidget(self.infolist)
        self.containerh.addLayout(self.containerv)
        self.container.addLayout(self.containerh)
        self.container.addWidget(self.info)
        self.setLayout(self.container)

    def showEvent(self, event):
        try:
            with open("tmp/load", "r") as r:
                self.path = r.read()
        except FileNotFoundError:
            QMessageBox.critical(self, "找不到文件", f"找不到名为{self.path}的服务器")
            return
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
            return
        self.load_ban_list()

    def btn_del(self):
        global del_info
        sel = self.infolist.selectedItems()
        for i in sel:
            info = i.text()
            info1 = str(info).split("“")[1]
            del_info = info1.split("”")[0]
        done_info = []
        for i in self.ban_ip_list:
            if i['ip'] != del_info:
                done_info.append(i)
        try:
            with open(f"server/{self.path}/banned-ips.json", "w") as w:
                json.dump(done_info, w, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
        self.btn_refresh()

    def btn_add(self):
        self.add_win = ban_ip_add()
        self.add_win.status.connect(self.add_refresh)
        self.add_win.show()

    def add_refresh(self):
        self.infolist.clear()
        self.load_ban_list()

    def load_ban_list(self):
        try:
            with open(f"server/{self.path}/banned-ips.json", "r") as r:
                ban_ip_info = r.read()
            self.ban_ip_list = json.loads(ban_ip_info)
        except FileNotFoundError:
            QMessageBox.critical(self, "找不到文件", "无法读取banned-ips.json文件")
            return
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
            return

        for i in self.ban_ip_list:
            info_ip = i['ip']
            # info_uuid = i['uuid']
            info_reason = i['reason']

            info = "玩家ID：“" + info_ip + "”  原因：“" + info_reason + "”"
            self.infolist.addItem(info)

    def btn_refresh(self):
        self.infolist.clear()
        self.load_ban_list()

    def closeEvent(self, event):
        if self.add_win:
            self.add_win.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ban_ip_mange()
    win.show()
    app.exec_()