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
    
    # Disable foreign key checks to allow dropping tables in any order
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if not tables:
        print("No tables found to drop.")
    else:
        for table in tables:
            print(f"Dropping table: {table[0]}")
            cursor.execute(f"DROP TABLE `{table[0]}`")
            
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.commit()
    print("All tables dropped successfully.")
    db.close()
except Exception as e:
    print(f"Failed to clear database: {e}")
