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
