
import os
import psycopg2


#def line_insert_record(record_list):
DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a ann-chang-dinnereat').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
create_table_query = '''CREATE TABLE tblfoodlist(
    seqno serial PRIMARY KEY,
    foodtype VARCHAR (50) NOT NULL,
    foodname VARCHAR (50) NOT NULL    );'''

cursor.execute(create_table_query)
conn.commit()
#
#    message = f"恭喜您！ 資料成功建立 tblfoodlist 表單！"
#    print(message)
cursor.close()
conn.close()

#    return message
