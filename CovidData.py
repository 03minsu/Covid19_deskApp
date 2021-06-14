import csv
import pymysql 
#ALTER TABLE covid19 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci 
#실행 할 때 호환에러가 일어나면 MYSQL에 입력
conn = pymysql.connect(host='localhost', user='root', password='123456', db='covid19', charset='utf8mb4')
curs = conn.cursor()
conn.commit()

f = open('covid19.csv','r',encoding='cp949')
csvReader = csv.reader(f)

for row in csvReader:
    no = (row[0])
    infecD = (row[1])
    place = (row[2])
    trv = (row[3])
    infecP = (row[4])
    state = (row[5])
    sql = "insert into covid19 (no,infecD,place,trv,infecP,state) values (%s,%s,%s,%s,%s,%s)"
    curs.execute(sql,(no,infecD,place,trv,infecP,state))

conn.commit()

f.close()   
conn.close()