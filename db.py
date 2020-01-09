
import os
import psycopg2


def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    table_columns = '(foodtype, foodname)'
    postgres_insert_query = f"""INSERT INTO tblfoodlist {table_columns} VALUES (%s, %s);"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ 資料成功建立 tblfoodlist 表單！"
    print(message)
    cursor.close()
    conn.close()

    return message
