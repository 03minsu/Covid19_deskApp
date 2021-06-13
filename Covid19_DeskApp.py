from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pymysql
import sys

from pyqtgraph.graphicsItems.ScatterPlotItem import Symbols


conn = pymysql.connect(host='localhost', user='root', password='123456', db='covid19', charset='utf8')
curs = conn.cursor()
curs.execute("use covid19;")
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Covid.ui")[0]

class WindowClass(QtWidgets.QMainWindow, form_class) :
    
    def __init__(self) :    
        super().__init__()
        self.setupUi(self)
        self.btn3.clicked.connect(self.clear)
        self.btn1.clicked.connect(self.year2020)
        self.btn2.clicked.connect(self.year2021)

        self.GraphWidget.setBackground("w")
        self.GraphWidget.showGrid(x=True, y=True)
        self.GraphWidget.setLabel('left', "<span style=\"color:black;font-size:20px\">확진자 수 (Infec)</span>")
        self.GraphWidget.setLabel('bottom', "<span style=\"color:black;font-size:20px\">월 (Month)</span>")

    def plot(self, date, infec):
        pen = pg.mkPen(color=(0, 0, 255), width=3)
        self.GraphWidget.plot(date, infec, pen=pen, symbol='o')

    def clear(self):
        self.GraphWidget.clear()

    def year2020(self):
        sql = "select date_format(infecD,'%y-%m') date,count(no) from covid19 group by date having date < 21"
        curs.execute(sql)
        rows = curs.fetchall()
        x = [1,2,3,4,5,6,7,8,9,10,11,12]
        y = []
        for row in rows:
            y.append(row[1])
        self.plot(x,y)

    def year2021(self):
        sql = "select date_format(infecD,'%y-%m') date,count(no) from covid19 group by date having date = 21"
        curs.execute(sql)
        rows = curs.fetchall()
        x = [1,2,3,4,5,6]
        y = []
        for row in rows:
            y.append(row[1])
        self.plot(x,y)

def main():
    app = QApplication(sys.argv) 
    main = WindowClass() 
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__" :
    main()