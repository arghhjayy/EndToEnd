from sqlalchemy import create_engine

username = "root"
password = "password"
host = "127.0.0.1"


def get_db_connection(database):
    # Create a SQLAlchemy engine
    conn_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"
    engine = create_engine(conn_string)

    return engine
