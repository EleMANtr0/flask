import psycopg2
from psycopg2 import Error
import os
import time

USER = os.getenv("DB_USER", "postgres")
PWD = os.getenv("DB_PASSWORD", "pynative@#29")
DB = os.getenv("DB_NAME", "postgres_db")
HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", "5432"))
def connect(r=10,d=2):
    last_err = None
    for _ in range(r):
        connection, cursor = None, None
        try:
            connection = psycopg2.connect(user=USER,
                                          password=PWD,
                                          host=HOST,
                                          port=PORT,
                                          database=DB)
            cursor = connection.cursor()
            print(connection.get_dsn_parameters(),"\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("connected to - ", record, "\n")
            return
        except (Exception, Error) as e:
            last_err = e
            time.sleep(d)
            print("error connecting to PostgreSQL: ", e)
        else:
            if connection:
                cursor.close()
                connection.close()
                print("closed")
    return

if __name__ == "__main__":
    connect(10,2)
