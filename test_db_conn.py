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
    print("Connection successful!")
    db.close()
except Exception as e:
    print(f"Connection failed: {e}")
