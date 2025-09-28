# In backend/tools/cloud_sql_tools.py
import psycopg2
import os

def get_db_conn():
    """Establishes a connection to the Google Cloud SQL database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# ... (Your other functions like create_listing, etc., will work the same as the Postgres/pg_vector versions)