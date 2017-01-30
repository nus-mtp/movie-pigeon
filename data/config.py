import psycopg2


def database_connection():
    try:
        connect_str = "dbname='postgres' user='' host='localhost' " + \
                      "password=''"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        return cursor, conn
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
