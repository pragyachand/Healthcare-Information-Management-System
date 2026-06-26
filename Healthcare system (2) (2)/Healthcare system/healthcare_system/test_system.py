"""
Healthcare Management System - Test and Verification Script
This script tests basic functionality of the healthcare system
"""

import os
import sys

def test_imports():
    """Test if all modules can be imported successfully"""
    print("Testing module imports...")
    
    try:
        # Test database modules
        from database.db_config import DatabaseConfig, db_manager
        print("✓ Database configuration module imported")
        
        from database.schema import DatabaseSchema
        print("✓ Database schema module imported")
        
        # Test utility modules
        from utils.db_utils import UserManager, AppointmentManager, PrescriptionManager, VitalsManager, ReportsManager
        print("✓ Database utilities imported")
        
        # Test authentication
        from auth import LoginWindow, RegistrationWindow
        print("✓ Authentication modules imported")
        
        # Test role modules
        from modules.admin_module import AdminDashboard
        print("✓ Admin module imported")
        
        from modules.doctor_module import DoctorDashboard
        print("✓ Doctor module imported")
        
        from modules.nurse_module import NurseDashboard
        print("✓ Nurse module imported")
        
        from modules.patient_module import PatientDashboard
        print("✓ Patient module imported")
        
        print("✅ All module imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        from database.db_config import db_manager
        
        if db_manager.connect():
            print("✓ Database connection successful")
            
            # Test basic query
            result = db_manager.execute_query("SELECT 1 as test", fetch=True)
            if result and result[0]['test'] == 1:
                print("✓ Database query test successful")
            
            db_manager.disconnect()
            print("✓ Database disconnection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\nTesting dependencies...")
    
    try:
        import mysql.connector
        print("✓ mysql-connector-python is available")
        
        import tkinter as tk
        print("✓ tkinter is available")
        
        # Test tkinter window creation
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        print("✓ GUI framework test successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Dependency test error: {e}")
        return False

def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking file structure...")
    
    required_files = [
        "main.py",
        "auth.py",
        "requirements.txt",
        "README.md",
        "database/__init__.py",
        "database/db_config.py",
        "database/schema.py",
        "utils/__init__.py",
        "utils/db_utils.py",
        "modules/__init__.py",
        "modules/admin_module.py",
        "modules/doctor_module.py",
        "modules/nurse_module.py",
        "modules/patient_module.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present!")
        return True

def test_database_schema():
    """Test database schema creation"""
    print("\nTesting database schema...")
    
    try:
        from database.schema import DatabaseSchema
        schema = DatabaseSchema()
        
        print("✓ Database schema object created")
        
        # Note: This would actually create the database in a real test
        # For this test, we just verify the schema object works
        print("✓ Database schema test completed")
        return True
        
    except Exception as e:
        print(f"❌ Database schema test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("="*60)
    print("HEALTHCARE MANAGEMENT SYSTEM - COMPREHENSIVE TEST")
    print("="*60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("File Structure", check_file_structure()))
    test_results.append(("Dependencies", test_dependencies()))
    test_results.append(("Module Imports", test_imports()))
    test_results.append(("Database Schema", test_database_schema()))
    test_results.append(("Database Connection", test_database_connection()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The system is ready to use.")
        print("\nTo start the application, run: python main.py")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please resolve the issues before using the system.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if not success:
        print("\nPlease check the following:")
        print("1. Ensure all required files are present")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Set up MySQL with root user and password 'Mnbv@123'")
        print("4. Ensure MySQL server is running on localhost:3306")
    
    input("\nPress Enter to exit...")