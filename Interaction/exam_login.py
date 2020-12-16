"""
    Author: j1193
    Time: 2020/11/26 18:59
"""
# ui文件转为py文件
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 790)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 80, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(260, 80, 271, 41))
        self.username.setObjectName("username")
        self.username.setPlaceholderText('测试。。。')
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 150, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(260, 150, 271, 41))
        self.password.setObjectName("password")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(260, 230, 141, 61))
        self.login.setObjectName("login")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 为登录按钮指定事件
        # clicked：信号，login_met:槽函数
        self.login.clicked.connect(self.login_met)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "用户名："))
        self.pushButton_2.setText(_translate("MainWindow", "密码："))
        self.login.setText(_translate("MainWindow", "登录"))

    def login_met(self):
        """
        登录事件（槽函数）
        :return:
        """
        # 用户名输入框的内容
        username = self.username.text()
        # 密码输入框的内容
        password = self.password.text()

        print("输入的用户名是:", username, "密码是:", password)


class CustomUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CustomUI, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
