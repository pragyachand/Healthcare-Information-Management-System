"""
Database Connection Test Script
Healthcare Management System
"""

import mysql.connector
from mysql.connector import Error

def test_database_connection():
    """Test database connection with different scenarios"""
    
    # Connection parameters from db_config.py
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Mnbv@123'
    }
    
    print("=" * 50)
    print("DATABASE CONNECTION TEST")
    print("=" * 50)
    
    # Test 1: Basic MySQL connection (without database)
    print("\n1. Testing basic MySQL connection...")
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("✓ Successfully connected to MySQL server")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"  MySQL Server version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"  Database version: {version[0]}")
            
            cursor.close()
            connection.close()
        else:
            print("❌ Failed to connect to MySQL server")
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False
    
    # Test 2: Check if healthcare_db exists
    print("\n2. Checking if healthcare_db database exists...")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        db_exists = False
        print("  Available databases:")
        for db in databases:
            print(f"    - {db[0]}")
            if db[0] == 'healthcare_db':
                db_exists = True
        
        if db_exists:
            print("✓ healthcare_db database exists")
        else:
            print("❌ healthcare_db database NOT found")
            
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error checking databases: {e}")
        return False
    
    # Test 3: Connect to healthcare_db and check tables
    print("\n3. Testing connection to healthcare_db...")
    try:
        config_with_db = config.copy()
        config_with_db['database'] = 'healthcare_db'
        
        connection = mysql.connector.connect(**config_with_db)
        if connection.is_connected():
            print("✓ Successfully connected to healthcare_db")
            
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print("  Available tables:")
                for table in tables:
                    print(f"    - {table[0]}")
            else:
                print("  No tables found in healthcare_db")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Failed to connect to healthcare_db")
            
    except Error as e:
        print(f"❌ Error connecting to healthcare_db: {e}")
        print("  This might be because the database doesn't exist or tables haven't been created")
    
    # Test 4: Check specific tables required by the application
    print("\n4. Checking required tables...")
    required_tables = ['users', 'patients', 'doctors', 'nurses', 'appointments']
    
    try:
        config_with_db = config.copy()
        config_with_db['database'] = 'healthcare_db'
        
        connection = mysql.connector.connect(**config_with_db)
        cursor = connection.cursor()
        
        for table in required_tables:
            try:
                cursor.execute(f"DESCRIBE {table}")
                print(f"  ✓ Table '{table}' exists")
            except Error as table_error:
                print(f"  ❌ Table '{table}' missing: {table_error}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Could not check tables: {e}")
    
    print("\n" + "=" * 50)
    print("Connection test completed!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_database_connection()