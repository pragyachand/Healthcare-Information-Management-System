"""
Create Dummy Data for Healthcare Management System
This script populates the database with sample data for testing purposes.
"""

from database.db_config import db_manager
from utils.db_utils import UserManager, AppointmentManager, PrescriptionManager, VitalsManager
import hashlib
from datetime import datetime, date, timedelta
import random

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_dummy_users():
    """Create dummy users (doctors, nurses, patients)"""
    print("Creating dummy users...")
    
    # Sample doctors
    doctors_data = [
        {
            'user': {
                'username': 'dr_smith',
                'password': hash_password('doctor123'),
                'email': 'dr.smith@hospital.com',
                'full_name': 'Dr. John Smith',
                'phone': '555-0101',
                'role': 'doctor'
            },
            'doctor_info': {
                'specialization': 'Cardiology',
                'license_number': 'MD001234',
                'department': 'Cardiology',
                'qualification': 'MD, FACC - Harvard Medical School',
                'experience_years': 15,
                'consultation_fee': 200.00
            }
        },
        {
            'user': {
                'username': 'dr_johnson',
                'password': hash_password('doctor123'),
                'email': 'dr.johnson@hospital.com',
                'full_name': 'Dr. Sarah Johnson',
                'phone': '555-0102',
                'role': 'doctor'
            },
            'doctor_info': {
                'specialization': 'Pediatrics',
                'license_number': 'MD001235',
                'department': 'Pediatrics',
                'qualification': 'MD, FAAP - Johns Hopkins University',
                'experience_years': 12,
                'consultation_fee': 180.00
            }
        },
        {
            'user': {
                'username': 'dr_williams',
                'password': hash_password('doctor123'),
                'email': 'dr.williams@hospital.com',
                'full_name': 'Dr. Michael Williams',
                'phone': '555-0103',
                'role': 'doctor'
            },
            'doctor_info': {
                'specialization': 'Orthopedics',
                'license_number': 'MD001236',
                'department': 'Orthopedics',
                'qualification': 'MD, FAAOS - Stanford University',
                'experience_years': 18,
                'consultation_fee': 250.00
            }
        },
        {
            'user': {
                'username': 'dr_brown',
                'password': hash_password('doctor123'),
                'email': 'dr.brown@hospital.com',
                'full_name': 'Dr. Emily Brown',
                'phone': '555-0104',
                'role': 'doctor'
            },
            'doctor_info': {
                'specialization': 'Dermatology',
                'license_number': 'MD001237',
                'department': 'Dermatology',
                'qualification': 'MD, AAD - UCLA Medical School',
                'experience_years': 10,
                'consultation_fee': 160.00
            }
        }
    ]
    
    # Sample nurses
    nurses_data = [
        {
            'user': {
                'username': 'nurse_davis',
                'password': hash_password('nurse123'),
                'email': 'n.davis@hospital.com',
                'full_name': 'Nancy Davis',
                'phone': '555-0201',
                'role': 'nurse'
            },
            'nurse_info': {
                'department': 'Emergency',
                'shift_type': 'Day',
                'qualification': 'BSN, RN - State University',
                'license_number': 'RN567890'
            }
        },
        {
            'user': {
                'username': 'nurse_wilson',
                'password': hash_password('nurse123'),
                'email': 'j.wilson@hospital.com',
                'full_name': 'James Wilson',
                'phone': '555-0202',
                'role': 'nurse'
            },
            'nurse_info': {
                'department': 'Pediatrics',
                'shift_type': 'Night',
                'qualification': 'ASN, RN - Community College',
                'license_number': 'RN567891'
            }
        },
        {
            'user': {
                'username': 'nurse_garcia',
                'password': hash_password('nurse123'),
                'email': 'm.garcia@hospital.com',
                'full_name': 'Maria Garcia',
                'phone': '555-0203',
                'role': 'nurse'
            },
            'nurse_info': {
                'department': 'Cardiology',
                'shift_type': 'Rotating',
                'qualification': 'BSN, RN, CCRN - Medical University',
                'license_number': 'RN567892'
            }
        }
    ]
    
    # Sample patients
    patients_data = [
        {
            'user': {
                'username': 'patient_jones',
                'password': hash_password('patient123'),
                'email': 'robert.jones@email.com',
                'full_name': 'Robert Jones',
                'phone': '555-0301',
                'role': 'patient'
            },
            'patient_info': {
                'date_of_birth': '1985-03-15',
                'gender': 'Male',
                'address': '123 Main St, Anytown, ST 12345',
                'emergency_contact': 'Linda Jones',
                'emergency_phone': '555-0311',
                'blood_group': 'A+',
                'medical_history': 'Hypertension diagnosed in 2020. Family history of heart disease.',
                'allergies': 'Penicillin, Peanuts'
            }
        },
        {
            'user': {
                'username': 'patient_taylor',
                'password': hash_password('patient123'),
                'email': 'susan.taylor@email.com',
                'full_name': 'Susan Taylor',
                'phone': '555-0302',
                'role': 'patient'
            },
            'patient_info': {
                'date_of_birth': '1992-07-22',
                'gender': 'Female',
                'address': '456 Oak Ave, Somewhere, ST 67890',
                'emergency_contact': 'David Taylor',
                'emergency_phone': '555-0312',
                'blood_group': 'B-',
                'medical_history': 'Asthma since childhood. No major surgeries.',
                'allergies': 'Shellfish, Latex'
            }
        },
        {
            'user': {
                'username': 'patient_anderson',
                'password': hash_password('patient123'),
                'email': 'mike.anderson@email.com',
                'full_name': 'Michael Anderson',
                'phone': '555-0303',
                'role': 'patient'
            },
            'patient_info': {
                'date_of_birth': '1978-11-08',
                'gender': 'Male',
                'address': '789 Pine Rd, Another City, ST 11111',
                'emergency_contact': 'Jessica Anderson',
                'emergency_phone': '555-0313',
                'blood_group': 'O+',
                'medical_history': 'Diabetes Type 2 diagnosed in 2018. Regular exercise routine.',
                'allergies': 'None known'
            }
        },
        {
            'user': {
                'username': 'patient_martinez',
                'password': hash_password('patient123'),
                'email': 'lisa.martinez@email.com',
                'full_name': 'Lisa Martinez',
                'phone': '555-0304',
                'role': 'patient'
            },
            'patient_info': {
                'date_of_birth': '1995-01-30',
                'gender': 'Female',
                'address': '321 Elm St, Different Town, ST 22222',
                'emergency_contact': 'Carlos Martinez',
                'emergency_phone': '555-0314',
                'blood_group': 'AB+',
                'medical_history': 'Migraines. Previous appendectomy in 2020.',
                'allergies': 'Aspirin, Cats'
            }
        },
        {
            'user': {
                'username': 'patient_white',
                'password': hash_password('patient123'),
                'email': 'thomas.white@email.com',
                'full_name': 'Thomas White',
                'phone': '555-0305',
                'role': 'patient'
            },
            'patient_info': {
                'date_of_birth': '1960-09-12',
                'gender': 'Male',
                'address': '654 Maple Dr, Old Town, ST 33333',
                'emergency_contact': 'Dorothy White',
                'emergency_phone': '555-0315',
                'blood_group': 'A-',
                'medical_history': 'Arthritis, High cholesterol. Previous knee replacement surgery.',
                'allergies': 'Sulfa drugs'
            }
        }
    ]
    
    # Create users
    if not db_manager.connect():
        print("✗ Failed to connect to database")
        return
    
    user_ids = {}
    
    # Create doctors
    for doctor in doctors_data:
        try:
            # Insert user
            user_query = """
            INSERT INTO users (username, password, email, full_name, phone, role) 
            VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(phone)s, %(role)s)
            """
            
            if db_manager.execute_query(user_query, doctor['user']):
                # Get user ID
                user_result = db_manager.execute_query("SELECT LAST_INSERT_ID() as user_id", fetch=True)
                user_id = user_result[0]['user_id']
                user_ids[doctor['user']['username']] = user_id
                
                # Insert doctor info
                doctor['doctor_info']['user_id'] = user_id
                doctor_query = """
                INSERT INTO doctors (user_id, specialization, license_number, 
                                   department, qualification, experience_years, consultation_fee)
                VALUES (%(user_id)s, %(specialization)s, %(license_number)s, 
                       %(department)s, %(qualification)s, %(experience_years)s, %(consultation_fee)s)
                """
                db_manager.execute_query(doctor_query, doctor['doctor_info'])
                print(f"✓ Created doctor: {doctor['user']['full_name']}")
        except Exception as e:
            print(f"✗ Failed to create doctor {doctor['user']['full_name']}: {e}")
    
    # Create nurses
    for nurse in nurses_data:
        try:
            # Insert user
            if db_manager.execute_query(user_query, nurse['user']):
                # Get user ID
                user_result = db_manager.execute_query("SELECT LAST_INSERT_ID() as user_id", fetch=True)
                user_id = user_result[0]['user_id']
                user_ids[nurse['user']['username']] = user_id
                
                # Insert nurse info
                nurse['nurse_info']['user_id'] = user_id
                nurse_query = """
                INSERT INTO nurses (user_id, department, shift_type, qualification, license_number)
                VALUES (%(user_id)s, %(department)s, %(shift_type)s, %(qualification)s, %(license_number)s)
                """
                db_manager.execute_query(nurse_query, nurse['nurse_info'])
                print(f"✓ Created nurse: {nurse['user']['full_name']}")
        except Exception as e:
            print(f"✗ Failed to create nurse {nurse['user']['full_name']}: {e}")
    
    # Create patients
    for patient in patients_data:
        try:
            # Insert user
            if db_manager.execute_query(user_query, patient['user']):
                # Get user ID
                user_result = db_manager.execute_query("SELECT LAST_INSERT_ID() as user_id", fetch=True)
                user_id = user_result[0]['user_id']
                user_ids[patient['user']['username']] = user_id
                
                # Insert patient info
                patient['patient_info']['user_id'] = user_id
                patient_query = """
                INSERT INTO patients (user_id, date_of_birth, gender, address, 
                                    emergency_contact, emergency_phone, blood_group, 
                                    medical_history, allergies)
                VALUES (%(user_id)s, %(date_of_birth)s, %(gender)s, %(address)s, 
                       %(emergency_contact)s, %(emergency_phone)s, %(blood_group)s, 
                       %(medical_history)s, %(allergies)s)
                """
                db_manager.execute_query(patient_query, patient['patient_info'])
                print(f"✓ Created patient: {patient['user']['full_name']}")
        except Exception as e:
            print(f"✗ Failed to create patient {patient['user']['full_name']}: {e}")
    
    db_manager.disconnect()
    return user_ids

