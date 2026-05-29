import psycopg2
import os
import csv

from dotenv import load_dotenv

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
        data_dir = os.path.join(base_dir, '..', '..', '..', 'data')

        # Run swearwords.sql
        with open(os.path.join(base_dir, "swearwords.sql")) as db_file:
            cur.execute(db_file.read())

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

        # Insert categories from file
        with open(os.path.join(data_dir, 'categories.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO Category (category_id, category) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['category_id'], row['category'])
                )

        # Insert words and link to language
        skip_files = {'countries.csv', 'languages.csv', 'speaks.csv', 'categories.csv', 'belongs_to.csv'}
        for filename in os.listdir(data_dir):
            if filename in skip_files:
                continue
            if not filename.endswith('.csv'):
                continue
            file_path = os.path.join(data_dir, filename)
            if not os.path.isfile(file_path):
                continue
            lang_code = filename.replace('.csv', '')
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'word_id' not in (reader.fieldnames or []):
                    continue
                for row in reader:
                    cur.execute(
                        "INSERT INTO Word (word_id, word) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (row['word_id'], row['word'])
                    )
                    cur.execute(
                        "INSERT INTO Has (language_id, word_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (lang_code, row['word_id'])
                    )

        # Insert belongs_to from file (must be after words and categories)
        with open(os.path.join(data_dir, 'belongs_to.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO BelongsTo (word_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (row['word_id'], row['category_id'])
                )

        conn.commit()
        print("Database initialized successfully!")

    conn.close()
