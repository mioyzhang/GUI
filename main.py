# -*- coding: utf-8 -*-
import os
import sys
import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication


class Item(QWidget):
    def __init__(self, address='text_label', description='text_label', parent=None):
        super(Item, self).__init__(parent)
        self.verticalLayout = QVBoxLayout()

        self.label_1 = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label_1)

        self.label_2 = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label_2)

        self.textBrowser = QtWidgets.QLineEdit()

        # self.verticalLayout.addWidget(self.textBrowser)

        self.verticalLayout_1 = QHBoxLayout()
        self.verticalLayout_1.addLayout(self.verticalLayout)
        self.verticalLayout_1.addWidget(self.textBrowser)

        self.setLayout(self.verticalLayout_1)

        self.address = address
        self.label_1.setText(address)
        self.label_2.setText(description)

    def refresh(self):
        # self.textBrowser.clear()

        # result = os.popen('pwd')
        # res = result.read()
        # for line in res.splitlines():
        # for line in result.splitlines():
        #     print(line)

        result = os.popen('pwd').read()
        mes = ''.join(result.splitlines())

        self.textBrowser.setText(mes)
        self.textBrowser.hide()
        self.textBrowser.show()


class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)

        host = '202.197.9.2'
        port = 22
        user = 'root'
        password = 'root'

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, port, user, password)

        self.items = []
        line = []
        line.append(Item('0x17000000', '星地LVDS口'))
        line.append(Item('0x17000001', '星地LVDS口'))
        line.append(Item('0x17000002', '星间LVDS口'))
        self.items.append(line)

        line = []
        line.append(Item('0x17000003', '星间LVDS口'))
        line.append(Item('0x17000004', '相机网口'))
        line.append(Item('0x17000005', '相机网口'))
        self.items.append(line)

        line = []
        line.append(Item('0x17000006', '板间网口'))
        line.append(Item('0x17000007', '板间网口'))
        line.append(Item('0x1700001c', '相机LVDS口'))
        self.items.append(line)

        layout = QVBoxLayout()

        for line in self.items:
            lineout = QHBoxLayout()
            for i in line:
                lineout.addWidget(i)
            layout.addLayout(lineout)

        # self.items = []
        # self.items.append(Item('0x17000000', '星地LVDS口'))
        # self.items.append(Item('0x17000001', '星地LVDS口'))
        # self.items.append(Item('0x17000002', '星间LVDS口'))
        # self.items.append(Item('0x17000003', '星间LVDS口'))
        # self.items.append(Item('0x17000004', '相机网口'))
        # self.items.append(Item('0x17000005', '相机网口'))
        # self.items.append(Item('0x17000006', '板间网口'))
        # self.items.append(Item('0x17000007', '板间网口'))
        # self.items.append(Item('0x1700001c', '相机LVDS口'))
        #
        # layout = QVBoxLayout()
        # for i in self.items:
        #     layout.addWidget(i)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setText('Refresh all')
        layout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.refresh_all)

        self.setLayout(layout)

    def refresh_all(self):
        # for i in self.items:
        for line in self.items:
            for i in line:
                # cmd = '/home/debian/readreg eth %s' % i.address
                cmd = 'pwd'
                stdin, stdout, stderr = self.ssh.exec_command(cmd)

                # cmd_result = stdout.read(), stderr.read()
                # mes = ' '.join(cmd_result)

                mes = stdout.read().strip().decode()

                i.textBrowser.setText(mes)
                i.textBrowser.hide()
                i.textBrowser.show()

                # i.refresh()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = WinForm()
    # ex = Item()
    ex.show()
    sys.exit(app.exec_())
