"""
Database Utilities - CRUD Operations
Healthcare Management System
"""

from database.db_config import db_manager
from datetime import datetime, date
import hashlib

class UserManager:
    """User management operations"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user login"""
        if not db_manager.connect():
            return None
        
        hashed_password = UserManager.hash_password(password)
        
        query = """
        SELECT u.*, 
               CASE 
                   WHEN u.role = 'patient' THEN p.patient_id
                   WHEN u.role = 'doctor' THEN d.doctor_id
                   WHEN u.role = 'nurse' THEN n.nurse_id
                   ELSE NULL
               END as role_id
        FROM users u
        LEFT JOIN patients p ON u.user_id = p.user_id
        LEFT JOIN doctors d ON u.user_id = d.user_id
        LEFT JOIN nurses n ON u.user_id = n.user_id
        WHERE u.username = %s AND u.password = %s AND u.is_active = TRUE
        """
        
        result = db_manager.execute_query(query, (username, hashed_password), fetch=True)
        db_manager.disconnect()
        
        return result[0] if result else None
    
    @staticmethod
    def create_user(user_data, role_specific_data=None):
        """Create a new user with role-specific data"""
        if not db_manager.connect():
            return False
        
        try:
            # Hash password
            user_data['password'] = UserManager.hash_password(user_data['password'])
            
            # Insert user
            user_query = """
            INSERT INTO users (username, password, email, full_name, phone, role) 
            VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(phone)s, %(role)s)
            """
            
            if not db_manager.execute_query(user_query, user_data):
                return False
            
            # Get the inserted user ID
            user_id_query = "SELECT LAST_INSERT_ID() as user_id"
            user_result = db_manager.execute_query(user_id_query, fetch=True)
            user_id = user_result[0]['user_id']
            
            # Insert role-specific data
            if role_specific_data and user_data['role'] != 'admin':
                role_specific_data['user_id'] = user_id
                
                if user_data['role'] == 'patient':
                    patient_query = """
                    INSERT INTO patients (user_id, date_of_birth, gender, address, 
                                        emergency_contact, emergency_phone, blood_group, 
                                        medical_history, allergies)
                    VALUES (%(user_id)s, %(date_of_birth)s, %(gender)s, %(address)s, 
                           %(emergency_contact)s, %(emergency_phone)s, %(blood_group)s, 
                           %(medical_history)s, %(allergies)s)
                    """
                    db_manager.execute_query(patient_query, role_specific_data)
                
                elif user_data['role'] == 'doctor':
                    doctor_query = """
                    INSERT INTO doctors (user_id, specialization, license_number, 
                                       department, qualification, experience_years, consultation_fee)
                    VALUES (%(user_id)s, %(specialization)s, %(license_number)s, 
                           %(department)s, %(qualification)s, %(experience_years)s, %(consultation_fee)s)
                    """
                    db_manager.execute_query(doctor_query, role_specific_data)
                
                elif user_data['role'] == 'nurse':
                    nurse_query = """
                    INSERT INTO nurses (user_id, department, shift_type, qualification, license_number)
                    VALUES (%(user_id)s, %(department)s, %(shift_type)s, %(qualification)s, %(license_number)s)
                    """
                    db_manager.execute_query(nurse_query, role_specific_data)
            
            db_manager.disconnect()
            return True
            
        except Exception as e:
            print(f"Error creating user: {e}")
            db_manager.disconnect()
            return False
    
    @staticmethod
    def update_user_profile(user_id, update_data):
        """Update user profile"""
        if not db_manager.connect():
            return False
        
        # Build dynamic update query
        set_clauses = []
        params = {}
        
        for key, value in update_data.items():
            if key != 'user_id' and value is not None:
                set_clauses.append(f"{key} = %({key})s")
                params[key] = value
        
        if not set_clauses:
            return True
        
        params['user_id'] = user_id
        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = %(user_id)s"
        
        result = db_manager.execute_query(query, params)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_all_users(role=None):
        """Get all users, optionally filtered by role"""
        if not db_manager.connect():
            return []
        
        query = "SELECT * FROM users WHERE is_active = TRUE"
        params = None
        
        if role:
            query += " AND role = %s"
            params = (role,)
        
        query += " ORDER BY full_name"
        
        result = db_manager.execute_query(query, params, fetch=True)
        db_manager.disconnect()
        return result or []

