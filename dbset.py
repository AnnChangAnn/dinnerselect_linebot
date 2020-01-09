
import os
import psycopg2


#def line_insert_record(record_list):
DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a ann-chang-dinnereat').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
#create_table_query = '''CREATE TABLE tblfoodlist(
#    seqno serial PRIMARY KEY,
#    foodtype VARCHAR (50) NOT NULL,
#    foodname VARCHAR (50) NOT NULL    );'''
#
#cursor.execute(create_table_query)
#conn.commit()

record = [('food', '維力炸醬麵'),('food', '辣炒年糕'),('food', '餛飩乾麵')]
table_columns = '(foodtype, foodname)'
postgres_insert_query = f"""INSERT INTO alpaca_training {table_columns} VALUES (%s, %s);"""

#cursor.execute(postgres_insert_query, record)
cursor.executemany(postgres_insert_query, record)
conn.commit()

count = cursor.rowcount
print(count, "Record inserted successfully into tblfoodlist")

postgres_select_query = f"""SELECT * FROM alpaca_training"""

cursor.execute(postgres_select_query)
cursor.fetchmany()
#
#    message = f"恭喜您！ 資料成功建立 tblfoodlist 表單！"
#    print(message)
cursor.close()
conn.close()

#    return message
