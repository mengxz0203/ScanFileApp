import os
import subprocess

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QVBoxLayout, QListWidget
from app.utils.utils import get_os, check_file_content, get_file_names
from app.window.main_window import Ui_MainWindow


class MyWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.file_list_widget2 = None
        self.file_list_widget = None
        self.folder_path = None
        self.file_path = None
        self.filter_words = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        # 设置文件列表组件
        layout = QVBoxLayout(self.groupBox)
        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)
        # layout.addStretch()

        layout2 = QVBoxLayout(self.groupBox_2)
        self.file_list_widget2 = QListWidget()
        layout2.addWidget(self.file_list_widget2)
        # layout2.addStretch()

        # 设置按钮功能
        self.pushButton.clicked.connect(self.select_folder)
        self.pushButton_2.clicked.connect(self.refresh_groupboxes)

        # 设置输入后回车搜索
        self.lineEdit.returnPressed.connect(self.pushButton_2.click)
        self.lineEdit_2.returnPressed.connect(self.pushButton_2.click)

        # 设置文件列表点击事件
        self.file_list_widget.itemClicked.connect(self.open_file)
        self.file_list_widget2.itemClicked.connect(self.open_file)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, "选择文件夹")
        self.refresh_groupboxes()

    def open_file(self, item):
        self.file_path = item.data(QtCore.Qt.UserRole)
        if self.file_path and os.path.isfile(self.file_path):
            os_type = get_os()
            if os_type == 'Windows':
                os.startfile(self.file_path)  # 在Windows系统中打开文件，适用于Word、Excel和PDF文件
            elif os_type == 'MacOS':
                subprocess.run(['open', self.file_path])  # 在macOS系统中打开文件，适用于Word、Excel和PDF文件
            else:
                Exception("暂不支持此系统，请联系作者")
                QtWidgets.QMessageBox.information(None, "提示", "暂不支持此系统，请联系作者")

    # 搜索并刷新文件列表状态
    def refresh_groupboxes(self):
        if self.folder_path:
            self.file_list_widget.clear()
            self.file_list_widget2.clear()
            self.filter_words.clear()

            self.filter_words.append(self.lineEdit.text())
            self.filter_words.append(self.lineEdit_2.text())

            file_names = get_file_names(self.folder_path)
            valid_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.txt']
            try:
                for file_name in file_names:
                    _, extension = os.path.splitext(file_name)
                    if extension.lower() in valid_extensions:
                        file_path = os.path.join(self.folder_path, file_name)
                        item = QListWidgetItem(file_name)
                        item.setData(QtCore.Qt.UserRole, file_name)
                        self.file_list_widget.addItem(item)

                        if not check_file_content(file_path, self.filter_words):
                            item = QListWidgetItem(file_name)
                            item.setData(QtCore.Qt.UserRole, file_name)
                            self.file_list_widget2.addItem(item)
            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.information(None, "提示", str(e))
