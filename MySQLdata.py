import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host='localhost', user='root', passwd='donnhh16', db='myblog', charset='utf8')
c = conn.cursor()

c.execute('''INSERT INTO `article`(`title`, `body`)  # 쿼리문을 실행
VALUES(\'second jemok\', \'second naeyong\')''') 
conn.commit() #변경된 값을 데이터베이스에 적용합니다.

c.execute('SELECT * FROM `article`')
list = c.fetchall()

for i in list: #하나의 요소는 하나의 튜플
	print i