def create_dummy_appointments():
    """Create dummy appointments"""
    print("\nCreating dummy appointments...")
    
    if not db_manager.connect():
        print("✗ Failed to connect to database")
        return
    
    # Get doctor and patient IDs
    doctors_query = """
    SELECT d.doctor_id, u.full_name 
    FROM doctors d 
    JOIN users u ON d.user_id = u.user_id
    """
    doctors = db_manager.execute_query(doctors_query, fetch=True)
    
    patients_query = """
    SELECT p.patient_id, u.full_name 
    FROM patients p 
    JOIN users u ON p.user_id = u.user_id
    """
    patients = db_manager.execute_query(patients_query, fetch=True)
    
    if not doctors or not patients:
        print("✗ No doctors or patients found")
        db_manager.disconnect()
        return
    
    # Sample appointments
    appointments_data = [
        {
            'doctor_id': doctors[0]['doctor_id'],  # Dr. Smith (Cardiology)
            'patient_id': patients[0]['patient_id'],  # Robert Jones
            'appointment_date': (datetime.now() + timedelta(days=7)).date(),
            'appointment_time': '09:00:00',
            'reason_for_visit': 'Regular cardiac checkup and blood pressure monitoring',
            'status': 'Scheduled'
        },
        {
            'doctor_id': doctors[1]['doctor_id'],  # Dr. Johnson (Pediatrics)
            'patient_id': patients[1]['patient_id'],  # Susan Taylor
            'appointment_date': (datetime.now() + timedelta(days=3)).date(),
            'appointment_time': '14:30:00',
            'reason_for_visit': 'Annual physical examination and vaccination',
            'status': 'Scheduled'
        },
        {
            'doctor_id': doctors[2]['doctor_id'],  # Dr. Williams (Orthopedics)
            'patient_id': patients[4]['patient_id'],  # Thomas White
            'appointment_date': (datetime.now() + timedelta(days=10)).date(),
            'appointment_time': '11:00:00',
            'reason_for_visit': 'Knee pain evaluation and arthritis management',
            'status': 'Scheduled'
        },
        {
            'doctor_id': doctors[0]['doctor_id'],  # Dr. Smith
            'patient_id': patients[2]['patient_id'],  # Michael Anderson
            'appointment_date': (datetime.now() - timedelta(days=5)).date(),
            'appointment_time': '10:30:00',
            'reason_for_visit': 'Diabetes management and cardiac risk assessment',
            'status': 'Completed'
        },
        {
            'doctor_id': doctors[3]['doctor_id'],  # Dr. Brown (Dermatology)
            'patient_id': patients[3]['patient_id'],  # Lisa Martinez
            'appointment_date': (datetime.now() + timedelta(days=14)).date(),
            'appointment_time': '15:00:00',
            'reason_for_visit': 'Skin condition evaluation and treatment',
            'status': 'Scheduled'
        },
        {
            'doctor_id': doctors[1]['doctor_id'],  # Dr. Johnson
            'patient_id': patients[1]['patient_id'],  # Susan Taylor
            'appointment_date': (datetime.now() - timedelta(days=30)).date(),
            'appointment_time': '13:00:00',
            'reason_for_visit': 'Asthma follow-up and inhaler adjustment',
            'status': 'Completed'
        }
    ]
    
    appointment_query = """
    INSERT INTO appointments (doctor_id, patient_id, appointment_date, appointment_time, reason_for_visit, status)
    VALUES (%(doctor_id)s, %(patient_id)s, %(appointment_date)s, %(appointment_time)s, %(reason_for_visit)s, %(status)s)
    """
    
    for appointment in appointments_data:
        try:
            if db_manager.execute_query(appointment_query, appointment):
                print(f"✓ Created appointment: {appointment['appointment_date']} at {appointment['appointment_time']}")
        except Exception as e:
            print(f"✗ Failed to create appointment: {e}")
    
    db_manager.disconnect()

