import mysql.connector
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default phpMyAdmin password is empty
    'database': 'fullstack_assessment'
}

def test_connection():
    try:
        # Try to connect to MySQL server
        print("Attempting to connect to MySQL server...")
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        print("Connected to MySQL server successfully!")
        
        # Check if database exists
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (DB_CONFIG['database'],))
        result = cursor.fetchone()
        
        if result:
            print(f"Database '{DB_CONFIG['database']}' exists.")
            
            # Connect to the specific database
            conn.close()
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print("Tables in the database:")
                for table in tables:
                    print(f"- {table[0]}")
                    
                    # Show table structure
                    cursor.execute(f"DESCRIBE {table[0]}")
                    columns = cursor.fetchall()
                    print("  Columns:")
                    for column in columns:
                        print(f"  - {column[0]}: {column[1]}")
                
                # Check if there's any data in the tables
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"- {table[0]} has {count} records")
            else:
                print("No tables found in the database.")
        else:
            print(f"Database '{DB_CONFIG['database']}' does not exist.")
        
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("\nDatabase connection test completed successfully.")
        sys.exit(0)
    else:
        print("\nDatabase connection test failed.")
        sys.exit(1) 