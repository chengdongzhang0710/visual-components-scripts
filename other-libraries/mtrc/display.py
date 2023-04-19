# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(461, 301)
        self.excel_label = QtWidgets.QLabel(Dialog)
        self.excel_label.setGeometry(QtCore.QRect(20, 40, 131, 21))
        self.excel_label.setTextFormat(QtCore.Qt.AutoText)
        self.excel_label.setObjectName("excel_label")
        self.udf_folder_label = QtWidgets.QLabel(Dialog)
        self.udf_folder_label.setGeometry(QtCore.QRect(20, 70, 131, 21))
        self.udf_folder_label.setObjectName("udf_folder_label")
        self.output_folder_label = QtWidgets.QLabel(Dialog)
        self.output_folder_label.setGeometry(QtCore.QRect(20, 100, 131, 21))
        self.output_folder_label.setObjectName("output_folder_label")
        self.excel_line_edit = QtWidgets.QLineEdit(Dialog)
        self.excel_line_edit.setGeometry(QtCore.QRect(150, 40, 201, 21))
        self.excel_line_edit.setObjectName("excel_line_edit")
        self.udf_folder_line_edit = QtWidgets.QLineEdit(Dialog)
        self.udf_folder_line_edit.setGeometry(QtCore.QRect(150, 70, 201, 21))
        self.udf_folder_line_edit.setObjectName("udf_folder_line_edit")
        self.output_folder_line_edit = QtWidgets.QLineEdit(Dialog)
        self.output_folder_line_edit.setGeometry(QtCore.QRect(150, 100, 201, 21))
        self.output_folder_line_edit.setObjectName("output_folder_line_edit")
        self.excel_add_btn = QtWidgets.QPushButton(Dialog)
        self.excel_add_btn.setGeometry(QtCore.QRect(360, 40, 81, 23))
        self.excel_add_btn.setObjectName("excel_add_btn")
        self.udf_folder_add_btn = QtWidgets.QPushButton(Dialog)
        self.udf_folder_add_btn.setGeometry(QtCore.QRect(360, 70, 81, 23))
        self.udf_folder_add_btn.setObjectName("udf_folder_add_btn")
        self.output_folder_add_btn = QtWidgets.QPushButton(Dialog)
        self.output_folder_add_btn.setGeometry(QtCore.QRect(360, 100, 81, 23))
        self.output_folder_add_btn.setObjectName("output_folder_add_btn")
        self.progress_bar = QtWidgets.QProgressBar(Dialog)
        self.progress_bar.setGeometry(QtCore.QRect(20, 140, 421, 23))
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.task_start_btn = QtWidgets.QPushButton(Dialog)
        self.task_start_btn.setGeometry(QtCore.QRect(270, 260, 81, 23))
        self.task_start_btn.setObjectName("task_start_btn")
        self.task_end_btn = QtWidgets.QPushButton(Dialog)
        self.task_end_btn.setGeometry(QtCore.QRect(360, 260, 81, 23))
        self.task_end_btn.setObjectName("task_end_btn")
        self.information_text_browser = QtWidgets.QTextBrowser(Dialog)
        self.information_text_browser.setGeometry(QtCore.QRect(20, 180, 421, 61))
        self.information_text_browser.setObjectName("information_text_browser")
        self.maintain_mode_label = QtWidgets.QLabel(Dialog)
        self.maintain_mode_label.setGeometry(QtCore.QRect(20, 10, 91, 21))
        self.maintain_mode_label.setObjectName("maintain_mode_label")
        self.maintain_mode_selection = QtWidgets.QComboBox(Dialog)
        self.maintain_mode_selection.setGeometry(QtCore.QRect(110, 10, 91, 22))
        self.maintain_mode_selection.setObjectName("maintain_mode_selection")
        self.information_clear_btn = QtWidgets.QPushButton(Dialog)
        self.information_clear_btn.setGeometry(QtCore.QRect(20, 260, 101, 23))
        self.information_clear_btn.setObjectName("information_clear_btn")

        self.retranslateUi(Dialog)
        self.task_end_btn.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MTRC-UDF库维护小工具"))
        self.excel_label.setText(_translate("Dialog", "UDF信息汇总表的位置："))
        self.udf_folder_label.setText(_translate("Dialog", "UDF原始文件夹的位置："))
        self.output_folder_label.setText(_translate("Dialog", "输出文件夹的位置："))
        self.excel_add_btn.setText(_translate("Dialog", "添加文件"))
        self.udf_folder_add_btn.setText(_translate("Dialog", "添加文件夹"))
        self.output_folder_add_btn.setText(_translate("Dialog", "添加文件夹"))
        self.task_start_btn.setText(_translate("Dialog", "开始"))
        self.task_end_btn.setText(_translate("Dialog", "完成"))
        self.maintain_mode_label.setText(_translate("Dialog", "维护模式选择："))
        self.information_clear_btn.setText(_translate("Dialog", "清空信息"))