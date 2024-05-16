import psycopg2
from config import config


def connect():
    connection = None
    try:
        params = config()
        print("Connection to the postgreSQL database ...")
        connection = psycopg2.connect(**params)

        # create cursor
        crsr = connection.cursor()
        print("PstgreSQL database version: ")
        crsr.execute("SELECT version()")
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()

    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminates")


if __name__ == "__main__":
    connect()
