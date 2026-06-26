"""
Database Configuration and Connection Manager
Healthcare Management System
"""

import mysql.connector
from mysql.connector import Error
import os

class DatabaseConfig:
    """Database configuration settings"""
    
    # Database connection parameters
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'Mnbv@123'
    DATABASE = 'healthcare_db'
    
    @classmethod
    def get_connection_params(cls, include_db=True):
        """Get connection parameters"""
        params = {
            'host': cls.HOST,
            'user': cls.USER,
            'password': cls.PASSWORD
        }
        if include_db:
            params['database'] = cls.DATABASE
        return params

class DatabaseManager:
    """Database connection and management class"""
    
    def __init__(self):
        self.connection = None
        
    def connect(self, include_db=True):
        """Establish database connection"""
        try:
            params = DatabaseConfig.get_connection_params(include_db)
            self.connection = mysql.connector.connect(**params)
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a database query"""
        # Check if connection exists and is active
        if not self.connection or not self.connection.is_connected():
            print("Database error: MySQL Connection not available. Attempting to reconnect...")
            if not self.connect():
                print("Database error: Failed to establish connection")
                return None if fetch else False
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            print(f"Database error: {e}")
            return None if fetch else False
    
    def execute_many(self, query, data_list):
        """Execute query with multiple data sets"""
        # Check if connection exists and is active
        if not self.connection or not self.connection.is_connected():
            print("Database error: MySQL Connection not available. Attempting to reconnect...")
            if not self.connect():
                print("Database error: Failed to establish connection")
                return False
        
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data_list)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

# Initialize connection on module import
def initialize_database():
    """Initialize database connection"""
    if not db_manager.connect():
        print("Warning: Could not establish initial database connection")
        print("Connection will be attempted automatically when needed")
    else:
        print("✓ Database connection established successfully")

# Auto-initialize when module is imported
initialize_database()