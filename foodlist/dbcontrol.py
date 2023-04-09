import os
import psycopg2
import random

def line_create_table(new_table_name):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    create_table_query = f'''CREATE TABLE tblreply(
        seqno serial PRIMARY KEY,
        foodtype VARCHAR (50) NOT NULL,
        replyfront VARCHAR (50) NOT NULL,
        replyend VARCHAR (50) NOT NULL
    );'''
    
    cursor.execute(create_table_query)
    conn.commit()

    message = f"恭喜您！ 成功建立新表單！"
    cursor.close()
    conn.close()

    return message

def line_insert_reply(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    table_columns = '(foodtype, replyfront, replyend)'
    postgres_insert_query = f"""INSERT INTO tblreply {table_columns} VALUES (%s, %s, %s);"""
    
    print(postgres_insert_query)
    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ 資料成功加入 tblreply 表單！"
    cursor.close()
    conn.close()

    return message

def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    table_columns = '(foodtype, foodname)'
    postgres_insert_query = f"""INSERT INTO tblfoodlist {table_columns} VALUES (%s, %s);"""
    print(postgres_insert_query)
    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ 資料成功加入 tblfoodlist 表單！"
    cursor.close()
    conn.close()

    return message

def user_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    table_columns = '(foodtype, foodname)'
    postgres_insert_query = f"""INSERT INTO tblfoodlist {table_columns} VALUES (%s, %s);"""
    print(postgres_insert_query)
    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"好喔！下次會考慮推薦你這個～"
    cursor.close()
    conn.close()

    return message

def line_select_overall(choosetype):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    strfoodtype = "'" + choosetype + "'"
    postgres_select_query = f"""SELECT foodname FROM tblfoodlist where foodtype =  {strfoodtype} ;"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)
    raw = cursor.fetchall()
    (food_name,) = random.choice(raw)
    
    postgres_select_query = f"""SELECT replyfront, replyend FROM tblreply where foodtype =  {strfoodtype};"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)
    rawreply = cursor.fetchall()
    (reply_front, reply_end) = random.choice(rawreply)
    print(reply_front)
    print(reply_end)
    
    if reply_end == '_':
        message = reply_front + food_name + "!!"
    else:
        message = reply_front + food_name + reply_end
    print(message)
        
    cursor.close()
    conn.close()

    return food_name, message

def line_select_sp(choosetype):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    strfoodtype = "'" + choosetype + "'"
    postgres_select_query = f"""SELECT foodname FROM tblfoodlist where foodtype =  {strfoodtype} ;"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)
    raw = cursor.fetchall()
    (food_name,) = random.choice(raw)
    
    message = food_name
    print(message)
        
    cursor.close()
    conn.close()

    return message

def line_select_reply(choosetype):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    strfoodtype = "'" + choosetype + "'"
    
    postgres_select_query = f"""SELECT replyfront, replyend FROM tblreply where foodtype =  {strfoodtype};"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)
    rawreply = cursor.fetchall()
    (reply_front, reply_end) = random.choice(rawreply)
    print(reply_front)
    print(reply_end)
    
    if reply_end == '_':
        reply_end = "!!"
        
    cursor.close()
    conn.close()

    return reply_front, reply_end
    
def line_delete_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    strfoodtype = record_list
    delete_table_query = f'''DELETE from tblfoodlist where
        foodname = '{strfoodtype}'
    ;'''
    print (delete_table_query)
    
    cursor.execute(delete_table_query)
    conn.commit()

    message = f"恭喜您！ 成功刪除資料！"
    
    cursor.close()
    conn.close()

    return message

def line_test_program(txttext):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT replyfront, replyend FROM tblreply;"""
    print(postgres_select_query)

    cursor.execute(postgres_select_query)
    raw = cursor.fetchall()
    print(raw)
    (message1, message2) = random.choice(raw)
    print(message1)
    print(message2)
    
    cursor.close()
    conn.close()

    return message1