def create_dummy_prescriptions():
    """Create dummy prescriptions"""
    print("\nCreating dummy prescriptions...")
    
    if not db_manager.connect():
        print("✗ Failed to connect to database")
        return
    
    # Get doctor and patient IDs
    doctors_query = """
    SELECT d.doctor_id, u.full_name 
    FROM doctors d 
    JOIN users u ON d.user_id = u.user_id
    """
    doctors = db_manager.execute_query(doctors_query, fetch=True)
    
    patients_query = """
    SELECT p.patient_id, u.full_name 
    FROM patients p 
    JOIN users u ON p.user_id = u.user_id
    """
    patients = db_manager.execute_query(patients_query, fetch=True)
    
    if not doctors or not patients:
        print("✗ No doctors or patients found")
        db_manager.disconnect()
        return
    
    # Sample prescriptions
    prescriptions_data = [
        {
            'doctor_id': doctors[0]['doctor_id'],  # Dr. Smith
            'patient_id': patients[0]['patient_id'],  # Robert Jones
            'prescription_date': (datetime.now() - timedelta(days=5)).date(),
            'diagnosis': 'Hypertension (Essential)',
            'medications': 'Lisinopril 10mg tablets\nAmlodipine 5mg tablets\nHydrochlorothiazide 25mg tablets',
            'dosage_instructions': 'Lisinopril: Take 1 tablet once daily in the morning\nAmlodipine: Take 1 tablet once daily\nHydrochlorothiazide: Take 1 tablet once daily with breakfast\n\nMonitor blood pressure daily and maintain a log.',
            'status': 'Active'
        },
        {
            'doctor_id': doctors[1]['doctor_id'],  # Dr. Johnson
            'patient_id': patients[1]['patient_id'],  # Susan Taylor
            'prescription_date': (datetime.now() - timedelta(days=30)).date(),
            'diagnosis': 'Asthma (Persistent)',
            'medications': 'Albuterol inhaler 90mcg\nFluticasone propionate inhaler 44mcg\nMontelukast 10mg tablets',
            'dosage_instructions': 'Albuterol: Use 2 puffs as needed for shortness of breath (rescue inhaler)\nFluticasone: Use 2 puffs twice daily (morning and evening)\nMontelukast: Take 1 tablet once daily at bedtime\n\nRinse mouth after inhaler use.',
            'status': 'Active'
        },
        {
            'doctor_id': doctors[0]['doctor_id'],  # Dr. Smith
            'patient_id': patients[2]['patient_id'],  # Michael Anderson
            'prescription_date': (datetime.now() - timedelta(days=10)).date(),
            'diagnosis': 'Type 2 Diabetes Mellitus with Hypertension',
            'medications': 'Metformin 500mg tablets\nGlipizide 5mg tablets\nLosartan 50mg tablets\nAtorvastatin 20mg tablets',
            'dosage_instructions': 'Metformin: Take 1 tablet twice daily with meals\nGlipizide: Take 1 tablet once daily before breakfast\nLosartan: Take 1 tablet once daily\nAtorvastatin: Take 1 tablet once daily at bedtime\n\nMonitor blood glucose levels regularly.',
            'status': 'Active'
        },
        {
            'doctor_id': doctors[3]['doctor_id'],  # Dr. Brown
            'patient_id': patients[3]['patient_id'],  # Lisa Martinez
            'prescription_date': (datetime.now() - timedelta(days=2)).date(),
            'diagnosis': 'Acute Migraine',
            'medications': 'Sumatriptan 50mg tablets\nIbuprofen 400mg tablets\nOndansetron 4mg tablets',
            'dosage_instructions': 'Sumatriptan: Take 1 tablet at onset of migraine, may repeat once after 2 hours if needed\nIbuprofen: Take 1 tablet every 6-8 hours as needed for pain\nOndansetron: Take 1 tablet as needed for nausea\n\nAvoid known triggers, maintain regular sleep schedule.',
            'status': 'Active'
        },
        {
            'doctor_id': doctors[2]['doctor_id'],  # Dr. Williams
            'patient_id': patients[4]['patient_id'],  # Thomas White
            'prescription_date': (datetime.now() - timedelta(days=7)).date(),
            'diagnosis': 'Osteoarthritis of Knee',
            'medications': 'Celecoxib 200mg capsules\nGlucosamine 1500mg tablets\nTopical diclofenac gel 1%',
            'dosage_instructions': 'Celecoxib: Take 1 capsule once daily with food\nGlucosamine: Take 1 tablet once daily\nDiclofenac gel: Apply thin layer to affected knee 3-4 times daily\n\nPhysical therapy recommended 2-3 times weekly.',
            'status': 'Active'
        }
    ]
    
    prescription_query = """
    INSERT INTO prescriptions (doctor_id, patient_id, prescription_date, diagnosis, medications, dosage_instructions, status)
    VALUES (%(doctor_id)s, %(patient_id)s, %(prescription_date)s, %(diagnosis)s, %(medications)s, %(dosage_instructions)s, %(status)s)
    """
    
    for prescription in prescriptions_data:
        try:
            if db_manager.execute_query(prescription_query, prescription):
                print(f"✓ Created prescription for {prescription['diagnosis']}")
        except Exception as e:
            print(f"✗ Failed to create prescription: {e}")
    
    db_manager.disconnect()

