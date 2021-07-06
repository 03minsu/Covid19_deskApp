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
import tensorflow.keras
import numpy as np
import cv2

from pyqtgraph.graphicsItems.ScatterPlotItem import Symbols
# ㄴ 그래프 심볼 

conn = pymysql.connect(host='localhost', user='root', password='123456', db='covid19', charset='utf8')
curs = conn.cursor()


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Covid.ui")[0]
main_class = uic.loadUiType("Main.ui")[0]
menu_class = uic.loadUiType("Menu.ui")[0]
place_class = uic.loadUiType("place.ui")[0]
vacCine_class = uic.loadUiType("VacCine.ui")[0]
issue_class = uic.loadUiType("issue.ui")[0]
vacAdv_class = uic.loadUiType("vaccine_adv.ui")[0]
district_class = uic.loadUiType("district.ui")[0]
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

        self.Quit_2.clicked.connect(self.place_close)

        self.MonthCovid.clicked.connect(self.covidGraph)
        self.CenterPlace.clicked.connect(self.CenterPlaceMap)
        self.VacCine.clicked.connect(self.VacCineInfo)
        self.VacCine_issue.clicked.connect(self.IssueForVaccien)
        self.dist_inc.clicked.connect(self.dist_list)
        self.vac_status.clicked.connect(self.vaccine_cal)
        self.maskMode.clicked.connect(self.MaskCheck)

    def covidGraph(self):
        CovidClass(self)
    def CenterPlaceMap(self):
        PlaceClass(self)
    def VacCineInfo(self):
        VacCineClass(self)
    def IssueForVaccien(self):
        IssueClass(self)
    def vaccine_cal(self):
        VaccineCalculator(self)
    def dist_list(self):
        DistrictInc(self)
    
    def MaskCheck(self):
        # 모델 위치
        model_filename ='./maskTEST/keras_model.h5'

        # 케라스 모델 가져오기
        model = tensorflow.keras.models.load_model(model_filename)

        # 카메라를 제어할 수 있는 객체
        capture = cv2.VideoCapture(0)

        # 카메라 길이 너비 조절
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

        # 이미지 처리하기
        def preprocessing(frame):
            #frame_fliped = cv2.flip(frame, 1)
            # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
            size = (224, 224)
            frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
            
            # 이미지 정규화
            # astype : 속성
            frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

            # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
            # keras 모델에 공급할 올바른 모양의 배열 생성
            frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
            #print(frame_reshaped)
            return frame_reshaped

        # 예측용 함수
        def predict(frame):
            prediction = model.predict(frame)
            return prediction

        while True:
            ret, frame = capture.read()

            if cv2.waitKey(100) > 0: 
                break

            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)

            if (prediction[0,0] < prediction[0,1]):
                cv2.putText(frame, 'mask on', (0, 250), cv2.FONT_HERSHEY_PLAIN, 10, (0, 128, 0), thickness=20)

            else:
                cv2.putText(frame, 'mask off', (0, 250), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), thickness=20)

            cv2.imshow("VideoFrame", frame)

    def place_close(self):
        self.close()


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

class VaccineCalculator(QtWidgets.QMainWindow, vacAdv_class) : # 백신 현황 페이지 백신 테이블/접종률대비 부작용 비율 계산
    
    def __init__(self, parent) :    
        super(VaccineCalculator, self).__init__(parent)
        self.setupUi(self)
        self.cal_but.clicked.connect(self.cal)
        self.show()

        self.Quit.clicked.connect(self.place_close)

    def cal(self):
        bring_txt = self.vac_box.currentText()

        if bring_txt == "아스트라제네카":
            sql = "select (ast_adv / ast) * 100 from vac_adv"
            curs.execute(sql)
            row = curs.fetchone()
            con_txt = "접종자수 대비 중대이상반응 비율 :  " + str(row[0]) + "%"
            self.vac_per.setText(con_txt)
            
        if bring_txt == "화이자":
            sql = "select (pfi_adv / pfi) * 100 from vac_adv"
            curs.execute(sql)
            row = curs.fetchone()
            con_txt = "접종자수 대비 중대이상반응 비율 :  " + str(row[0]) + "%"
            self.vac_per.setText(con_txt)

        if bring_txt == "얀센":
            sql = "select (jan_adv / jan) * 100 from vac_adv"
            curs.execute(sql)
            row = curs.fetchone()
            con_txt = "접종자수 대비 중대이상반응 비율 :  " + str(row[0]) + "%"
            self.vac_per.setText(con_txt)

        if bring_txt == "모더나":
            sql = "select (moder_adv / moder) * 100 from vac_adv"
            curs.execute(sql)
            row = curs.fetchone()
            con_txt = "접종자수 대비 중대이상반응 비율 :  " + str(row[0]) + "%"
            self.vac_per.setText(con_txt)
        
    
    def place_close(self):
        self.close()

class DistrictInc(QtWidgets.QMainWindow, district_class) :
    
    def __init__(self, parent) :    
        super(DistrictInc, self).__init__(parent)
        self.setupUi(self)
        self.calendar.clicked.connect(self.dist)
        self.show()
        self.Quit_2.clicked.connect(self.place_close)


    def dist(self):
        self.dist_txt.clear()
        district = self.dist_list.currentText()
        caln = self.calendar.selectedDate().toString().split(" ")
        date = caln[3] + "-" + caln[1] + "-" + caln[2]
        count = 0

        sql = "select infecD, place, infecP, state from covid19 where place = '{0}' and infecD = '{1}'".format(district, date)
        curs.execute(sql)
        rows = curs.fetchall()

        for row in rows:
            count += 1
            txt = str(row[0]) + "/위치 : " + row[1] + "/감염경로 : " + row[2] + "/상태 : " + row[3]
            print(txt)
            self.dist_txt.append(txt)
        self.dist_txt.append("총 " + str(count) + "명 확진자가 발생")

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
