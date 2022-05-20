from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from openpyxl import load_workbook
from UI import Ui_Form
import pandas as pd
import numpy as np


class Form_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        # TODO
        self.creat_table_show()
        self.ui.searchButton.clicked.connect(self.searchButtonClicked)
        self.ui.addButton.clicked.connect(self.addButtonClicked)
        self.ui.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.ui.reviseButton.clicked.connect(self.reviseButtonClicked)
        self.ui.borrowButton.clicked.connect(self.borrowButtonClicked)

    def searchButtonClicked(self):
        msg = self.ui.lineEdit.text()
        self.ui.text.setText(msg)

    def creat_table_show(self):
        workbook = pd.read_excel("database.xlsx")
        current_rows = workbook.shape[0]
        current_columns = workbook.shape[1]
        header = workbook.columns.values.tolist()
        self.ui.tableWidget.setRowCount(current_rows)
        self.ui.tableWidget.setColumnCount(current_columns)
        self.ui.tableWidget.setHorizontalHeaderLabels(header)

        for i in range(current_rows):
            rows_values = workbook.iloc[[i]]
            rows_values_array = np.array(rows_values)
            rows_values_list = rows_values_array.tolist()[0]
            for j in range(current_columns):
                items_list = rows_values_list[j]
                items = str(items_list)
                newitem = QTableWidgetItem(items)
                newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.tableWidget.setItem(i, j, newitem)

    def addButtonClicked(self):
        rowcount = self.ui.tableWidget.rowCount()
        msg = self.ui.lineEdit.text()
        self.ui.tableWidget.insertRow(rowcount)
        item = QTableWidgetItem(msg)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ui.tableWidget.setItem(rowcount, 0, item)

        book = load_workbook("database.xlsx")  # 載入原有的資料到Workbook
        df = pd.DataFrame({'設備名稱': [msg], '物品種類': [53]})
        # '設備名稱': [], '物品種類': [], '型號': [], '品牌': [], '保管人': [], '財產編號': [], '大櫃位': [], '小櫃位': [], '物品狀態': [], '備註': []
        with pd.ExcelWriter('database.xlsx', engine='openpyxl') as writer:
            writer.book = book  # 讓writer加入原來的workbook
            writer.sheets = {ws.title: ws for ws in book.worksheets}
            df.to_excel(writer, sheet_name='工作表1', index=False, startrow=rowcount+1, header=False)
            # columns = ['設備名稱', '物品種類', '型號', '品牌', '保管人', '財產編號', '大櫃位', '小櫃位', '物品狀態', '備註'], na_rep="空值"

    def deleteButtonClicked(self):
        currentrow = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(currentrow)

        workbook = pd.read_excel("database.xlsx")
        df = workbook.drop(currentrow)
        df.to_excel("database.xlsx", sheet_name='工作表1', index=False)

    def reviseButtonClicked(self):
        currentrow = self.ui.tableWidget.currentRow()
        msg = self.ui.lineEdit.text()
        self.ui.tableWidget.item(currentrow, 0).setText(msg)

        workbook = pd.read_excel("database.xlsx")
        workbook.iloc[currentrow, 0] = msg
        workbook.to_excel("database.xlsx", sheet_name='工作表1', index=False)