def create_dummy_vitals():
    """Create dummy vital signs records"""
    print("\nCreating dummy vital signs...")
    
    if not db_manager.connect():
        print("✗ Failed to connect to database")
        return
    
    # Get patient IDs
    patients_query = """
    SELECT p.patient_id, u.full_name 
    FROM patients p 
    JOIN users u ON p.user_id = u.user_id
    """
    patients = db_manager.execute_query(patients_query, fetch=True)
    
    if not patients:
        print("✗ No patients found")
        db_manager.disconnect()
        return
    
    # Sample vital signs for multiple dates
    vitals_data = []
    
    for patient in patients:
        # Create vitals for the last 30 days (every few days)
        for days_back in [1, 5, 10, 15, 20, 30]:
            record_date = datetime.now() - timedelta(days=days_back)
            
            # Generate realistic vitals based on patient condition
            if patient['patient_id'] == 1:  # Robert Jones (Hypertension)
                systolic = random.randint(140, 160)
                diastolic = random.randint(85, 95)
                heart_rate = random.randint(70, 85)
            elif patient['patient_id'] == 3:  # Michael Anderson (Diabetes)
                systolic = random.randint(130, 145)
                diastolic = random.randint(80, 90)
                heart_rate = random.randint(75, 90)
            else:  # Normal patients
                systolic = random.randint(110, 130)
                diastolic = random.randint(70, 85)
                heart_rate = random.randint(65, 80)
            
            vitals_data.append({
                'patient_id': patient['patient_id'],
                'recorded_by': 1,  # Assuming admin user records vitals
                'recorded_at': record_date,
                'temperature': round(random.uniform(97.8, 99.2), 1),
                'blood_pressure_systolic': systolic,
                'blood_pressure_diastolic': diastolic,
                'heart_rate': heart_rate,
                'oxygen_saturation': random.randint(96, 100),
                'weight': round(random.uniform(120, 220), 1),
                'height': round(random.uniform(60, 75), 1),
                'notes': f'Routine vital signs check - Patient stable'
            })
    
    vitals_query = """
    INSERT INTO vitals (patient_id, recorded_by, recorded_at, temperature, 
                       blood_pressure_systolic, blood_pressure_diastolic, heart_rate, 
                       oxygen_saturation, weight, height, notes)
    VALUES (%(patient_id)s, %(recorded_by)s, %(recorded_at)s, %(temperature)s, 
           %(blood_pressure_systolic)s, %(blood_pressure_diastolic)s, %(heart_rate)s, 
           %(oxygen_saturation)s, %(weight)s, %(height)s, %(notes)s)
    """
    
    for vital in vitals_data:
        try:
            if db_manager.execute_query(vitals_query, vital):
                pass  # Don't print each one to avoid spam
        except Exception as e:
            print(f"✗ Failed to create vital record: {e}")
    
    print(f"✓ Created {len(vitals_data)} vital signs records")
    db_manager.disconnect()

