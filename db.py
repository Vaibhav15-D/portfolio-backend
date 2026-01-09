
import os
import psycopg2

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def get_connection():
    return psycopg2.connect(
        dbname="portfolio_db",
        user="postgres",
        password="Vai@post",
        host="localhost"
    )

