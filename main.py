import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from app.window.my_window import MyWindow

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    myWin = QMainWindow()
    myUI = MyWindow()

    myUI.setupUi(myWin)
    myWin.show()
    sys.exit(myApp.exec_())
