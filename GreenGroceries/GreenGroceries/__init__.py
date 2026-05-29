import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask
from psycopg2.extras import RealDictCursor

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
)

db_cursor = conn.cursor(cursor_factory=RealDictCursor)

from GreenGroceries.blueprints.Login.routes import Login
from GreenGroceries.blueprints.Produce.routes import Produce

app.register_blueprint(Login)
app.register_blueprint(Produce)
