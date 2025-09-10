import os
import psycopg

from dotenv import load_dotenv # Loads .env
load_dotenv()

connection = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)

with connection.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            link TEXT UNIQUE NOT NULL,
            guid TEXT,
            published TIMESTAMP,
            media TEXT,
            original_content TEXT,
            modified_content TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    connection.commit()

connection.close()
print("Database initialised.")