def main():
    """Main function to create all dummy data"""
    print("=" * 60)
    print("CREATING DUMMY DATA FOR HEALTHCARE MANAGEMENT SYSTEM")
    print("=" * 60)
    
    print("This will create sample data including:")
    print("- 4 Doctors (Cardiology, Pediatrics, Orthopedics, Dermatology)")
    print("- 3 Nurses (Emergency, Pediatrics, Cardiology)")
    print("- 5 Patients with medical histories")
    print("- Sample appointments (past and future)")
    print("- Active prescriptions with medications")
    print("- Vital signs records")
    print()
    
    # Check if we should proceed
    proceed = input("Do you want to proceed? (y/n): ").lower().strip()
    if proceed != 'y':
        print("Operation cancelled.")
        return
    
    try:
        # Create users first
        create_dummy_users()
        
        # Create appointments
        create_dummy_appointments()
        
        # Create prescriptions
        create_dummy_prescriptions()
        
        # Create vital signs
        create_dummy_vitals()
        
        print("\n" + "=" * 60)
        print("DUMMY DATA CREATION COMPLETED!")
        print("=" * 60)
        print()
        print("Sample Login Credentials:")
        print("Doctors:")
        print("  - Username: dr_smith,    Password: doctor123  (Cardiology)")
        print("  - Username: dr_johnson,  Password: doctor123  (Pediatrics)")
        print("  - Username: dr_williams, Password: doctor123  (Orthopedics)")
        print("  - Username: dr_brown,    Password: doctor123  (Dermatology)")
        print()
        print("Nurses:")
        print("  - Username: nurse_davis,   Password: nurse123   (Emergency)")
        print("  - Username: nurse_wilson,  Password: nurse123   (Pediatrics)")
        print("  - Username: nurse_garcia,  Password: nurse123   (Cardiology)")
        print()
        print("Patients:")
        print("  - Username: patient_jones,     Password: patient123")
        print("  - Username: patient_taylor,    Password: patient123")
        print("  - Username: patient_anderson,  Password: patient123")
        print("  - Username: patient_martinez,  Password: patient123")
        print("  - Username: patient_white,     Password: patient123")
        print()
        print("Admin:")
        print("  - Username: admin,       Password: admin123")
        print()
        print("You can now test the system with realistic data!")
        
    except Exception as e:
        print(f"\n✗ Error creating dummy data: {e}")

if __name__ == "__main__":
    main()