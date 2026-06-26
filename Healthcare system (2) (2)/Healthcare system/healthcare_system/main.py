"""
Healthcare Management System - Main Application
Entry point for the Healthcare Management System

Author: GitHub Copilot Assistant
Description: Complete healthcare management system with role-based access
Technology Stack: Python Tkinter (GUI) + MySQL (Database) + mysql-connector-python
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_and_install_dependencies():
    """Check and install required dependencies"""
    try:
        print("Checking dependencies...")
        
        # Check for mysql-connector-python
        try:
            import mysql.connector
            print("✓ mysql-connector-python is available")
        except ImportError:
            print("Installing mysql-connector-python...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python==8.2.0"])
            print("✓ mysql-connector-python installed successfully")
        
        # Check for reportlab
        try:
            import reportlab
            print("✓ reportlab is available")
        except ImportError:
            print("Installing reportlab...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab==4.0.7"])
            print("✓ reportlab installed successfully")
        
        # Check for tkinter (usually comes with Python)
        try:
            import tkinter as tk
            print("✓ tkinter is available")
        except ImportError:
            print("❌ tkinter is not available. Please install tkinter for your Python distribution.")
            return False
        
        print("All dependencies are ready!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def setup_database():
    """Initialize database and create tables"""
    try:
        print("Setting up database...")
        
        # Import database modules
        from database.schema import DatabaseSchema
        
        # Create database and tables
        schema = DatabaseSchema()
        
        if schema.create_database():
            print("✓ Database 'healthcare_db' created/verified")
        else:
            print("❌ Failed to create/verify database")
            return False
        
        if schema.create_tables():
            print("✓ Database tables created/verified")
        else:
            print("❌ Failed to create database tables")
            return False
        
        if schema.initialize_admin_user():
            print("✓ Default admin user initialized")
        else:
            print("❌ Failed to initialize admin user")
            return False
        
        print("Database setup completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importing database modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def start_application():
    """Start the main application"""
    try:
        print("Starting Healthcare Management System...")
        
        # Import authentication module
        from auth import LoginWindow
        
        # Create main application window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Start with login window
        login_window = LoginWindow()
        
        # Start the application event loop
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error importing application modules: {e}")
        messagebox.showerror("Import Error", f"Failed to import required modules: {e}")
    except Exception as e:
        print(f"❌ Application startup error: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")

def show_system_info():
    """Display system information"""
    print("="*60)
    print("HEALTHCARE MANAGEMENT SYSTEM")
    print("="*60)
    print("Version: 1.0.0")
    print("Technology Stack:")
    print("  - GUI Framework: Python Tkinter")
    print("  - Database: MySQL")
    print("  - Database Connector: mysql-connector-python 8.2.0")
    print("  - Programming Language: Python 3.x")
    print()
    print("Features:")
    print("  - Role-based authentication (Admin, Doctor, Nurse, Patient)")
    print("  - Appointment management")
    print("  - Patient record management")
    print("  - Prescription management")
    print("  - Vitals recording and tracking")
    print("  - Comprehensive reporting system")
    print("  - User management (Admin)")
    print()
    print("Database Requirements:")
    print("  - MySQL Server (localhost)")
    print("  - Username: root")
    print("  - Password: Mnbv@123")
    print("  - Database: healthcare_db (auto-created)")
    print()
    print("Default Admin Credentials:")
    print("  - Username: admin")
    print("  - Password: admin123")
    print()
    print("="*60)

def main():
    """Main function"""
    try:
        # Show system information
        show_system_info()
        
        # Step 1: Check and install dependencies
        print("Step 1: Checking dependencies...")
        if not check_and_install_dependencies():
            print("❌ Dependency check failed. Please resolve the issues and try again.")
            input("Press Enter to exit...")
            sys.exit(1)
        
        print()
        
        # Step 2: Setup database
        print("Step 2: Setting up database...")
        if not setup_database():
            print("❌ Database setup failed. Please check your MySQL configuration:")
            print("   - Ensure MySQL Server is running")
            print("   - Verify credentials (root/Mnbv@123)")
            print("   - Check network connectivity to localhost:3306")
            input("Press Enter to exit...")
            sys.exit(1)
        
        print()
        
        # Step 3: Start application
        print("Step 3: Starting application...")
        print("✓ Healthcare Management System is ready!")
        print()
        print("Please use the following credentials to get started:")
        print("   Admin Login - Username: admin, Password: admin123")
        print()
        
        start_application()
        
    except KeyboardInterrupt:
        print("\n\n❌ Application startup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Critical error during startup: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()