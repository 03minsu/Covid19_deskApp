from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pymysql
import sys

from pyqtgraph.graphicsItems.ScatterPlotItem import Symbols
# ㄴ 그래프 심볼 

conn = pymysql.connect(host='localhost', user='root', password='123456', db='covid19', charset='utf8')
curs = conn.cursor()
curs.execute("use covid19;")

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Covid.ui")[0]
main_class = uic.loadUiType("Main.ui")[0]
menu_class = uic.loadUiType("Menu.ui")[0]
# ㄴ 시작 화면 


# 시작 화면 (초기 화면: 실행/종료)
class MainClass(QtWidgets.QMainWindow, main_class):
    def __init__(self) :    
        super().__init__()
        self.setupUi(self)
                                                                           #  부모 클래스  메인창                #  자식 클래스 새창
        self.pushButton.clicked.connect(self.menu)                        # def __init__(self) :    ->   def __init__(self, parent) :
                                                                              # super().__init__()   ->      super([클래스명], self).__init__(parent)
    def menu(self):                                                                                        # self.show()
        MenuClass(self)                                                                     
                                                                                                # 클래스 호출은 함수 안에 '[클래스명](self)' 로 선언
# 메뉴 화면 (실행 버튼 클릭 시)
class MenuClass(QtWidgets.QMainWindow, menu_class):
    def __init__(self, parent) :
        super(MenuClass, self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.MonthCovid.clicked.connect(self.covidGraph)

    def covidGraph(self):
        CovidClass(self)

# 기능 페이지 / 코로나 월 별 확진자 (연도 별 그래프)
class CovidClass(QtWidgets.QMainWindow, form_class) :
    
    def __init__(self, parent) :    
        super(CovidClass, self).__init__(parent)
        self.setupUi(self)
        self.btn3.clicked.connect(self.clear)
        self.btn1.clicked.connect(self.year2020)
        self.btn2.clicked.connect(self.year2021)
        self.show()

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


# 최초 실행 로직 --
def main():
    app = QApplication(sys.argv) 
    main = MainClass() 
    main.show()
    app.exec_()

if __name__ == "__main__" :
    main()