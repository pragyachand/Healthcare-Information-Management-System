"""
Nurse Module - Nurse Dashboard and Functionality
Healthcare Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modules.doctor_module import DoctorDashboard

class NurseDashboard(DoctorDashboard):
    """Nurse dashboard using the same professional interface as doctors"""
    
    def __init__(self, user_data, parent_window):
        # Simply initialize with doctor's professional interface
        super().__init__(user_data, parent_window)
        
        # Update window title for nurse
        self.root.title(f"Nurse Dashboard - {user_data['full_name']}")
        
        # Store nurse-specific ID (same logic as doctor)
        self.nurse_id = user_data.get('role_id')
        self.doctor_id = self.nurse_id  # Use same database logic as doctor module
    
    def create_dashboard(self):
        """Create the nurse dashboard with customized header and tabs"""
        # Call parent's create_dashboard first
        super().create_dashboard()
        
        # Now customize the header for nurse
        self.customize_header_for_nurse()
        
        # Customize tabs for nurse workflow
        self.customize_tabs_for_nurse()
    
    def customize_tabs_for_nurse(self):
        """Customize tabs to be appropriate for nurses"""
        # Remove "My Patients" tab since nurses don't own patients
        try:
            # Find the "My Patients" tab and hide it
            for i in range(self.notebook.index("end")):
                tab_text = self.notebook.tab(i, "text")
                if "My Patients" in tab_text:
                    self.notebook.forget(i)
                    break
        except:
            pass  # If tab doesn't exist or error occurs, continue
        
        # Optionally rename "Prescriptions" to "View Prescriptions" to clarify nurse role
        try:
            for i in range(self.notebook.index("end")):
                tab_text = self.notebook.tab(i, "text")
                if tab_text == "Prescriptions":
                    self.notebook.tab(i, text="View Prescriptions")
                    break
        except:
            pass
    
    def refresh_appointments(self):
        """Refresh appointments list - NURSES see ALL appointments in the system"""
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Apply filters
        date_filter = self.date_filter_var.get().strip() if hasattr(self, 'date_filter_var') else None
        status_filter = self.status_filter_var.get() if hasattr(self, 'status_filter_var') and self.status_filter_var.get() != "All" else None
        
        # Get ALL appointments in the system (not filtered by doctor_id like in doctor module)
        from utils.db_utils import AppointmentManager
        appointments = AppointmentManager.get_all_appointments(
            date_filter=date_filter or None, 
            status=status_filter
        )
        
        for appointment in appointments:
            # Include doctor name in the display for nurses
            self.appointments_tree.insert("", tk.END, values=(
                appointment['appointment_date'],
                appointment['appointment_time'],
                appointment['patient_name'],
                appointment.get('doctor_name', 'N/A'),  # Show which doctor
                appointment['status'],
                appointment['reason_for_visit'] or 'N/A',
                appointment['notes'] or 'N/A'
            ), tags=(appointment['appointment_id'],))
    
    def create_appointments_tab(self):
        """Create all appointments management tab - customized for nurses"""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="All Appointments")
        
        # Filter frame
        filter_frame = ttk.LabelFrame(appointments_frame, text="Filters", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Date filter
        ttk.Label(filter_frame, text="Date:").pack(side=tk.LEFT)
        self.date_filter_var = tk.StringVar()
        date_entry = ttk.Entry(filter_frame, textvariable=self.date_filter_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=(5, 20))
        ttk.Label(filter_frame, text="(YYYY-MM-DD or leave empty for all)").pack(side=tk.LEFT)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=(20, 5))
        self.status_filter_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_filter_var, 
                                   values=["All", "Scheduled", "Completed", "Cancelled", "Rescheduled"], 
                                   width=12, state="readonly")
        status_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Filter button
        ttk.Button(filter_frame, text="Apply Filter", 
                  command=self.refresh_appointments).pack(side=tk.LEFT)
        
        # Buttons frame - nurses can schedule appointments
        appointments_buttons = ttk.Frame(appointments_frame)
        appointments_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(appointments_buttons, text="📅 Schedule New Appointment", style="Modern.TButton",
                  command=self.show_nurse_schedule_appointment_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="Refresh", style="Secondary.TButton",
                  command=self.refresh_appointments).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="Edit Appointment", style="Modern.TButton",
                  command=self.edit_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="Reschedule", style="Modern.TButton",
                  command=self.reschedule_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="Cancel", style="Secondary.TButton",
                  command=self.cancel_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="Complete", style="Modern.TButton",
                  command=self.complete_appointment).pack(side=tk.LEFT, padx=(0, 10))
        
        # Appointments section
        appointments_section = ttk.LabelFrame(appointments_frame, text="All Appointments in System", padding="10")
        appointments_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Appointments treeview - modified columns for nurses
        columns = ("Date", "Time", "Patient", "Doctor", "Status", "Reason", "Notes")
        self.appointments_tree = ttk.Treeview(appointments_section, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            if col == "Doctor":
                self.appointments_tree.column(col, width=120)  # Doctor column
            else:
                self.appointments_tree.column(col, width=130)
        
        # Add scrollbar
        appointments_scrollbar = ttk.Scrollbar(appointments_section, orient=tk.VERTICAL, 
                                             command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=appointments_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        appointments_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load appointments
        self.refresh_appointments()
    
    def show_nurse_schedule_appointment_form(self):
        """Show appointment scheduling form for nurses - can schedule for any doctor"""
        from tkinter import ttk
        
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Schedule New Appointment")
        schedule_window.geometry("700x850")
        schedule_window.grab_set()
        
        # Center the window
        schedule_window.update_idletasks()
        width = schedule_window.winfo_width()
        height = schedule_window.winfo_height()
        x = (schedule_window.winfo_screenwidth() // 2) - (width // 2)
        y = (schedule_window.winfo_screenheight() // 2) - (height // 2)
        schedule_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create scrollable frame
        canvas = tk.Canvas(schedule_window)
        scrollbar = ttk.Scrollbar(schedule_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main container (now inside scrollable frame)
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            try:
                if schedule_window.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Window is destroyed, ignore the event
        
        def cleanup_bindings():
            try:
                canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                pass
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        schedule_window.protocol("WM_DELETE_WINDOW", lambda: [cleanup_bindings(), schedule_window.destroy()])
        
        # Title
        title_label = tk.Label(main_frame, text="Schedule New Appointment", 
                              font=("Arial", 16, "bold"), fg="#2E86AB")
        title_label.pack(pady=(0, 20))
        
        # Patient selection
        ttk.Label(main_frame, text="Select Patient:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(main_frame, textvariable=patient_var, width=60, state="readonly")
        patient_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Doctor selection - NURSES can schedule for any doctor
        ttk.Label(main_frame, text="Select Doctor:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(main_frame, textvariable=doctor_var, width=60, state="readonly")
        doctor_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Load patients and doctors
        self.load_all_patients(patient_combo)
        self.load_all_doctors(doctor_combo)
        
        # Date selection
        ttk.Label(main_frame, text="Appointment Date:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        from datetime import datetime
        
        # Year
        year_var = tk.StringVar(value=str(datetime.now().year))
        ttk.Label(date_frame, text="Year:").pack(side=tk.LEFT)
        year_combo = ttk.Combobox(date_frame, textvariable=year_var, width=8, state="readonly")
        current_year = datetime.now().year
        year_combo['values'] = [str(y) for y in range(current_year, current_year + 2)]
        year_combo.pack(side=tk.LEFT, padx=(5, 15))
        
        # Month
        month_var = tk.StringVar(value=str(datetime.now().month).zfill(2))
        ttk.Label(date_frame, text="Month:").pack(side=tk.LEFT)
        month_combo = ttk.Combobox(date_frame, textvariable=month_var, width=8, state="readonly")
        month_combo['values'] = [str(m).zfill(2) for m in range(1, 13)]
        month_combo.pack(side=tk.LEFT, padx=(5, 15))
        
        # Day
        day_var = tk.StringVar(value=str(datetime.now().day).zfill(2))
        ttk.Label(date_frame, text="Day:").pack(side=tk.LEFT)
        day_combo = ttk.Combobox(date_frame, textvariable=day_var, width=8, state="readonly")
        day_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Function to update day combobox based on selected year and month (disable past dates)
        def update_day_combobox():
            try:
                from datetime import datetime, timedelta
                from calendar import monthrange
                
                selected_year = int(year_var.get())
                selected_month = int(month_var.get())
                current_date = datetime.now()
                
                # Get the number of days in the selected month
                _, max_days = monthrange(selected_year, selected_month)
                
                # If selected year/month is current year/month, only show days from today onwards
                if selected_year == current_date.year and selected_month == current_date.month:
                    current_day = current_date.day
                    valid_days = [str(d).zfill(2) for d in range(current_day, max_days + 1)]
                # If it's a future year/month, show all days
                elif (selected_year > current_date.year) or (selected_year == current_date.year and selected_month > current_date.month):
                    valid_days = [str(d).zfill(2) for d in range(1, max_days + 1)]
                # If it's a past year/month, show no days (shouldn't happen, but just in case)
                else:
                    valid_days = []
                
                day_combo['values'] = valid_days
                
                # If current day value is not in valid days, reset to first valid day
                if day_var.get() not in valid_days and valid_days:
                    day_var.set(valid_days[0])
                elif not valid_days:
                    day_var.set("")
            except Exception as e:
                # Fallback to all days if there's an error
                day_combo['values'] = [str(d).zfill(2) for d in range(1, 32)]
        
        # Initialize day combobox
        update_day_combobox()
        
        # Bind year and month changes to update day combobox
        year_combo.bind('<<ComboboxSelected>>', lambda e: update_day_combobox())
        month_combo.bind('<<ComboboxSelected>>', lambda e: update_day_combobox())
        
        # Time selection
        ttk.Label(main_frame, text="Appointment Time:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        time_frame = ttk.Frame(main_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Hour
        hour_var = tk.StringVar(value="09")
        ttk.Label(time_frame, text="Hour:").pack(side=tk.LEFT)
        hour_combo = ttk.Combobox(time_frame, textvariable=hour_var, width=8, state="readonly")
        hour_combo['values'] = [str(h).zfill(2) for h in range(8, 18)]  # 8 AM to 5 PM
        hour_combo.pack(side=tk.LEFT, padx=(5, 15))
        
        # Minute
        minute_var = tk.StringVar(value="00")
        ttk.Label(time_frame, text="Minute:").pack(side=tk.LEFT)
        minute_combo = ttk.Combobox(time_frame, textvariable=minute_var, width=8, state="readonly")
        minute_combo['values'] = ["00", "15", "30", "45"]
        minute_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Visual Time Slot Availability (for selected doctor)
        ttk.Label(main_frame, text="Available Time Slots:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        availability_frame = ttk.LabelFrame(main_frame, text="Select doctor first, then click on available slots", padding="10")
        availability_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Time slots grid
        slots_frame = ttk.Frame(availability_frame)
        slots_frame.pack(fill=tk.X)
        
        # Generate time slots (8 AM to 6 PM, every 30 minutes)
        time_slots = []
        for hour in range(8, 18):
            for minute in [0, 30]:
                time_slots.append(f"{hour:02d}:{minute:02d}")
        
        slot_buttons = {}
        row = 0
        col = 0
        
        def update_time_selection(selected_time):
            hour, minute = selected_time.split(":")
            hour_var.set(hour)
            minute_var.set(minute)
            # Update button colors
            update_slot_availability()
        
        def update_slot_availability():
            try:
                if not doctor_var.get():
                    # No doctor selected, disable all slots
                    for button in slot_buttons.values():
                        button.config(bg="#D3D3D3", fg="gray", state="disabled", text=button.cget('text').split('\\n')[0])
                    return
                
                doctor_id = doctor_var.get().split("ID: ")[1]
                selected_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
                
                from utils.db_utils import AppointmentManager
                available_slots = AppointmentManager.get_available_time_slots(int(doctor_id), selected_date)
                
                for time_slot, button in slot_buttons.items():
                    if time_slot in available_slots:
                        button.config(bg="#90EE90", fg="black", state="normal", text=time_slot)  # Light green for available
                    else:
                        button.config(bg="#FFB6C1", fg="gray", state="disabled", text=f"{time_slot}\\n(Busy)")  # Light red for busy
                        
                # Highlight selected time
                selected_time = f"{hour_var.get()}:{minute_var.get()}"
                if selected_time in slot_buttons:
                    current_bg = slot_buttons[selected_time].cget('bg')
                    if current_bg == "#90EE90":  # If available
                        slot_buttons[selected_time].config(bg="#32CD32", fg="white", text=f"{selected_time}\\n✓")  # Darker green for selected
                    else:  # If busy but selected
                        slot_buttons[selected_time].config(bg="#FF69B4", fg="white", text=f"{selected_time}\\n⚠️")  # Pink for selected busy
                        
            except Exception as e:
                print(f"Error updating slot availability: {e}")
        
        # Create time slot buttons
        for i, time_slot in enumerate(time_slots):
            button = tk.Button(slots_frame, text=time_slot, width=10, height=2,
                             command=lambda t=time_slot: update_time_selection(t))
            button.grid(row=row, column=col, padx=2, pady=2)
            slot_buttons[time_slot] = button
            
            col += 1
            if col >= 5:  # 5 columns for nurse view
                col = 0
                row += 1
        
        # Bind changes to update availability
        doctor_combo.bind('<<ComboboxSelected>>', lambda e: update_slot_availability())
        year_combo.bind('<<ComboboxSelected>>', lambda e: update_slot_availability())
        month_combo.bind('<<ComboboxSelected>>', lambda e: update_slot_availability())
        day_combo.bind('<<ComboboxSelected>>', lambda e: update_slot_availability())
        
        # Legend
        legend_frame = ttk.Frame(availability_frame)
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(legend_frame, text="🟢 Available", bg="#90EE90", width=12).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(legend_frame, text="🔴 Busy", bg="#FFB6C1", width=12).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(legend_frame, text="🟡 Selected", bg="#32CD32", width=12).pack(side=tk.LEFT)
        
        # Initial availability update
        schedule_window.after(200, update_slot_availability)
        
        # Reason for visit
        ttk.Label(main_frame, text="Reason for Visit:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        reason_text = tk.Text(main_frame, height=4, width=60)
        reason_text.pack(fill=tk.X, pady=(0, 10))
        
        # Notes (optional)
        ttk.Label(main_frame, text="Additional Notes (Optional):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        notes_text = tk.Text(main_frame, height=3, width=60)
        notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save_appointment():
            try:
                # Validate inputs
                if not patient_var.get() or not doctor_var.get():
                    messagebox.showerror("Error", "Please select both patient and doctor")
                    return
                
                if not reason_text.get("1.0", tk.END).strip():
                    messagebox.showerror("Error", "Please enter a reason for visit")
                    return
                
                # Extract IDs from selection strings
                patient_id = patient_var.get().split("ID: ")[1]
                doctor_id = doctor_var.get().split("ID: ")[1]
                
                # Format date and time
                appointment_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
                appointment_time = f"{hour_var.get()}:{minute_var.get()}:00"
                
                # Validate that appointment is not in the past
                from datetime import datetime
                appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M:%S")
                if appointment_datetime <= datetime.now():
                    messagebox.showerror("Error", "Cannot schedule appointments in the past. Please select a future date and time.")
                    return
                
                # Check for appointment conflicts for the selected doctor
                from utils.db_utils import AppointmentManager
                has_conflict, conflicting_appointments, suggested_times = AppointmentManager.check_appointment_conflict(
                    int(doctor_id), appointment_date, appointment_time
                )
                
                if has_conflict:
                    # Get doctor name for conflict message
                    doctor_name = doctor_var.get().split(" (")[0]  # Extract name before email
                    
                    conflict_msg = "⚠️ APPOINTMENT CONFLICT DETECTED\\n\\n"
                    conflict_msg += f"Dr. {doctor_name} already has an appointment at {appointment_time} on {appointment_date}.\\n"
                    conflict_msg += "This would violate the 30-minute buffer rule.\\n\\n"
                    
                    if conflicting_appointments:
                        conflict_msg += "Conflicting appointment(s):\\n"
                        for apt in conflicting_appointments:
                            conflict_msg += f"• {apt['appointment_time']} - {apt['patient_name']}\\n"
                    
                    if suggested_times:
                        conflict_msg += f"\\n🕐 Suggested alternative times for Dr. {doctor_name}:\\n"
                        for i, time in enumerate(suggested_times, 1):
                            conflict_msg += f"{i}. {time}\\n"
                    
                    conflict_msg += "\\n❓ Do you want to schedule anyway? (Not recommended)"
                    
                    response = messagebox.askyesno("Appointment Conflict", conflict_msg)
                    if not response:
                        return
                
                # Prepare appointment data
                appointment_data = {
                    'patient_id': int(patient_id),
                    'doctor_id': int(doctor_id),
                    'appointment_date': appointment_date,
                    'appointment_time': appointment_time,
                    'reason_for_visit': reason_text.get("1.0", tk.END).strip(),
                    'notes': notes_text.get("1.0", tk.END).strip() or None
                }
                
                # Create the appointment
                if AppointmentManager.create_appointment(appointment_data):
                    if has_conflict:
                        messagebox.showinfo("Success", "⚠️ Appointment scheduled with conflict warning!")
                    else:
                        messagebox.showinfo("Success", "✅ Appointment scheduled successfully!")
                    schedule_window.destroy()
                    self.refresh_appointments()  # Refresh the appointments list
                else:
                    messagebox.showerror("Error", "Failed to schedule appointment")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error scheduling appointment: {str(e)}")
        
        ttk.Button(button_frame, text="💾 Schedule Appointment", style="Modern.TButton",
                  command=save_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancel", style="Secondary.TButton",
                  command=schedule_window.destroy).pack(side=tk.LEFT)
    
    def load_all_patients(self, combo_widget):
        """Load ALL patients in the system for nurses"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get ALL patients in the system
            query = """
            SELECT p.patient_id, u.full_name, u.email
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, fetch=True)
            
            values = []
            for patient in result or []:
                values.append(f"{patient['full_name']} ({patient['email']}) - ID: {patient['patient_id']}")
            
            combo_widget['values'] = values
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading patients: {e}")
    
    def load_all_doctors(self, combo_widget):
        """Load ALL doctors for nurses to schedule appointments"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get ALL doctors in the system
            query = """
            SELECT d.doctor_id, u.full_name, u.email
            FROM doctors d
            JOIN users u ON d.user_id = u.user_id
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, fetch=True)
            
            values = []
            for doctor in result or []:
                values.append(f"Dr. {doctor['full_name']} ({doctor['email']}) - ID: {doctor['doctor_id']}")
            
            combo_widget['values'] = values
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading doctors: {e}")
    
    def refresh_prescriptions(self):
        """Refresh prescriptions list - NURSES see ALL prescriptions in the system"""
        # Clear existing items
        for item in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(item)
        
        # Apply status filter
        status_filter = self.prescription_status_var.get() if hasattr(self, 'prescription_status_var') and self.prescription_status_var.get() != "All" else None
        
        # Get ALL prescriptions in the system (not filtered by doctor_id like in doctor module)
        from utils.db_utils import PrescriptionManager
        prescriptions = PrescriptionManager.get_all_prescriptions(status=status_filter)
        
        for prescription in prescriptions:
            medications_preview = prescription['medications'][:50] + "..." if len(prescription['medications']) > 50 else prescription['medications']
            
            self.prescriptions_tree.insert("", tk.END, values=(
                prescription['prescription_date'],
                prescription['patient_name'],
                prescription.get('doctor_name', 'N/A'),  # Show which doctor prescribed
                prescription['diagnosis'] or 'N/A',
                medications_preview,
                prescription['status']
            ), tags=(prescription['prescription_id'],))
    
    def create_prescriptions_tab(self):
        """Create prescriptions management tab - customized for nurses to view all prescriptions"""
        prescriptions_frame = ttk.Frame(self.notebook)
        self.notebook.add(prescriptions_frame, text="View Prescriptions")
        
        # Filter frame
        filter_frame = ttk.LabelFrame(prescriptions_frame, text="Filters", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT)
        self.prescription_status_var = tk.StringVar(value="Active")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.prescription_status_var, 
                                   values=["All", "Active", "Completed", "Cancelled"], 
                                   width=12, state="readonly")
        status_combo.pack(side=tk.LEFT, padx=(5, 20))
        
        # Filter button
        ttk.Button(filter_frame, text="Apply Filter", 
                  command=self.refresh_prescriptions).pack(side=tk.LEFT)
        
        # Buttons frame - nurses can only view and refresh prescriptions
        prescriptions_buttons = ttk.Frame(prescriptions_frame)
        prescriptions_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(prescriptions_buttons, text="Refresh", style="Secondary.TButton",
                  command=self.refresh_prescriptions).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="View Details", style="Modern.TButton",
                  command=self.view_prescription_details).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="Print Report", style="Secondary.TButton",
                  command=self.print_prescription_report).pack(side=tk.LEFT, padx=(0, 10))
        
        # Prescriptions section
        prescriptions_section = ttk.LabelFrame(prescriptions_frame, text="All Prescriptions in System", padding="10")
        prescriptions_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Prescriptions treeview - modified columns for nurses
        columns = ("Date", "Patient", "Doctor", "Diagnosis", "Medications", "Status")
        self.prescriptions_tree = ttk.Treeview(prescriptions_section, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.prescriptions_tree.heading(col, text=col)
            if col == "Doctor":
                self.prescriptions_tree.column(col, width=120)  # Doctor column
            elif col == "Patient":
                self.prescriptions_tree.column(col, width=150)  # Patient column
            elif col == "Medications":
                self.prescriptions_tree.column(col, width=200)  # Medications column
            else:
                self.prescriptions_tree.column(col, width=120)
        
        # Add scrollbar
        prescriptions_scrollbar = ttk.Scrollbar(prescriptions_section, orient=tk.VERTICAL, 
                                              command=self.prescriptions_tree.yview)
        self.prescriptions_tree.configure(yscrollcommand=prescriptions_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.prescriptions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prescriptions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load prescriptions
        self.refresh_prescriptions()
    
    def view_prescription_details(self):
        """View detailed prescription information"""
        selected_item = self.prescriptions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a prescription to view details")
            return
        
        prescription_id = self.prescriptions_tree.item(selected_item[0])['tags'][0]
        
        # Get full prescription details
        from utils.db_utils import PrescriptionManager
        prescriptions = PrescriptionManager.get_all_prescriptions()
        prescription = next((p for p in prescriptions if p['prescription_id'] == prescription_id), None)
        
        if not prescription:
            messagebox.showerror("Error", "Prescription not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Prescription Details")
        details_window.geometry("600x700")
        details_window.grab_set()
        
        # Center the window
        details_window.update_idletasks()
        width = details_window.winfo_width()
        height = details_window.winfo_height()
        x = (details_window.winfo_screenwidth() // 2) - (width // 2)
        y = (details_window.winfo_screenheight() // 2) - (height // 2)
        details_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create scrollable content
        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text=f"Prescription Details", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Prescription information
        info_items = [
            ("Date", prescription['prescription_date']),
            ("Patient", prescription['patient_name']),
            ("Doctor", prescription.get('doctor_name', 'N/A')),
            ("Status", prescription['status'])
        ]
        
        for label, value in info_items:
            if value:
                frame = ttk.Frame(main_frame)
                frame.pack(fill=tk.X, pady=2)
                ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                ttk.Label(frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Diagnosis
        if prescription['diagnosis']:
            ttk.Label(main_frame, text="Diagnosis:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            diagnosis_text = tk.Text(main_frame, height=3, width=60)
            diagnosis_text.pack(fill=tk.X, pady=(0, 10))
            diagnosis_text.insert("1.0", prescription['diagnosis'])
            diagnosis_text.config(state=tk.DISABLED)
        
        # Medications
        ttk.Label(main_frame, text="Medications:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        medications_text = tk.Text(main_frame, height=6, width=60)
        medications_text.pack(fill=tk.X, pady=(0, 10))
        medications_text.insert("1.0", prescription['medications'])
        medications_text.config(state=tk.DISABLED)
        
        # Dosage instructions
        if prescription['dosage_instructions']:
            ttk.Label(main_frame, text="Dosage Instructions:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            dosage_text = tk.Text(main_frame, height=4, width=60)
            dosage_text.pack(fill=tk.X, pady=(0, 10))
            dosage_text.insert("1.0", prescription['dosage_instructions'])
            dosage_text.config(state=tk.DISABLED)
        
        # Notes
        if prescription['notes']:
            ttk.Label(main_frame, text="Notes:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            notes_text = tk.Text(main_frame, height=4, width=60)
            notes_text.pack(fill=tk.X, pady=(0, 10))
            notes_text.insert("1.0", prescription['notes'])
            notes_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(main_frame, text="Close", 
                  command=details_window.destroy).pack(pady=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh_today(self):
        """Refresh today's appointments - NURSES see ALL appointments for today"""
        # Clear existing items
        for item in self.today_tree.get_children():
            self.today_tree.delete(item)
        
        # Get today's date
        from datetime import date
        today = date.today()
        
        # Get ALL appointments for today (not filtered by doctor_id like in doctor module)
        from utils.db_utils import AppointmentManager
        appointments = AppointmentManager.get_all_appointments(date_filter=today)
        
        for appointment in appointments:
            self.today_tree.insert("", tk.END, values=(
                appointment['appointment_time'],
                appointment['patient_name'],
                appointment.get('doctor_name', 'N/A'),  # Show which doctor
                appointment['status'],
                appointment['reason_for_visit'] or 'N/A',
                appointment['notes'] or 'N/A'
            ), tags=(appointment['appointment_id'],))
    
    def create_today_tab(self):
        """Create today's appointments tab - customized for nurses to see all today's appointments"""
        today_frame = ttk.Frame(self.notebook)
        self.notebook.add(today_frame, text="Today's Schedule")
        
        # Buttons frame - moved to top for better visibility
        today_buttons = ttk.Frame(today_frame)
        today_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(today_buttons, text="Refresh", style="Secondary.TButton",
                  command=self.refresh_today).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="View Details", style="Modern.TButton",
                  command=self.view_appointment_details).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="Update Status", style="Modern.TButton",
                  command=self.update_appointment_status).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="Add Notes", style="Secondary.TButton",
                  command=self.add_appointment_notes).pack(side=tk.LEFT, padx=(0, 10))
        
        # Today's appointments section
        from datetime import date
        today_section = ttk.LabelFrame(today_frame, text=f"All Appointments Today - {date.today().strftime('%B %d, %Y')}", padding="10")
        today_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Today's appointments treeview - modified columns for nurses
        columns = ("Time", "Patient", "Doctor", "Status", "Reason", "Notes")
        self.today_tree = ttk.Treeview(today_section, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.today_tree.heading(col, text=col)
            if col == "Doctor":
                self.today_tree.column(col, width=120)  # Doctor column
            elif col == "Patient":
                self.today_tree.column(col, width=150)  # Patient column
            else:
                self.today_tree.column(col, width=130)
        
        # Add scrollbar
        today_scrollbar = ttk.Scrollbar(today_section, orient=tk.VERTICAL, 
                                       command=self.today_tree.yview)
        self.today_tree.configure(yscrollcommand=today_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.today_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        today_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load today's appointments
        self.refresh_today()
    
    def view_appointment_details(self):
        """View detailed appointment information"""
        selected_item = self.today_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to view details")
            return
        
        appointment_id = self.today_tree.item(selected_item[0])['tags'][0]
        
        # Get appointment details
        from utils.db_utils import AppointmentManager
        appointments = AppointmentManager.get_all_appointments()
        appointment = next((a for a in appointments if a['appointment_id'] == appointment_id), None)
        
        if not appointment:
            messagebox.showerror("Error", "Appointment not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Appointment Details")
        details_window.geometry("500x600")
        details_window.grab_set()
        
        # Center the window
        details_window.update_idletasks()
        width = details_window.winfo_width()
        height = details_window.winfo_height()
        x = (details_window.winfo_screenwidth() // 2) - (width // 2)
        y = (details_window.winfo_screenheight() // 2) - (height // 2)
        details_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(details_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Appointment Details", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Appointment information
        info_items = [
            ("Date", appointment['appointment_date']),
            ("Time", appointment['appointment_time']),
            ("Patient", appointment['patient_name']),
            ("Doctor", appointment.get('doctor_name', 'N/A')),
            ("Status", appointment['status'])
        ]
        
        for label, value in info_items:
            if value:
                frame = ttk.Frame(main_frame)
                frame.pack(fill=tk.X, pady=2)
                ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                ttk.Label(frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Reason for visit
        if appointment['reason_for_visit']:
            ttk.Label(main_frame, text="Reason for Visit:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            reason_text = tk.Text(main_frame, height=3, width=50)
            reason_text.pack(fill=tk.X, pady=(0, 10))
            reason_text.insert("1.0", appointment['reason_for_visit'])
            reason_text.config(state=tk.DISABLED)
        
        # Notes
        if appointment['notes']:
            ttk.Label(main_frame, text="Notes:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            notes_text = tk.Text(main_frame, height=4, width=50)
            notes_text.pack(fill=tk.X, pady=(0, 10))
            notes_text.insert("1.0", appointment['notes'])
            notes_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(main_frame, text="Close", 
                  command=details_window.destroy).pack(pady=20)
    
    def update_appointment_status(self):
        """Update appointment status"""
        selected_item = self.today_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to update status")
            return
        
        appointment_id = self.today_tree.item(selected_item[0])['tags'][0]
        
        # Create status update window
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Appointment Status")
        status_window.geometry("400x200")
        status_window.grab_set()
        
        # Center the window
        status_window.update_idletasks()
        width = status_window.winfo_width()
        height = status_window.winfo_height()
        x = (status_window.winfo_screenwidth() // 2) - (width // 2)
        y = (status_window.winfo_screenheight() // 2) - (height // 2)
        status_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(status_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select New Status:", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        status_var = tk.StringVar(value="Scheduled")
        status_combo = ttk.Combobox(main_frame, textvariable=status_var, 
                                   values=["Scheduled", "In Progress", "Completed", "Cancelled", "Rescheduled"], 
                                   width=20, state="readonly")
        status_combo.pack(pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_status():
            new_status = status_var.get()
            from utils.db_utils import AppointmentManager
            if AppointmentManager.update_appointment_status(appointment_id, new_status):
                messagebox.showinfo("Success", f"Appointment status updated to: {new_status}")
                status_window.destroy()
                self.refresh_today()
            else:
                messagebox.showerror("Error", "Failed to update appointment status")
        
        ttk.Button(button_frame, text="Update", style="Modern.TButton", command=save_status).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", style="Secondary.TButton", command=status_window.destroy).pack(side=tk.LEFT)
    
    def create_vitals_tab(self):
        """Create vitals recording tab - customized for nurses to see ALL patients"""
        vitals_frame = ttk.Frame(self.notebook)
        self.notebook.add(vitals_frame, text="Patient Vitals")
        
        # Patient selection frame
        selection_frame = ttk.LabelFrame(vitals_frame, text="Select Patient", padding="10")
        selection_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        ttk.Label(selection_frame, text="Patient:").pack(side=tk.LEFT)
        self.selected_patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(selection_frame, textvariable=self.selected_patient_var, 
                                         width=30, state="readonly")
        self.patient_combo.pack(side=tk.LEFT, padx=(5, 10))
        self.patient_combo.bind("<<ComboboxSelected>>", self.on_patient_selected_for_vitals)
        
        ttk.Button(selection_frame, text="🔄 Refresh Patient List", 
                  command=self.load_all_patients_for_vitals).pack(side=tk.LEFT, padx=(5, 0))
        
        # Show patient count
        self.patient_count_label = ttk.Label(selection_frame, text="", font=("Arial", 9), foreground="gray")
        self.patient_count_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Vitals recording frame
        vitals_recording_frame = ttk.LabelFrame(vitals_frame, text="Record Vitals", padding="15")
        vitals_recording_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create form for vitals
        self.vitals_vars = {}
        vitals_fields = [
            ("Blood Pressure Systolic", "blood_pressure_systolic"),
            ("Blood Pressure Diastolic", "blood_pressure_diastolic"),
            ("Heart Rate (bpm)", "heart_rate"),
            ("Temperature (°F)", "temperature"),
            ("Weight (kg)", "weight"),
            ("Height (cm)", "height"),
            ("Oxygen Saturation (%)", "oxygen_saturation")
        ]
        
        # Create grid layout for vitals
        row = 0
        for label, var_name in vitals_fields:
            ttk.Label(vitals_recording_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
            self.vitals_vars[var_name] = tk.StringVar()
            ttk.Entry(vitals_recording_frame, textvariable=self.vitals_vars[var_name], 
                     width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
        
        # Notes
        ttk.Label(vitals_recording_frame, text="Notes:").grid(row=row, column=0, sticky=tk.NW, padx=(0, 10), pady=5)
        self.vitals_notes_text = tk.Text(vitals_recording_frame, height=4, width=40)
        self.vitals_notes_text.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Record/Update button
        self.record_vitals_btn = ttk.Button(vitals_recording_frame, text="📝 Record New Vitals", 
                                           command=self.record_vitals)
        self.record_vitals_btn.grid(row=row+1, column=1, pady=20)
        
        # Clear form button
        ttk.Button(vitals_recording_frame, text="🗑️ Clear Form", 
                  command=self.clear_vitals_form).grid(row=row+1, column=2, pady=20, padx=(10, 0))
        
        # Vitals history section
        history_section = ttk.LabelFrame(vitals_frame, text="Vitals History for Selected Patient", padding="10")
        history_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Vitals history treeview
        columns = ("Date/Time", "BP", "HR", "Temp", "Weight", "Height", "O2 Sat", "Recorded By")
        self.vitals_tree = ttk.Treeview(history_section, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            self.vitals_tree.heading(col, text=col)
            self.vitals_tree.column(col, width=100)
        
        # Add scrollbar
        vitals_scrollbar = ttk.Scrollbar(history_section, orient=tk.VERTICAL, 
                                       command=self.vitals_tree.yview)
        self.vitals_tree.configure(yscrollcommand=vitals_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.vitals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vitals_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load ALL patients list for nurses
        self.load_all_patients_for_vitals()
    
    def load_all_patients_for_vitals(self):
        """Load ALL patients in the system for vitals recording"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                self.patient_count_label.config(text="❌ Database connection failed")
                return
            
            # Get ALL patients in the system (not just doctor's patients)
            query = """
            SELECT p.patient_id, u.full_name, u.email
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, fetch=True)
            
            values = []
            for patient in result or []:
                values.append(f"{patient['full_name']} ({patient['email']}) - ID: {patient['patient_id']}")
            
            self.patient_combo['values'] = values
            
            # Update patient count
            patient_count = len(values)
            self.patient_count_label.config(text=f"✅ {patient_count} patients loaded")
            
            db_manager.disconnect()
            
        except Exception as e:
            self.patient_count_label.config(text=f"❌ Error: {str(e)[:30]}...")
            print(f"Error loading patients: {e}")
    
    def on_patient_selected_for_vitals(self, event=None):
        """Load vitals history and latest vitals for selected patient"""
        if not self.selected_patient_var.get():
            return
        
        # Extract patient ID from selection
        patient_selection = self.selected_patient_var.get()
        if 'ID:' in patient_selection:
            patient_id = patient_selection.split('ID: ')[1]
            self.load_vitals_history(patient_id)
            self.load_latest_vitals_for_editing(patient_id)
    
    def load_vitals_history(self, patient_id):
        """Load vitals history for the selected patient"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Clear existing items
            for item in self.vitals_tree.get_children():
                self.vitals_tree.delete(item)
            
            query = """
            SELECT v.recorded_at, v.blood_pressure_systolic, v.blood_pressure_diastolic,
                   v.heart_rate, v.temperature, v.weight, v.height, v.oxygen_saturation,
                   u.full_name as recorded_by
            FROM vitals v
            JOIN users u ON v.recorded_by = u.user_id
            WHERE v.patient_id = %s
            ORDER BY v.recorded_at DESC
            """
            
            result = db_manager.execute_query(query, (patient_id,), fetch=True)
            
            for vital in result or []:
                # Format blood pressure
                bp = f"{vital['blood_pressure_systolic'] or '-'}/{vital['blood_pressure_diastolic'] or '-'}"
                
                self.vitals_tree.insert('', 'end', values=(
                    vital['recorded_at'].strftime('%Y-%m-%d %H:%M') if vital['recorded_at'] else 'N/A',
                    bp,
                    vital['heart_rate'] or '-',
                    f"{vital['temperature']}°F" if vital['temperature'] else '-',
                    f"{vital['weight']}kg" if vital['weight'] else '-',
                    f"{vital['height']}cm" if vital['height'] else '-',
                    f"{vital['oxygen_saturation']}%" if vital['oxygen_saturation'] else '-',
                    vital['recorded_by']
                ))
            
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading vitals history: {e}")
    
    def load_latest_vitals_for_editing(self, patient_id):
        """Load the most recent vitals into the form for editing"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            query = """
            SELECT blood_pressure_systolic, blood_pressure_diastolic, heart_rate,
                   temperature, weight, height, oxygen_saturation, notes
            FROM vitals
            WHERE patient_id = %s
            ORDER BY recorded_at DESC
            LIMIT 1
            """
            
            result = db_manager.execute_query(query, (patient_id,), fetch=True)
            
            if result:
                vitals = result[0]
                # Populate form with latest vitals for editing
                self.vitals_vars['blood_pressure_systolic'].set(vitals['blood_pressure_systolic'] or '')
                self.vitals_vars['blood_pressure_diastolic'].set(vitals['blood_pressure_diastolic'] or '')
                self.vitals_vars['heart_rate'].set(vitals['heart_rate'] or '')
                self.vitals_vars['temperature'].set(vitals['temperature'] or '')
                self.vitals_vars['weight'].set(vitals['weight'] or '')
                self.vitals_vars['height'].set(vitals['height'] or '')
                self.vitals_vars['oxygen_saturation'].set(vitals['oxygen_saturation'] or '')
                
                # Clear and set notes
                self.vitals_notes_text.delete('1.0', tk.END)
                if vitals['notes']:
                    self.vitals_notes_text.insert('1.0', vitals['notes'])
                
                # Update button text to indicate editing
                self.record_vitals_btn.config(text="✏️ Update Vitals")
            else:
                # No existing vitals, clear form
                self.clear_vitals_form()
            
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading latest vitals: {e}")
    
    def clear_vitals_form(self):
        """Clear all vitals form fields"""
        for var in self.vitals_vars.values():
            var.set('')
        self.vitals_notes_text.delete('1.0', tk.END)
        self.record_vitals_btn.config(text="📝 Record New Vitals")
    
    def record_vitals(self):
        """Record patient vitals - overridden for nurse module"""
        patient_text = self.selected_patient_var.get()
        if not patient_text:
            messagebox.showerror("Error", "Please select a patient first")
            return
        
        try:
            # Extract patient ID from combo text
            if 'ID:' in patient_text:
                patient_id = int(patient_text.split('ID: ')[1])
            else:
                messagebox.showerror("Error", "Invalid patient selection")
                return
            
            # Prepare vitals data with ALL required fields
            vitals_data = {
                'patient_id': patient_id,
                'recorded_by': self.user_data['user_id'],
                'blood_pressure_systolic': None,
                'blood_pressure_diastolic': None,
                'heart_rate': None,
                'temperature': None,
                'weight': None,
                'height': None,
                'oxygen_saturation': None,
                'notes': None
            }
            
            # Add vital measurements with proper type conversion and validation
            conversion_errors = []
            
            # Integer fields
            int_fields = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'oxygen_saturation']
            for field in int_fields:
                value = self.vitals_vars[field].get().strip()
                if value:
                    try:
                        vitals_data[field] = int(float(value))  # Convert to float first, then int for better parsing
                    except ValueError:
                        conversion_errors.append(f"{field.replace('_', ' ').title()}: '{value}' is not a valid number")
            
            # Float fields
            float_fields = ['temperature', 'weight', 'height']
            for field in float_fields:
                value = self.vitals_vars[field].get().strip()
                if value:
                    try:
                        vitals_data[field] = float(value)
                    except ValueError:
                        conversion_errors.append(f"{field.replace('_', ' ').title()}: '{value}' is not a valid number")
            
            # Check for conversion errors
            if conversion_errors:
                error_msg = "Please correct the following errors:\n" + "\n".join(conversion_errors)
                messagebox.showerror("Input Error", error_msg)
                return
            
            # Add notes
            notes = self.vitals_notes_text.get("1.0", tk.END).strip()
            if notes:
                vitals_data['notes'] = notes
            
            # Check if any vital was recorded (check for non-None values)
            vital_fields = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 
                          'temperature', 'weight', 'height', 'oxygen_saturation']
            
            if not any(vitals_data[field] is not None for field in vital_fields):
                messagebox.showerror("Error", "Please enter at least one vital measurement")
                return
            
            # Import VitalsManager
            from utils.db_utils import VitalsManager
            
            # Record vitals
            if VitalsManager.record_vitals(vitals_data):
                messagebox.showinfo("Success", "Vitals recorded successfully!")
                
                # Reload vitals history and latest vitals for the same patient
                self.load_vitals_history(patient_id)
                self.load_latest_vitals_for_editing(patient_id)
                
            else:
                messagebox.showerror("Error", "Failed to record vitals. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while recording vitals: {str(e)}")
            print(f"Error in record_vitals: {e}")
            import traceback
            traceback.print_exc()
    
    def customize_header_for_nurse(self):
        """Update the header to show nurse-specific information"""
        # Find and update the header labels
        self.update_header_text("Doctor Dashboard", "Nurse Dashboard")
        self.update_header_text("Dr.", "Nurse")
        self.update_header_icon("👨‍⚕️", "👩‍⚕️")
    
    def update_header_text(self, old_text, new_text):
        """Update text in header labels"""
        def update_widget(widget):
            try:
                if hasattr(widget, 'cget') and hasattr(widget, 'config'):
                    if widget.winfo_class() == 'Label':
                        current_text = widget.cget('text')
                        if old_text in current_text:
                            widget.config(text=current_text.replace(old_text, new_text))
                
                # Recursively check children
                for child in widget.winfo_children():
                    update_widget(child)
            except:
                pass  # Skip any widgets that cause errors
        
        update_widget(self.root)
    
    def update_header_icon(self, old_icon, new_icon):
        """Update icon in header"""
        def update_widget(widget):
            try:
                if hasattr(widget, 'cget') and hasattr(widget, 'config'):
                    if widget.winfo_class() == 'Label':
                        current_text = widget.cget('text')
                        if current_text == old_icon:
                            widget.config(text=new_icon)
                
                # Recursively check children
                for child in widget.winfo_children():
                    update_widget(child)
            except:
                pass  # Skip any widgets that cause errors
        
        update_widget(self.root)

if __name__ == "__main__":
    # Test the nurse dashboard (requires authentication first)
    pass
