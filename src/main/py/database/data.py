from database.config import config
import psycopg2

def getAllData(table):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)        
        cur = conn.cursor()
        sql_command = "SELECT * FROM {};".format(str(table))
        print (sql_command)
        cur.execute(sql_command)
        result = cur.fetchall()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def getSpecificData(table,col,param):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)        
        cur = conn.cursor()
        sql_command = "SELECT * FROM {} where {}='{}';".format(str(table),str(col),str(param))
        print (sql_command)
        cur.execute(sql_command)
        result = cur.fetchone()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insertUserData(val1,val2,val3,val4,val5,val6,val7,val8,val9):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)        
        cur = conn.cursor()
        sql_command="INSERT INTO crypto_user (user_id, first_name, last_name, email, pan_no, dob, mobile_no, exchange_account_id, status) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(str(val1),str(val2),str(val3),str(val4),str(val5),str(val6),str(val7),str(val8),str(val9))
        print(sql_command)
        cur.execute(sql_command)
        conn.commit()
        print("Record inserted successfully")
        cur.close()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insertTrade(val1,val2):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)        
        cur = conn.cursor()
        sql_command="INSERT INTO crypto_trade (user_id, trade_id) VALUES ('{}', '{}');".format(str(val1),str(val2))
        print(sql_command)
        cur.execute(sql_command)
        conn.commit()
        print("Record inserted successfully")
        cur.close()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')  

def getSpecificDataList(table,col,param):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)        
        cur = conn.cursor()
        sql_command = "SELECT * FROM {} where {}='{}';".format(str(table),str(col),str(param))
        print (sql_command)
        cur.execute(sql_command)
        result = cur.fetchall()
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')            
