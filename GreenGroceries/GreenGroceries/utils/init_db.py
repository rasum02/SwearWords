import psycopg2
import os

from dotenv import load_dotenv
from choices import df
import numpy as np

np.set_printoptions(legacy='1.25')

load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
    )
    with conn.cursor() as cur:
        base_dir = os.path.dirname(__file__)
        # Run users.sql
        with open(os.path.join(base_dir, "users.sql")) as db_file:
            cur.execute(db_file.read())
        # Run produce.sql
        with open(os.path.join(base_dir, "swearwords.sql")) as db_file:
            cur.execute(db_file.read())

        for code, name in LANGUAGES.items():
            cur.execute

        conn.commit()

    conn.close()
