import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, \
    QAbstractItemView
from main_design import Ui_Form
from add_coffee_design import Ui_Form2


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.func = self.load_info
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.pushButton.clicked.connect(self.open_add_widget)
        self.tableWidget.itemClicked.connect(self.open_edit_widget)
        self.load_info()

    def load_info(self):
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM coffee_info""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def open_edit_widget(self):
        self.edit_info = EditCoffee(self.func, self.tableWidget.item(
            self.tableWidget.currentRow(), 0).text())
        self.edit_info.show()

    def open_add_widget(self):
        self.new_info = AddCoffee(self.func)
        self.new_info.show()


class AddCoffee(QWidget, Ui_Form2):
    def __init__(self, func):
        super().__init__()
        self.setupUi(self)
        self.func = func
        self.pushButton.clicked.connect(self.add_info)

    def add_info(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        cur.execute(f"""INSERT INTO coffee_info(variety, roast, beanOrGround,
        taste, price, volume) VALUES('{self.lineEdit.text()}',
        '{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}',
        '{self.lineEdit_4.text()}', {int(self.lineEdit_5.text())},
        {int(self.lineEdit_6.text())})""")

        con.commit()
        con.close()
        self.func()
        self.close()


class EditCoffee(QWidget, Ui_Form2):
    def __init__(self, func, id=None):
        super().__init__()
        self.setupUi(self)
        self.func = func
        self.id = int(id)
        self.load_cells_info()
        self.pushButton.clicked.connect(self.edit_info)

    def load_cells_info(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT * FROM coffee_info 
        WHERE id = {self.id}""").fetchone()
        self.con.commit()
        self.con.close()

        self.lineEdit.setText(str(result[1]))
        self.lineEdit_2.setText(str(result[2]))
        self.lineEdit_3.setText(str(result[3]))
        self.lineEdit_4.setText(str(result[4]))
        self.lineEdit_5.setText(str(result[5]))
        self.lineEdit_6.setText(str(result[6]))

    def edit_info(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        cur.execute(f"""UPDATE coffee_info SET variety = 
        '{self.lineEdit.text()}', roast = '{self.lineEdit_2.text()}', 
        beanOrGround = '{self.lineEdit_3.text()}',
        taste = '{self.lineEdit_4.text()}', 
        price = {int(self.lineEdit_5.text())},
        volume = {int(self.lineEdit_6.text())} WHERE id = {self.id}""")

        con.commit()
        con.close()
        self.func()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
