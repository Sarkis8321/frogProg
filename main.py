from PyQt5 import QtWidgets
from d import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import sqlite3

# подключение к базе
conn = sqlite3.connect("data.db")
cursor = conn.cursor()


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.clickSave)
        self.ui.pushButton_2.clicked.connect(self.clickDelete)
        self.renderViewTable()

    def clickSave(self):
        surname = self.ui.lineEdit.text()
        name = self.ui.lineEdit_2.text()
        patr = self.ui.lineEdit_3.text()
        birth = self.ui.dateEdit.text()
        gen = (surname, name, patr, birth)
        cursor.execute("""
            INSERT INTO users(surname, name, patr, birth)
            VALUES(?,?,?,?);
        """, gen)
        conn.commit()
        self.renderViewTable()

    def renderViewTable(self):
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        self.ui.tableWidget.clear()

        self.ui.tableWidget.setColumnCount(5)  # количество столбцов
        self.ui.tableWidget.setRowCount(len(data))  # количество столбцов
        self.ui.tableWidget.setHorizontalHeaderLabels(['id', "Фамилия", "Имя", "Отчество", "Дата рождения"])
        self.ui.tableWidget.setVerticalHeaderLabels([""])
        # подключение функции обработки клика на ячейки таблицы
        # self.ui.tableWidget.cellPressed[int,int].connect(self.clickRowCol)

        for i in range(len(data)):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(data[i][0])))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(data[i][1]))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(data[i][2]))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(data[i][3]))
            self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(data[i][4]))
        self.ui.tableWidget.selectionModel().selectionChanged.connect(self.clickRowCol)

    def clickRowCol(self, r, c):
        SelectItem = {
            'id': '',
            'surname': '',
            'name': '',
            'patr': '',
            'birth': ''
        }
        for item in r.indexes():
            if item.column() != 0:
                pass
        for item in c.indexes():
            if item.column() != 0:
                SelectItem['id'] = self.ui.tableWidget.item(item.row(), 0).text()
                SelectItem['surname'] = self.ui.tableWidget.item(item.row(), 1).text()
                SelectItem['name'] = self.ui.tableWidget.item(item.row(), 2).text()
                SelectItem['patr'] = self.ui.tableWidget.item(item.row(), 3).text()
                SelectItem['birth'] = self.ui.tableWidget.item(item.row(), 4).text()

                cursor.execute("UPDATE users SET surname=?, name=?, patr=?, birth=? WHERE id=?",(SelectItem['surname'],SelectItem['name'],SelectItem['patr'],SelectItem['birth'],SelectItem['id']))
                conn.commit()
                SelectItem = {
                    'id': '',
                    'surname': '',
                    'name': '',
                    'patr': '',
                    'birth': ''
                }

    def clickDelete(self):
        try:
            delId = int(self.ui.lineEdit_4.text())
            cursor.execute("DELETE FROM users WHERE id = " + str(delId))
            conn.commit()
            self.ui.label_6.setText('Удалено !')
            self.renderViewTable()
        except ValueError:
            self.ui.label_6.setText('введите правильный id')


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
