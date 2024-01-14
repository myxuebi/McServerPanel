# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'homejRxsvO.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from dialog.create_server import create_server_window
from dialog.load_server import load_server_window
from dialog.start_server import mc_cmd
from dialog.change_config import change_config_window
from dialog.manage_server import manage_server_window
from dialog.about import about_app
from PySide2.QtCore import Slot

class Ui_MinecraftServerPanel(object):
    def __init__(self):
        self.window = None
    
    def setupUi(self, MinecraftServerPanel):
        if not MinecraftServerPanel.objectName():
            MinecraftServerPanel.setObjectName(u"MinecraftServerPanel")
        MinecraftServerPanel.resize(463, 596)
        MinecraftServerPanel.setMinimumSize(QSize(463, 596))
        MinecraftServerPanel.setMaximumSize(QSize(463, 596))
        MinecraftServerPanel.setWindowIcon(QIcon("image/Conditional_Repeating_Command_Block.gif"))
        self.centralwidget = QWidget(MinecraftServerPanel)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, -1, -1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(10)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 40))
        self.label_2.setFont(font)

        self.horizontalLayout.addWidget(self.label_2, 0, Qt.AlignRight)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(60, 20, 321, 451))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(20, 0, 20, 0)
        self.create_server = QPushButton(self.layoutWidget)
        self.create_server.setObjectName(u"create_server")
        self.create_server.clicked.connect(self.start_createserver_window)

        self.verticalLayout.addWidget(self.create_server)

        self.load_server = QPushButton(self.layoutWidget)
        self.load_server.setObjectName(u"load_server")
        self.load_server.clicked.connect(self.start_loadserver_window)

        self.verticalLayout.addWidget(self.load_server)

        self.status_server = QPushButton(self.layoutWidget)
        self.status_server.setObjectName(u"status_server")
        self.status_server.clicked.connect(self.start_server)

        self.verticalLayout.addWidget(self.status_server)

        self.change_config = QPushButton(self.layoutWidget)
        self.change_config.setObjectName(u"change_config")
        self.change_config.clicked.connect(self.start_change_window)

        self.verticalLayout.addWidget(self.change_config)

        self.server_con = QPushButton(self.layoutWidget)
        self.server_con.setObjectName(u"server_con")
        self.server_con.clicked.connect(self.manage_server)

        self.verticalLayout.addWidget(self.server_con)

        self.about_app = QPushButton(self.layoutWidget)
        self.about_app.setObjectName(u"about_app")
        self.about_app.clicked.connect(self.aboutapp)

        self.verticalLayout.addWidget(self.about_app)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        MinecraftServerPanel.setCentralWidget(self.centralwidget)

        self.retranslateUi(MinecraftServerPanel)

        QMetaObject.connectSlotsByName(MinecraftServerPanel)
    # setupUi

    def aboutapp(self):
        self.aw = about_app()
        self.aw.show()

    def start_change_window(self):
        if self.label_3.text() == "[未选择]":
            QMessageBox.critical(None,"错误","请先加载服务器后再试")
        else:
            self.cw_window = change_config_window()
            self.cw_window.show()

    def start_createserver_window(self):
        self.c_window = create_server_window()
        self.c_window.show()

    def start_loadserver_window(self):
        if "mc_cmd" not in str(self.window):
            self.window = load_server_window()
            self.window.value.connect(self.load_server_n)
            self.window.show()
        else:
            if self.window.isVisible():
                QMessageBox.warning(None,"警告","服务器控制台启动时无法使用此功能")
            else:
                self.window = load_server_window()
                self.window.value.connect(self.load_server_n)
                self.window.show()
        
    def start_server(self):
        if self.label_3.text() == "[未选择]":
            QMessageBox.critical(None,"错误","请先加载服务器后再试")
        else:
            self.window = mc_cmd()
            self.window.show()

    def manage_server(self):
        if self.label_3.text() == "[未选择]":
            QMessageBox.critical(None,"错误","请先加载服务器后再试")
        else:
            self.window1 = manage_server_window()
            self.window1.show()
    @Slot(str)
    def load_server_n(self,value):
        self.label_3.setText(value)

    def retranslateUi(self, MinecraftServerPanel):
        MinecraftServerPanel.setWindowTitle(QCoreApplication.translate("MinecraftServerPanel", u"MinecraftServerPanel", None))
        self.label.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u6b22\u8fce\u4f7f\u7528MSP\u63a7\u5236\u9762\u677f\uff01", None))
        self.label_2.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u5f53\u524d\u670d\u52a1\u5668\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MinecraftServerPanel", u"[\u672a\u9009\u62e9]", None))
        self.groupBox.setTitle(QCoreApplication.translate("MinecraftServerPanel", u"\u63a7\u5236\u9009\u9879", None))
        self.create_server.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u65b0\u5efa/\u5bfc\u5165\u670d\u52a1\u5668", None))
        self.load_server.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u52a0\u8f7d\u670d\u52a1\u5668", None))
        self.status_server.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u542f\u52a8/\u505c\u6b62\u670d\u52a1\u5668", None))
        self.change_config.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u4fee\u6539\u914d\u7f6e\u6587\u4ef6", None))
        self.server_con.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u670d\u52a1\u5668\u7ba1\u7406", None))
        self.about_app.setText(QCoreApplication.translate("MinecraftServerPanel", u"\u5173\u4e8e\u8f6f\u4ef6", None))
    # retranslateUi

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MinecraftServerPanel()
ui.setupUi(window)
window.show()
sys.exit(app.exec_())