import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db = MySQLdb.connect(
        host='localhost',
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
    db.close()
except Exception as e:
    print(f"Failed to list tables: {e}")
