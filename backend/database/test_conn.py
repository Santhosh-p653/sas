# backend/database/test_conn.py

import sys
import os

# Add backend folder to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now imports will work
from config.config import DB_NAME, DB_HOST, DB_PORT, SAN_PASS
import psycopg2

# Connect as Santhosh (Admin)
conn = psycopg2.connect(
    dbname=DB_NAME,
    user="santhosh_user",
    password=SAN_PASS,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Example: Check current database
cur.execute("SELECT current_database();")
print(cur.fetchone())

# Close cursor and connection
cur.close()
conn.close()
