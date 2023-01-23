import os.path


from database import create_sqlite_engine, logs_table
from consts import DB_FILE

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(DB_FILE)):
        os.mkdir(os.path.dirname(DB_FILE))

    engine = create_sqlite_engine(DB_FILE)

    try:
        logs_table.create(engine)
        print("Tables created")
    except Exception as e:
        print("Error occurred during Table creation!")
        print(e)
