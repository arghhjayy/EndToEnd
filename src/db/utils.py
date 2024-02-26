import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
host = os.environ["DB_HOST"]


def get_db_connection(database):
    # Create a SQLAlchemy engine
    conn_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"
    engine = create_engine(conn_string)

    return engine