class AppointmentManager:
    """Appointment management operations"""
    
    @staticmethod
    def create_appointment(appointment_data):
        """Create a new appointment"""
        if not db_manager.connect():
            return False
        
        query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, 
                                appointment_time, reason_for_visit, notes)
        VALUES (%(patient_id)s, %(doctor_id)s, %(appointment_date)s, 
                %(appointment_time)s, %(reason_for_visit)s, %(notes)s)
        """
        
        result = db_manager.execute_query(query, appointment_data)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_appointments(patient_id=None, doctor_id=None, date_filter=None, status=None):
        """Get appointments with various filters"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT a.*, 
               u_patient.full_name as patient_name,
               u_doctor.full_name as doctor_name,
               d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN users u_patient ON p.user_id = u_patient.user_id
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN users u_doctor ON doc.user_id = u_doctor.user_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE 1=1
        """
        
        params = []
        
        if patient_id:
            query += " AND a.patient_id = %s"
            params.append(patient_id)
        
        if doctor_id:
            query += " AND a.doctor_id = %s"
            params.append(doctor_id)
        
        if date_filter:
            query += " AND a.appointment_date = %s"
            params.append(date_filter)
        
        if status:
            query += " AND a.status = %s"
            params.append(status)
        
        query += " ORDER BY a.appointment_date, a.appointment_time"
        
        result = db_manager.execute_query(query, params, fetch=True)
        db_manager.disconnect()
        return result or []
    
    @staticmethod
    def update_appointment_status(appointment_id, status, notes=None):
        """Update appointment status"""
        if not db_manager.connect():
            return False
        
        query = "UPDATE appointments SET status = %s"
        params = [status]
        
        if notes:
            query += ", notes = %s"
            params.append(notes)
        
        query += " WHERE appointment_id = %s"
        params.append(appointment_id)
        
        result = db_manager.execute_query(query, params)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def update_appointment(appointment_id, update_data):
        """Update appointment details"""
        if not db_manager.connect():
            return False
        
        # Build dynamic query based on provided fields
        set_clauses = []
        params = []
        
        for field, value in update_data.items():
            if value is not None:
                set_clauses.append(f"{field} = %s")
                params.append(value)
        
        if not set_clauses:
            return False
        
        query = f"UPDATE appointments SET {', '.join(set_clauses)} WHERE appointment_id = %s"
        params.append(appointment_id)
        
        result = db_manager.execute_query(query, params)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_all_appointments(date_filter=None, status=None):
        """Get ALL appointments in the system (for nurses)"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT a.*, 
               u_patient.full_name as patient_name,
               u_doctor.full_name as doctor_name,
               d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN users u_patient ON p.user_id = u_patient.user_id
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN users u_doctor ON doc.user_id = u_doctor.user_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE 1=1
        """
        
        params = []
        
        if date_filter:
            query += " AND a.appointment_date = %s"
            params.append(date_filter)
        
        if status:
            query += " AND a.status = %s"
            params.append(status)
        
        query += " ORDER BY a.appointment_date, a.appointment_time"
        
        result = db_manager.execute_query(query, params, fetch=True)
        db_manager.disconnect()
        return result or []
    
    @staticmethod
    def check_appointment_conflict(doctor_id, appointment_date, appointment_time, exclude_appointment_id=None):
        """
        Check if an appointment conflicts with existing appointments (30-minute buffer).
        Returns (has_conflict, conflicting_appointments, suggested_times)
        """
        if not db_manager.connect():
            return True, [], []
        
        from datetime import datetime, timedelta
        
        try:
            # Convert appointment_date to date object if it's a string
            if isinstance(appointment_date, str):
                appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            else:
                appointment_date_obj = appointment_date
            
            # Normalize appointment_time to HH:MM:SS format if needed
            if isinstance(appointment_time, str):
                if len(appointment_time) == 5:  # HH:MM format
                    appointment_time = appointment_time + ":00"  # Convert to HH:MM:SS
                appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M:%S")
            else:
                appointment_datetime = datetime.combine(appointment_date_obj, appointment_time)
            
            # Calculate 30-minute window (before and after)
            start_buffer = appointment_datetime - timedelta(minutes=30)
            end_buffer = appointment_datetime + timedelta(minutes=30)
            
            # Query for conflicting appointments - get all appointments for the doctor on that date
            query = """
            SELECT a.appointment_id, a.appointment_time, a.status,
                   u.full_name as patient_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN users u ON p.user_id = u.user_id
            WHERE a.doctor_id = %s 
            AND a.appointment_date = %s
            AND a.status IN ('Scheduled', 'Confirmed')
            """
            
            # Use string format for database query
            appointment_date_str = appointment_date if isinstance(appointment_date, str) else appointment_date.strftime("%Y-%m-%d")
            params = [doctor_id, appointment_date_str]
            
            # Exclude current appointment if editing
            if exclude_appointment_id:
                query += " AND a.appointment_id != %s"
                params.append(exclude_appointment_id)
            
            all_appointments = db_manager.execute_query(query, params, fetch=True) or []
            
            # Check each appointment for time conflicts
            conflicting_appointments = []
            appointment_date_str = appointment_date if isinstance(appointment_date, str) else appointment_date.strftime("%Y-%m-%d")
            for apt in all_appointments:
                # Convert appointment time to datetime for comparison
                apt_time_str = str(apt['appointment_time'])
                if len(apt_time_str) == 8:  # Already HH:MM:SS format
                    apt_datetime = datetime.strptime(f"{appointment_date_str} {apt_time_str}", "%Y-%m-%d %H:%M:%S")
                elif len(apt_time_str) == 5:  # HH:MM format
                    apt_datetime = datetime.strptime(f"{appointment_date_str} {apt_time_str}:00", "%Y-%m-%d %H:%M:%S")
                else:
                    # Handle datetime object
                    apt_datetime = datetime.combine(appointment_date_obj, apt['appointment_time'])
                
                # Check if within 30-minute buffer
                time_diff = abs((appointment_datetime - apt_datetime).total_seconds())
                if time_diff < 30 * 60:  # 30 minutes in seconds
                    conflicting_appointments.append(apt)
            
            # Generate suggested alternative times if there's a conflict
            suggested_times = []
            if conflicting_appointments:
                suggested_times = AppointmentManager._generate_suggested_times(
                    doctor_id, appointment_date, appointment_datetime
                )
            
            db_manager.disconnect()
            return len(conflicting_appointments) > 0, conflicting_appointments, suggested_times
            
        except Exception as e:
            print(f"Error checking appointment conflict: {e}")
            db_manager.disconnect()
            return True, [], []
    
    @staticmethod
    def _generate_suggested_times(doctor_id, appointment_date, requested_time):
        """Generate alternative appointment time suggestions"""
        from datetime import datetime, timedelta
        
        suggestions = []
        
        # Convert appointment_date to date object if it's a string
        if isinstance(appointment_date, str):
            appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        else:
            appointment_date_obj = appointment_date
        
        # Get all existing appointments for the doctor on that date
        if not db_manager.connect():
            return suggestions
        
        query = """
        SELECT appointment_time
        FROM appointments
        WHERE doctor_id = %s AND appointment_date = %s
        AND status IN ('Scheduled', 'Confirmed')
        ORDER BY appointment_time
        """
        
        # Use string format for database query
        appointment_date_str = appointment_date if isinstance(appointment_date, str) else appointment_date.strftime("%Y-%m-%d")
        existing_appointments = db_manager.execute_query(query, (doctor_id, appointment_date_str), fetch=True) or []
        db_manager.disconnect()
        
        # Convert to list of datetime objects
        busy_times = []
        for apt in existing_appointments:
            # Handle different time formats
            apt_time_str = str(apt['appointment_time'])
            
            if len(apt_time_str) == 8:  # HH:MM:SS format
                time_obj = datetime.strptime(apt_time_str, "%H:%M:%S").time()
            elif len(apt_time_str) == 5:  # HH:MM format
                time_obj = datetime.strptime(apt_time_str, "%H:%M").time()
            else:
                # Handle datetime object
                if hasattr(apt['appointment_time'], 'hour'):
                    time_obj = apt['appointment_time']
                else:
                    continue  # Skip if we can't parse the time
            
            busy_times.append(datetime.combine(appointment_date_obj, time_obj))
        
        # Generate suggestions (next 3 available slots)
        current_time = requested_time
        suggestions_count = 0
        
        while suggestions_count < 3:
            # Try next 30-minute slot
            current_time += timedelta(minutes=30)
            
            # Skip if outside working hours (8 AM to 6 PM)
            if current_time.hour < 8 or current_time.hour >= 18:
                # Move to next day 8 AM if past working hours
                next_day = current_time.date() + timedelta(days=1)
                current_time = datetime.combine(next_day, datetime.strptime("08:00", "%H:%M").time())
                continue
            
            # Check if this slot conflicts with existing appointments
            conflicts = False
            for busy_time in busy_times:
                if abs((current_time - busy_time).total_seconds()) < 30 * 60:  # 30 minutes buffer
                    conflicts = True
                    break
            
            if not conflicts:
                suggestions.append(current_time.strftime("%H:%M"))
                suggestions_count += 1
        
        return suggestions
    
    @staticmethod
    def get_available_time_slots(doctor_id, appointment_date):
        """Get all available time slots for a doctor on a specific date"""
        if not db_manager.connect():
            return []
        
        from datetime import datetime, timedelta
        
        # Convert appointment_date to date object if it's a string
        if isinstance(appointment_date, str):
            appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        else:
            appointment_date_obj = appointment_date
        
        # Get existing appointments
        query = """
        SELECT appointment_time
        FROM appointments
        WHERE doctor_id = %s AND appointment_date = %s
        AND status IN ('Scheduled', 'Confirmed')
        """
        
        # Use string format for database query
        appointment_date_str = appointment_date if isinstance(appointment_date, str) else appointment_date.strftime("%Y-%m-%d")
        existing_appointments = db_manager.execute_query(query, (doctor_id, appointment_date_str), fetch=True) or []
        db_manager.disconnect()
        
        # Generate all possible time slots (8 AM to 6 PM, every 30 minutes)
        all_slots = []
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("18:00", "%H:%M")
        
        current_slot = start_time
        while current_slot < end_time:
            all_slots.append(current_slot.strftime("%H:%M"))
            current_slot += timedelta(minutes=30)
        
        # Remove busy slots (with 30-minute buffer)
        available_slots = []
        for slot in all_slots:
            slot_time = datetime.strptime(slot, "%H:%M")
            
            is_available = True
            for appointment in existing_appointments:
                # Handle different time formats
                apt_time_str = str(appointment['appointment_time'])
                
                if len(apt_time_str) == 8:  # HH:MM:SS format
                    apt_time = datetime.strptime(apt_time_str, "%H:%M:%S")
                elif len(apt_time_str) == 5:  # HH:MM format
                    apt_time = datetime.strptime(apt_time_str, "%H:%M")
                else:
                    # Handle datetime object
                    if hasattr(appointment['appointment_time'], 'hour'):
                        apt_time = datetime.combine(appointment_date_obj, appointment['appointment_time'])
                        apt_time = datetime.strptime(apt_time.strftime("%H:%M"), "%H:%M")
                    else:
                        continue  # Skip if we can't parse the time
                
                # Check if within 30-minute buffer
                time_diff = abs((slot_time - apt_time).total_seconds())
                if time_diff < 30 * 60:  # 30 minutes
                    is_available = False
                    break
            
            if is_available:
                available_slots.append(slot)
        
        return available_slots

class PrescriptionManager:
    """Prescription management operations"""
    
    @staticmethod
    def create_prescription(prescription_data):
        """Create a new prescription"""
        if not db_manager.connect():
            return False
        
        query = """
        INSERT INTO prescriptions (patient_id, doctor_id, appointment_id, 
                                 prescription_date, diagnosis, medications, 
                                 dosage_instructions, notes)
        VALUES (%(patient_id)s, %(doctor_id)s, %(appointment_id)s, 
                %(prescription_date)s, %(diagnosis)s, %(medications)s, 
                %(dosage_instructions)s, %(notes)s)
        """
        
        result = db_manager.execute_query(query, prescription_data)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_prescriptions(patient_id=None, doctor_id=None, status='Active'):
        """Get prescriptions with filters"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT p.*, 
               u_patient.full_name as patient_name,
               u_doctor.full_name as doctor_name
        FROM prescriptions p
        JOIN patients pat ON p.patient_id = pat.patient_id
        JOIN users u_patient ON pat.user_id = u_patient.user_id
        JOIN doctors d ON p.doctor_id = d.doctor_id
        JOIN users u_doctor ON d.user_id = u_doctor.user_id
        WHERE 1=1
        """
        
        params = []
        
        if patient_id:
            query += " AND p.patient_id = %s"
            params.append(patient_id)
        
        if doctor_id:
            query += " AND p.doctor_id = %s"
            params.append(doctor_id)
        
        if status:
            query += " AND p.status = %s"
            params.append(status)
        
        query += " ORDER BY p.prescription_date DESC"
        
        result = db_manager.execute_query(query, params, fetch=True)
        db_manager.disconnect()
        return result or []
    
    @staticmethod
    def update_prescription(prescription_id, update_data):
        """Update prescription"""
        if not db_manager.connect():
            return False
        
        set_clauses = []
        params = {}
        
        for key, value in update_data.items():
            if key != 'prescription_id' and value is not None:
                set_clauses.append(f"{key} = %({key})s")
                params[key] = value
        
        if not set_clauses:
            return True
        
        params['prescription_id'] = prescription_id
        query = f"UPDATE prescriptions SET {', '.join(set_clauses)} WHERE prescription_id = %(prescription_id)s"
        
        result = db_manager.execute_query(query, params)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_all_prescriptions(status=None):
        """Get ALL prescriptions in the system (for nurses)"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT p.*, 
               u_patient.full_name as patient_name,
               u_doctor.full_name as doctor_name
        FROM prescriptions p
        JOIN patients pat ON p.patient_id = pat.patient_id
        JOIN users u_patient ON pat.user_id = u_patient.user_id
        JOIN doctors d ON p.doctor_id = d.doctor_id
        JOIN users u_doctor ON d.user_id = u_doctor.user_id
        WHERE 1=1
        """
        
        params = []
        
        if status and status != "All":
            query += " AND p.status = %s"
            params.append(status)
        
        query += " ORDER BY p.prescription_date DESC"
        
        result = db_manager.execute_query(query, params, fetch=True)
        db_manager.disconnect()
        return result or []

class VitalsManager:
    """Patient vitals management"""
    
    @staticmethod
    def record_vitals(vitals_data):
        """Record patient vitals"""
        if not db_manager.connect():
            return False
        
        query = """
        INSERT INTO vitals (patient_id, recorded_by, blood_pressure_systolic, 
                          blood_pressure_diastolic, heart_rate, temperature, 
                          weight, height, oxygen_saturation, notes)
        VALUES (%(patient_id)s, %(recorded_by)s, %(blood_pressure_systolic)s, 
                %(blood_pressure_diastolic)s, %(heart_rate)s, %(temperature)s, 
                %(weight)s, %(height)s, %(oxygen_saturation)s, %(notes)s)
        """
        
        result = db_manager.execute_query(query, vitals_data)
        db_manager.disconnect()
        return result
    
    @staticmethod
    def get_patient_vitals(patient_id, limit=10):
        """Get patient vitals history"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT v.*, u.full_name as recorded_by_name
        FROM vitals v
        JOIN users u ON v.recorded_by = u.user_id
        WHERE v.patient_id = %s
        ORDER BY v.recorded_at DESC
        LIMIT %s
        """
        
        result = db_manager.execute_query(query, (patient_id, limit), fetch=True)
        db_manager.disconnect()
        return result or []

class ReportsManager:
    """Generate various reports"""
    
    @staticmethod
    def get_doctor_patient_count():
        """Get patient count per doctor"""
        if not db_manager.connect():
            return []
        
        query = """
        SELECT u.full_name as doctor_name, d.specialization,
               COUNT(DISTINCT a.patient_id) as patient_count
        FROM doctors d
        JOIN users u ON d.user_id = u.user_id
        LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, u.full_name, d.specialization
        ORDER BY patient_count DESC
        """
        
        result = db_manager.execute_query(query, fetch=True)
        db_manager.disconnect()
        return result or []
    
    @staticmethod
    def get_system_stats():
        """Get system statistics"""
        if not db_manager.connect():
            return {}
        
        stats = {}
        
        # Count queries
        queries = {
            'total_patients': "SELECT COUNT(*) as count FROM patients",
            'total_doctors': "SELECT COUNT(*) as count FROM doctors",
            'total_nurses': "SELECT COUNT(*) as count FROM nurses",
            'active_prescriptions': "SELECT COUNT(*) as count FROM prescriptions WHERE status = 'Active'"
        }
        
        for key, query in queries.items():
            result = db_manager.execute_query(query, fetch=True)
            stats[key] = result[0]['count'] if result else 0
        
        db_manager.disconnect()
        return stats