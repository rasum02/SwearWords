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
        host=os.getenv('DB_HOST', 'localhost'),
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
        # Run produce.sql
        with open(os.path.join(base_dir, "produce.sql")) as db_file:
            cur.execute(db_file.read())
        # Run swearwords.sql
        with open(os.path.join(base_dir, "swearwords.sql")) as db_file:
            cur.execute(db_file.read())

        # Import all produce from the dataset
        all_produce = list(
            map(lambda x: tuple(x),
                df[['category', 'item', 'unit', 'variety', 'price']].to_records(index=False))
        )
        args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", i).decode('utf-8') for i in all_produce)
        cur.execute("INSERT INTO Produce (category, item, unit, variety, price) VALUES " + args_str)

        # Dummy farmer 1 sells all produce
        dummy_sales = [(1, i) for i in range(1, len(all_produce) + 1)]
        args_str = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in dummy_sales)
        cur.execute("INSERT INTO Sell (farmer_pk, produce_pk) VALUES " + args_str)

        # Insert countries from file
        with open(os.path.join(data_dir, 'countries.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Country (country_id, country) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['country_id'], row['country'])
                )

        # Insert languages from file
        with open(os.path.join(data_dir, 'languages.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Language (language_id, language) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['language_id'], row['language'])
                )

        # Insert speaks (country-language relationship) from file
        with open(os.path.join(data_dir, 'speaks.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Speaks (country_id, language_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['country_id'], row['language_id'])
                )

        # Insert words and link to language
        skip_files = {'countries.csv', 'languages.csv', 'speaks.csv'}
        for filename in os.listdir(data_dir):
            if filename in skip_files:
                continue
            file_path = os.path.join(data_dir, filename)
            if not os.path.isfile(file_path):
                continue
            lang_id = filename.replace('.csv', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute(
                        "INSERT INTO Word (word_id, word) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (row['word_id'], row['word'])
                    )
                    cur.execute(
                        "INSERT INTO Has (language_id, word_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (lang_id, row['word_id'])
                    )

        conn.commit()
        print("Database initialized successfully!")

    conn.close()
