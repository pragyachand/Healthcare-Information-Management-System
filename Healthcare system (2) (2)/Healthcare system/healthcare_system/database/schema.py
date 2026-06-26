"""
Database Schema Creator
Creates all necessary tables for the Healthcare Management System
"""

from .db_config import DatabaseManager, DatabaseConfig
import mysql.connector
from mysql.connector import Error

class DatabaseSchema:
    """Database schema creation and management"""
    
    @staticmethod
    def create_database():
        """Create the healthcare_db database if it doesn't exist"""
        db_manager = DatabaseManager()
        
        try:
            # Connect without specifying database
            if not db_manager.connect(include_db=False):
                print("Failed to connect to MySQL server")
                return False
            
            # Check if database exists
            cursor = db_manager.connection.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (DatabaseConfig.DATABASE,))
            result = cursor.fetchone()
            
            if not result:
                # Create database
                cursor.execute(f"CREATE DATABASE {DatabaseConfig.DATABASE}")
                print(f"✓ Database '{DatabaseConfig.DATABASE}' created successfully")
            else:
                print(f"✓ Database '{DatabaseConfig.DATABASE}' already exists")
            
            cursor.close()
            db_manager.disconnect()
            return True
            
        except Error as e:
            print(f"Error creating database: {e}")
            return False
    
    @staticmethod
    def create_tables():
        """Create all necessary tables"""
        db_manager = DatabaseManager()
        
        if not db_manager.connect():
            print("Failed to connect to database")
            return False
        
        tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(15),
                    role ENUM('admin', 'doctor', 'nurse', 'patient') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """,
            
            'patients': """
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    date_of_birth DATE,
                    gender ENUM('Male', 'Female', 'Other'),
                    address TEXT,
                    emergency_contact VARCHAR(100),
                    emergency_phone VARCHAR(15),
                    blood_group VARCHAR(5),
                    medical_history TEXT,
                    allergies TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,
            
            'doctors': """
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    specialization VARCHAR(100),
                    license_number VARCHAR(50) UNIQUE,
                    department VARCHAR(50),
                    qualification VARCHAR(200),
                    experience_years INT,
                    consultation_fee DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,
            
            'nurses': """
                CREATE TABLE IF NOT EXISTS nurses (
                    nurse_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    department VARCHAR(50),
                    shift_type ENUM('Day', 'Night', 'Rotating'),
                    qualification VARCHAR(200),
                    license_number VARCHAR(50) UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """,
            
            'appointments': """
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status ENUM('Scheduled', 'Completed', 'Cancelled', 'Rescheduled') DEFAULT 'Scheduled',
                    reason_for_visit TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
                )
            """,
            
            'prescriptions': """
                CREATE TABLE IF NOT EXISTS prescriptions (
                    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    appointment_id INT,
                    prescription_date DATE NOT NULL,
                    diagnosis TEXT,
                    medications TEXT NOT NULL,
                    dosage_instructions TEXT,
                    notes TEXT,
                    status ENUM('Active', 'Completed', 'Cancelled') DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
                    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
                )
            """,
            
            'vitals': """
                CREATE TABLE IF NOT EXISTS vitals (
                    vital_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    recorded_by INT NOT NULL,
                    blood_pressure_systolic INT,
                    blood_pressure_diastolic INT,
                    heart_rate INT,
                    temperature DECIMAL(4,1),
                    weight DECIMAL(5,2),
                    height DECIMAL(5,2),
                    oxygen_saturation INT,
                    notes TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                    FOREIGN KEY (recorded_by) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """
        }
        
        success = True
        for table_name, create_query in tables.items():
            try:
                db_manager.execute_query(create_query)
                print(f"✓ Table '{table_name}' created successfully")
            except Exception as e:
                print(f"✗ Error creating table '{table_name}': {e}")
                success = False
        
        db_manager.disconnect()
        return success
    
    @staticmethod
    def initialize_admin_user():
        """Create default admin user"""
        db_manager = DatabaseManager()
        
        if not db_manager.connect():
            return False
        
        # Check if admin user exists
        admin_check = db_manager.execute_query(
            "SELECT user_id FROM users WHERE username = %s AND role = 'admin'",
            ('admin',),
            fetch=True
        )
        
        if not admin_check:
            # Create admin user with hashed password
            import hashlib
            
            plain_password = 'admin123'
            hashed_password = hashlib.sha256(plain_password.encode()).hexdigest()
            
            admin_data = {
                'username': 'admin',
                'password': hashed_password,  # Properly hashed password
                'email': 'admin@healthcare.com',
                'full_name': 'System Administrator',
                'phone': '1234567890',
                'role': 'admin'
            }
            
            success = db_manager.execute_query(
                """INSERT INTO users (username, password, email, full_name, phone, role) 
                   VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(phone)s, %(role)s)""",
                admin_data
            )
            
            if success:
                print("✓ Default admin user created (username: admin, password: admin123)")
            else:
                print("✗ Failed to create admin user")
        else:
            print("✓ Admin user already exists")
        
        db_manager.disconnect()
        return True

def initialize_database():
    """Initialize the complete database"""
    print("Initializing Healthcare Database...")
    print("=" * 40)
    
    # Step 1: Create database
    if not DatabaseSchema.create_database():
        print("Failed to create database")
        return False
    
    # Step 2: Create tables
    if not DatabaseSchema.create_tables():
        print("Failed to create tables")
        return False
    
    # Step 3: Create admin user
    if not DatabaseSchema.initialize_admin_user():
        print("Failed to create admin user")
        return False
    
    print("=" * 40)
    print("✅ Database initialization completed successfully!")
    return True

if __name__ == "__main__":
    initialize_database()