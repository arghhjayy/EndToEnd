import pymysql.cursors


def get_db_connection(database):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="actual_data",
        cursorclass=pymysql.cursors.DictCursor,
    )

    return connection
