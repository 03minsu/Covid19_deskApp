from os import close
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pymysql
import sys
import requests
from bs4 import BeautifulSoup

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
place_class = uic.loadUiType("place.ui")[0]
vacCine_class = uic.loadUiType("VacCine.ui")[0]
issue_class = uic.loadUiType("issue.ui")[0]
# ㄴ 시작 화면 


# 시작 화면 (초기 화면: 실행/종료)
class MainClass(QtWidgets.QMainWindow, main_class):
    def __init__(self) :    
        super().__init__()
        self.setupUi(self)
                                                                          
        self.pushButton.clicked.connect(self.menu) 
        # 종료 버튼 (전역 함수) 
        self.Exit.clicked.connect(QCoreApplication.instance().quit)                       
                                                                              
    def menu(self):                                                                                       
        MenuClass(self)                                                                     
                                                                                                
# 메뉴 화면 (실행 버튼 클릭 시)
class MenuClass(QtWidgets.QMainWindow, menu_class):
    def __init__(self, parent) :
        super(MenuClass, self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.MonthCovid.clicked.connect(self.covidGraph)
        self.CenterPlace.clicked.connect(self.CenterPlaceMap)
        self.VacCine.clicked.connect(self.VacCineInfo)
        self.VacCine_issue.clicked.connect(self.IssueForVaccien)

    def covidGraph(self):
        CovidClass(self)
    def CenterPlaceMap(self):
        PlaceClass(self)
    def VacCineInfo(self):
        VacCineClass(self)
    def IssueForVaccien(self):
        IssueClass(self)

# 기능 페이지 / 코로나 월 별 확진자 (연도 별 그래프)
class CovidClass(QtWidgets.QMainWindow, form_class) :
    
    def __init__(self, parent) :    
        super(CovidClass, self).__init__(parent)
        self.setupUi(self)
        self.btn3.clicked.connect(self.clear)
        self.btn1.clicked.connect(self.year2020)
        self.btn2.clicked.connect(self.year2021)
        # 현재 창 종료
        self.Quit.clicked.connect(self.place_close)
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
        self.GraphWidget.clear()
        sql = "select date_format(infecD,'%y%m') dateM, count(no) from covid19 group by dateM having dateM < 2100;"
        curs.execute(sql)
        rows = curs.fetchall()
        x = []
        y = []
        for row in rows:
            y.append(row[1])
        for row in rows:
            x.append(int(row[0]))
        self.plot(x,y)

    def year2021(self):
        self.GraphWidget.clear()
        sql = "select date_format(infecD,'%y%m') dateM, count(no) from covid19 group by dateM having dateM > 2100"
        curs.execute(sql)
        rows = curs.fetchall()
        x = []
        y = []
        for row in rows:
            y.append(row[1])
        for row in rows:
            x.append(int(row[0]))
        self.plot(x,y)

    def place_close(self):
        self.close()

class PlaceClass(QtWidgets.QMainWindow, place_class):
    def __init__(self, parent) :
        super(PlaceClass, self).__init__(parent)
        self.setupUi(self)
        self.show()
        
        # 현재 창 종료
        self.Quit.clicked.connect(self.place_close)
        
    def place_close(self):
        self.close()

class VacCineClass(QtWidgets.QMainWindow, vacCine_class):
    def __init__(self, parent) :
        super(VacCineClass, self).__init__(parent)
        self.setupUi(self)
        self.show()
    
        self.Quit.clicked.connect(self.place_close)
    
    def place_close(self):
        self.close()

class IssueClass(QtWidgets.QMainWindow, issue_class):
    def __init__(self, parent) :
        super(IssueClass, self).__init__(parent)
        self.setupUi(self)
        self.show()

        url = 'https://m.search.naver.com/search.naver?sm=mtb_hty.top&where=m_news&oquery=%EB%B0%B1%EC%8B%A0&tqi=hLj%2FFwp0JxossMRDexRssssstGd-286066&query=%22%EB%B0%B1%EC%8B%A0%22&nso=so%3Add%2Cp%3Aall&mynews=0&office_section_code=0&office_type=0&pd=0&photo=0&sort=1'

        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
    

            for x in range(1,16): 
                title_html = soup.select_one('#news_result_list > li:nth-child({0}) > div > a > div'.format(x))
                title = title_html.getText()
                link = soup.select_one('#news_result_list > li:nth-child({0}) > div > a'.format(x)).get('href')
                self.tb.append(str(x) + ". " + title + ' (' + '<a href="' + link + '">Link</a>' + ')' + "<br>")
            else : 
                print(response.status_code)

        self.Quit.clicked.connect(self.place_close)
    
    def place_close(self):
        self.close()

# 최초 실행 로직 --
def main():
    app = QApplication(sys.argv) 
    main = MainClass() 
    main.show()
    app.exec_()

if __name__ == "__main__" :
    main()
     
     #  부모 클래스  메인창                #  자식 클래스 새창
     # def __init__(self) :    ->   def __init__(self, parent) :
         # super().__init__()   ->      super([클래스명], self).__init__(parent)
                                            # self.show()
            # 클래스 호출은 함수 안에 '[클래스명](self)' 로 선언