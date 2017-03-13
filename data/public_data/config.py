import psycopg2


def database_connection():
    try:
        connect_str = "dbname='production' " \
                      "user='postgres' " \
                      "host='128.199.231.190' " + \
                      "password=''"

        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        return cursor, conn
    except Exception as e:
        print(e)
