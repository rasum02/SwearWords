import psycopg2
import os
import csv

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
        data_dir = os.path.join(base_dir, '..', '..', 'data')

        # Run users.sql
        with open(os.path.join(base_dir, "users.sql")) as db_file:
            cur.execute(db_file.read())

        # Run swearwords.sql
        with open(os.path.join(base_dir, "swearwords.sql")) as db_file:
            cur.execute(db_file.read())

        # Insert countries from file
        with open(os.path.join(data_dir, 'countries.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Country (country_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['country_id'], row['name'])
                )

        # Insert languages from file
        with open(os.path.join(data_dir, 'languages.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Language (language_code, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['language_code'], row['name'])
                )

        # Insert speaks (country-language relationship) from file
        with open(os.path.join(data_dir, 'speaks.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Speaks (country_id, language_code) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['country_id'], row['language_code'])
                )

        # Insert words and link to language
        for filename in os.listdir(data_dir):
            if filename in ('countries.csv', 'languages.csv', 'speaks.csv'):
                continue
            file_path = os.path.join(data_dir, filename)
            if not os.path.isfile(file_path):
                continue
            lang_code = filename.replace('.csv', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute(
                        "INSERT INTO Word (word_id, word) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (row['word_id'], row['word'])
                    )
                    cur.execute(
                        "INSERT INTO Has (language_code, word_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (lang_code, row['word_id'])
                    )

        conn.commit()

    conn.close()
