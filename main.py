from PyQt5 import QtCore, QtGui, QtWidgets
from UI.ui import Ui_MainWindow
import find_list


class MainWindow(Ui_MainWindow):
    def __init__(self, w):
        self.ret_list = []
        self.deauth_list = []
        self.white_list = []

        Ui_MainWindow.__init__(self)
        self.setupUi(w)
        self.Listlen.clear()
        self.refresh()
        self.Refresh.clicked.connect(self.refresh)
        self.refresh_deauth()
        self.Refresh_deauth.clicked.connect(self.refresh_deauth)
        self.refresh_white()
        self.DelWhite.clicked.connect(self.del_white)
        self.InputWhite.clicked.connect(self.input_white)

    def refresh(self):
        self.ConnectedTable.clearContents()
        self.ret_list = find_list.refresh()
        self.Listlen.clear()
        self.Listlen.setText(str(len(self.ret_list)) + " connected")

        num_rows = len(self.ret_list)
        num_cols = len(self.ret_list[0])
        self.ConnectedTable.setColumnCount(num_cols)
        self.ConnectedTable.setRowCount(num_rows)

        for row in range(num_rows):
            for column in range(num_cols):
                self.ConnectedTable.setItem(row, column, QtWidgets.QTableWidgetItem((self.ret_list[row][column])))

        self.ConnectedTable.setHorizontalHeaderLabels(["IP address", "MAC address"])

    def refresh_deauth(self):
        self.deauthlen.clear()
        self.Deauthlist.clear()
        self.deauth_list = []
        file = open("./data/deauth.txt", "r")
        line = file.readline().replace("\n", "")
        while line:
            self.deauth_list.append(line.lower())
            line = file.readline().replace("\n", "")
        file.close()
        self.deauth_list=set(self.deauth_list)
        for i in self.deauth_list:
            self.Deauthlist.addItem(i)
        self.deauthlen.setText("Deauthenticate "+str(len(self.deauth_list))+" components")

    def refresh_white(self):
        self.Whitelist.clear()
        self.white_list = []
        file = open("./data/whitelist.txt", "r")
        line = file.readline().replace("\n", "")
        while line:
            self.white_list.append(line.lower())
            line = file.readline().replace("\n", "")
        file.close()
        self.white_list = set(self.white_list)
        for i in self.white_list:
            self.Whitelist.addItem(i.lower())

    def input_white(self):
        input_item = self.Deauthlist.currentItem().text()
        self.deauth_list.remove(input_item)
        file = open("./data/deauth.txt","w")
        for i in self.deauth_list:
            file.write(i + "\n")
        file.close()
        self.refresh_deauth()
        if input_item not in self.white_list:
            file = open("./data/whitelist.txt","a")
            file.write(input_item + "\n")
            file.close()
        self.refresh_white()

    def del_white(self):
        delete_item = self.Whitelist.currentItem().text()
        self.white_list.remove(delete_item)
        file = open("./data/whitelist.txt", "w")
        for i in self.white_list:
            file.write(i + "\n")
        file.close()
        self.refresh_white()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = MainWindow(w)
    w.show()
    sys.exit(app.exec_())
