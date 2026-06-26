"""
Doctor Module - Doctor Dashboard and Functionality
Healthcare Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from datetime import datetime, date, timedelta
from utils.db_utils import AppointmentManager, PrescriptionManager, VitalsManager, UserManager

class DoctorDashboard:
    """Doctor dashboard interface with modern design"""
    
    def __init__(self, user_data, parent_window):
        self.user_data = user_data
        self.parent_window = parent_window
        
        # Modern color scheme (matching admin module)
        self.colors = {
            'primary': '#2E86AB',      # Medical blue
            'secondary': '#A23B72',    # Accent purple
            'success': '#10B981',      # Green
            'warning': '#F59E0B',      # Yellow
            'danger': '#EF4444',       # Red
            'background': '#F8FAFC',   # Light background
            'card': '#FFFFFF',         # White cards
            'border': '#E5E7EB',       # Light border
            'text_primary': '#111827', # Dark text
            'text_secondary': '#6B7280' # Gray text
        }
        
        # Create main window
        self.root = tk.Toplevel()
        self.root.title(f"Doctor Dashboard - Dr. {user_data['full_name']}")
        self.root.geometry("1400x900")
        
        # Window state management
        self.is_maximized = False
        self.normal_geometry = "1400x900"
        
        # Configure window properties
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.minsize(800, 600)  # Minimum window size
        
        # Configure window styling
        self.root.configure(bg=self.colors['background'])
        
        # Setup modern styles
        self.setup_styles()
        
        # Center window initially
        self.center_window()
        
        # Start maximized for better experience
        self.maximize_window()
        
        # Get doctor-specific data
        self.doctor_id = user_data.get('role_id')
        
        self.create_dashboard()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('Modern.TNotebook', 
                       background=self.colors['background'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       padding=[20, 12],
                       font=('Segoe UI', 11, 'bold'),
                       focuscolor='none')
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['border'])],
                 foreground=[('selected', 'white'),
                           ('active', self.colors['text_primary'])])
        
        # Configure treeview style
        style.configure('Modern.Treeview',
                       background=self.colors['card'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['card'],
                       font=('Segoe UI', 9))
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['border'],
                       foreground=self.colors['text_primary'])
        
        # Configure button styles
        style.configure('Modern.TButton',
                       padding=(10, 5),
                       font=('Segoe UI', 9, 'bold'),
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        style.map('Modern.TButton',
                 background=[('active', self.colors['secondary']),
                           ('pressed', self.colors['text_primary'])],
                 foreground=[('active', 'white'),
                           ('pressed', 'white')])
        
        # Configure alternate button styles
        style.configure('Secondary.TButton',
                       padding=(10, 5),
                       font=('Segoe UI', 9),
                       background=self.colors['border'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       focuscolor='none')
        style.map('Secondary.TButton',
                 background=[('active', self.colors['text_secondary']),
                           ('pressed', self.colors['primary'])],
                 foreground=[('active', 'white'),
                           ('pressed', 'white')])

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def maximize_window(self):
        """Maximize the window"""
        if not self.is_maximized:
            # Store current geometry
            self.normal_geometry = self.root.geometry()
            # Maximize window
            self.root.state('zoomed')
            self.is_maximized = True
    
    def minimize_window(self):
        """Minimize the window"""
        self.root.iconify()
    
    def restore_window(self):
        """Restore window from maximized state"""
        if self.is_maximized:
            self.root.state('normal')
            self.root.geometry(self.normal_geometry)
            self.is_maximized = False
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            self.restore_window()
            self.maximize_btn.configure(text="🗖")  # Maximize icon
        else:
            self.maximize_window()
            self.maximize_btn.configure(text="🗗")  # Restore icon
    
    def create_dashboard(self):
        """Create the main dashboard interface with modern design"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with professional medical design
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Left side - Welcome message with icon
        left_header = tk.Frame(header_content, bg=self.colors['primary'])
        left_header.pack(side=tk.LEFT, fill=tk.Y)
        
        # Doctor icon
        icon_label = tk.Label(left_header, text="👨‍⚕️", font=("Arial", 20), 
                             bg=self.colors['primary'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Welcome text
        welcome_frame = tk.Frame(left_header, bg=self.colors['primary'])
        welcome_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Doctor Dashboard", 
                                font=("Segoe UI", 18, "bold"),
                                bg=self.colors['primary'], fg='white')
        welcome_label.pack(anchor=tk.W)
        
        user_label = tk.Label(welcome_frame, 
                             text=f"Dr. {self.user_data['full_name']}", 
                             font=("Segoe UI", 11),
                             bg=self.colors['primary'], fg='#E0F2FE')
        user_label.pack(anchor=tk.W)
        
        # Right side - User actions and window controls
        right_header = tk.Frame(header_content, bg=self.colors['primary'])
        right_header.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Window controls section
        window_controls = tk.Frame(right_header, bg=self.colors['primary'])
        window_controls.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Minimize button
        minimize_btn = tk.Button(window_controls, text="🗕", 
                                command=self.minimize_window,
                                font=("Segoe UI", 12),
                                bg='white', fg=self.colors['primary'],
                                relief='flat', width=3, height=1,
                                cursor='hand2')
        minimize_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(window_controls, text="🗗", 
                                     command=self.toggle_maximize,
                                     font=("Segoe UI", 12),
                                     bg='white', fg=self.colors['primary'],
                                     relief='flat', width=3, height=1,
                                     cursor='hand2')
        self.maximize_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Close button
        close_btn = tk.Button(window_controls, text="🗙", 
                             command=self.on_closing,
                             font=("Segoe UI", 12),
                             bg='#EF4444', fg='white',
                             relief='flat', width=3, height=1,
                             cursor='hand2')
        close_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # User info section
        user_info = tk.Frame(right_header, bg=self.colors['primary'])
        user_info.pack(side=tk.RIGHT)
        
        # Current time
        time_label = tk.Label(user_info, 
                             text=datetime.now().strftime("%Y-%m-%d %H:%M"), 
                             font=("Segoe UI", 10),
                             bg=self.colors['primary'], fg='#E0F2FE')
        time_label.pack(pady=(0, 5))
        
        # Logout button with modern style
        logout_btn = tk.Button(user_info, text="🚪 Logout", 
                              command=self.logout,
                              font=("Segoe UI", 10, "bold"),
                              bg='white', fg=self.colors['primary'],
                              relief='flat', padx=15, pady=6,
                              cursor='hand2')
        logout_btn.pack()
        
        # Content area
        content_area = tk.Frame(main_container, bg=self.colors['background'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create modern notebook for tabs
        self.notebook = ttk.Notebook(content_area, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_today_tab()
        self.create_appointments_tab()
        self.create_patients_tab()
        self.create_prescriptions_tab()
        self.create_vitals_tab()
        
        # Set focus to first tab
        self.notebook.select(0)
    
    def create_today_tab(self):
        """Create today's appointments tab"""
        today_frame = ttk.Frame(self.notebook)
        self.notebook.add(today_frame, text="Today's Schedule")
        
        # Buttons frame - moved to top for better visibility
        today_buttons = ttk.Frame(today_frame)
        today_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(today_buttons, text="Refresh", style="Secondary.TButton",
                  command=self.refresh_today).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="Edit Appointment", style="Modern.TButton",
                  command=self.edit_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="Complete Appointment", style="Modern.TButton",
                  command=self.complete_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(today_buttons, text="Add Notes", style="Secondary.TButton",
                  command=self.add_appointment_notes).pack(side=tk.LEFT, padx=(0, 10))
        
        # Today's appointments section
        today_section = ttk.LabelFrame(today_frame, text=f"Appointments - {date.today().strftime('%B %d, %Y')}", padding="10")
        today_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Today's appointments treeview
        columns = ("Time", "Patient", "Status", "Reason", "Notes")
        self.today_tree = ttk.Treeview(today_section, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.today_tree.heading(col, text=col)
            self.today_tree.column(col, width=200)
        
        # Add scrollbar
        today_scrollbar = ttk.Scrollbar(today_section, orient=tk.VERTICAL, 
                                       command=self.today_tree.yview)
        self.today_tree.configure(yscrollcommand=today_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.today_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        today_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load today's appointments
        self.refresh_today()
    
    def create_appointments_tab(self):
        """Create all appointments management tab"""
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
        
        # Buttons frame - moved under filters for better visibility
        appointments_buttons = ttk.Frame(appointments_frame)
        appointments_buttons.pack(fill=tk.X, padx=10, pady=10)
        
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
        appointments_section = ttk.LabelFrame(appointments_frame, text="Appointments", padding="10")
        appointments_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Appointments treeview
        columns = ("Date", "Time", "Patient", "Status", "Reason", "Notes")
        self.appointments_tree = ttk.Treeview(appointments_section, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150)
        
        # Add scrollbar
        appointments_scrollbar = ttk.Scrollbar(appointments_section, orient=tk.VERTICAL, 
                                             command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=appointments_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        appointments_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load appointments
        self.refresh_appointments()
    
    def create_patients_tab(self):
        """Create patients management tab"""
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="My Patients")
        
        # Patients section
        patients_section = ttk.LabelFrame(patients_frame, text="Patients Assigned to Me", padding="10")
        patients_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Patients treeview
        columns = ("Name", "Phone", "Blood Group", "Last Visit", "Total Visits")
        self.patients_tree = ttk.Treeview(patients_section, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=150)
        
        # Add scrollbar
        patients_scrollbar = ttk.Scrollbar(patients_section, orient=tk.VERTICAL, 
                                         command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=patients_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.patients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        patients_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        patients_buttons = ttk.Frame(patients_frame)
        patients_buttons.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(patients_buttons, text="Refresh", 
                  command=self.refresh_patients).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(patients_buttons, text="View Patient Details", 
                  command=self.view_patient_details).pack(side=tk.LEFT, padx=(0, 10))
        
        # Load patients
        self.refresh_patients()
    
    def create_prescriptions_tab(self):
        """Create prescriptions management tab"""
        prescriptions_frame = ttk.Frame(self.notebook)
        self.notebook.add(prescriptions_frame, text="Prescriptions")
        
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
        
        # Buttons frame - moved under filters for better visibility
        prescriptions_buttons = ttk.Frame(prescriptions_frame)
        prescriptions_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(prescriptions_buttons, text="Refresh", style="Secondary.TButton",
                  command=self.refresh_prescriptions).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="New Prescription", style="Modern.TButton",
                  command=self.new_prescription).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="Edit Selected", style="Modern.TButton",
                  command=self.edit_prescription).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="Delete Selected", style="Secondary.TButton",
                  command=self.delete_prescription).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="Print Report", style="Secondary.TButton",
                  command=self.print_prescription_report).pack(side=tk.LEFT, padx=(0, 10))
        
        # Prescriptions section
        prescriptions_section = ttk.LabelFrame(prescriptions_frame, text="Prescriptions", padding="10")
        prescriptions_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Prescriptions treeview
        columns = ("Date", "Patient", "Diagnosis", "Medications", "Status")
        self.prescriptions_tree = ttk.Treeview(prescriptions_section, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.prescriptions_tree.heading(col, text=col)
            self.prescriptions_tree.column(col, width=180)
        
        # Add scrollbar
        prescriptions_scrollbar = ttk.Scrollbar(prescriptions_section, orient=tk.VERTICAL, 
                                              command=self.prescriptions_tree.yview)
        self.prescriptions_tree.configure(yscrollcommand=prescriptions_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.prescriptions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prescriptions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load prescriptions
        self.refresh_prescriptions()
    
    def create_vitals_tab(self):
        """Create vitals recording tab"""
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
        self.patient_combo.bind("<<ComboboxSelected>>", self.on_patient_selected)
        
        ttk.Button(selection_frame, text="Load Patient List", 
                  command=self.load_patient_list).pack(side=tk.LEFT)
        
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
        
        # Record button
        ttk.Button(vitals_recording_frame, text="Record Vitals", 
                  command=self.record_vitals).grid(row=row+1, column=1, pady=20)
        
        # Vitals history section
        history_section = ttk.LabelFrame(vitals_frame, text="Vitals History", padding="10")
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
        
        # Load patient list
        self.load_patient_list()
    
    def refresh_today(self):
        """Refresh today's appointments"""
        # Clear existing items
        for item in self.today_tree.get_children():
            self.today_tree.delete(item)
        
        if not self.doctor_id:
            return
        
        # Get today's appointments
        today = date.today()
        appointments = AppointmentManager.get_appointments(doctor_id=self.doctor_id, date_filter=today)
        
        for appointment in appointments:
            self.today_tree.insert("", tk.END, values=(
                appointment['appointment_time'],
                appointment['patient_name'],
                appointment['status'],
                appointment['reason_for_visit'] or 'N/A',
                appointment['notes'] or 'N/A'
            ), tags=(appointment['appointment_id'],))
    
    def refresh_appointments(self):
        """Refresh appointments list with filters"""
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        if not self.doctor_id:
            return
        
        # Apply filters
        date_filter = self.date_filter_var.get().strip() if hasattr(self, 'date_filter_var') else None
        status_filter = self.status_filter_var.get() if hasattr(self, 'status_filter_var') and self.status_filter_var.get() != "All" else None
        
        # Get appointments
        appointments = AppointmentManager.get_appointments(
            doctor_id=self.doctor_id, 
            date_filter=date_filter or None, 
            status=status_filter
        )
        
        for appointment in appointments:
            self.appointments_tree.insert("", tk.END, values=(
                appointment['appointment_date'],
                appointment['appointment_time'],
                appointment['patient_name'],
                appointment['status'],
                appointment['reason_for_visit'] or 'N/A',
                appointment['notes'] or 'N/A'
            ), tags=(appointment['appointment_id'],))
    
    def refresh_patients(self):
        """Refresh patients list"""
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        if not self.doctor_id:
            return
        
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get patients assigned to this doctor
            query = """
            SELECT DISTINCT p.patient_id, u.full_name, u.phone, p.blood_group,
                   MAX(a.appointment_date) as last_visit,
                   COUNT(a.appointment_id) as total_visits
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            LEFT JOIN appointments a ON p.patient_id = a.patient_id AND a.doctor_id = %s
            WHERE a.doctor_id = %s
            GROUP BY p.patient_id, u.full_name, u.phone, p.blood_group
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, (self.doctor_id, self.doctor_id), fetch=True)
            
            for patient in result or []:
                self.patients_tree.insert("", tk.END, values=(
                    patient['full_name'],
                    patient['phone'] or 'N/A',
                    patient['blood_group'] or 'N/A',
                    patient['last_visit'] or 'Never',
                    patient['total_visits']
                ), tags=(patient['patient_id'],))
            
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error refreshing patients: {e}")
    
    def refresh_prescriptions(self):
        """Refresh prescriptions list"""
        # Clear existing items
        for item in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(item)
        
        if not self.doctor_id:
            return
        
        # Apply status filter
        status_filter = self.prescription_status_var.get() if hasattr(self, 'prescription_status_var') and self.prescription_status_var.get() != "All" else None
        
        # Get prescriptions
        prescriptions = PrescriptionManager.get_prescriptions(doctor_id=self.doctor_id, status=status_filter)
        
        for prescription in prescriptions:
            medications_preview = prescription['medications'][:50] + "..." if len(prescription['medications']) > 50 else prescription['medications']
            
            self.prescriptions_tree.insert("", tk.END, values=(
                prescription['prescription_date'],
                prescription['patient_name'],
                prescription['diagnosis'] or 'N/A',
                medications_preview,
                prescription['status']
            ), tags=(prescription['prescription_id'],))
    
    def complete_appointment(self):
        """Mark selected appointment as completed"""
        # Get selected appointment from any tree that has focus
        selected_item = None
        appointment_id = None
        
        if self.notebook.tab(self.notebook.select(), "text") == "Today's Schedule":
            selected_item = self.today_tree.selection()
            if selected_item:
                appointment_id = self.today_tree.item(selected_item[0])['tags'][0]
        else:
            selected_item = self.appointments_tree.selection()
            if selected_item:
                appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to complete")
            return
        
        if AppointmentManager.update_appointment_status(appointment_id, 'Completed'):
            messagebox.showinfo("Success", "Appointment marked as completed")
            self.refresh_today()
            self.refresh_appointments()
        else:
            messagebox.showerror("Error", "Failed to update appointment status")
    
    def add_appointment_notes(self):
        """Add notes to selected appointment"""
        selected_item = self.today_tree.selection() or self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to add notes")
            return
        
        # Get appointment ID
        if self.notebook.tab(self.notebook.select(), "text") == "Today's Schedule":
            appointment_id = self.today_tree.item(selected_item[0])['tags'][0]
        else:
            appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        # Create notes window
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Add Appointment Notes")
        notes_window.geometry("500x400")
        notes_window.grab_set()
        
        # Center the window
        notes_window.update_idletasks()
        width = notes_window.winfo_width()
        height = notes_window.winfo_height()
        x = (notes_window.winfo_screenwidth() // 2) - (width // 2)
        y = (notes_window.winfo_screenheight() // 2) - (height // 2)
        notes_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create content
        main_frame = ttk.Frame(notes_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Appointment Notes:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        notes_text = tk.Text(main_frame, height=15, width=50)
        notes_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_notes():
            notes = notes_text.get("1.0", tk.END).strip()
            if AppointmentManager.update_appointment_status(appointment_id, None, notes):
                messagebox.showinfo("Success", "Notes saved successfully")
                notes_window.destroy()
                self.refresh_today()
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to save notes")
        
        ttk.Button(button_frame, text="Save", style="Modern.TButton", command=save_notes).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", style="Secondary.TButton", command=notes_window.destroy).pack(side=tk.RIGHT)
    
    def reschedule_appointment(self):
        """Reschedule selected appointment"""
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to reschedule")
            return
        
        appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        # For now, just mark as rescheduled - full rescheduling would require date/time picker
        if messagebox.askyesno("Confirm", "Mark this appointment as rescheduled?"):
            if AppointmentManager.update_appointment_status(appointment_id, 'Rescheduled'):
                messagebox.showinfo("Success", "Appointment marked as rescheduled")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to reschedule appointment")
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            if AppointmentManager.update_appointment_status(appointment_id, 'Cancelled'):
                messagebox.showinfo("Success", "Appointment cancelled successfully")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to cancel appointment")
    
    def view_patient_details(self):
        """View detailed patient information"""
        selected_item = self.patients_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to view details")
            return
        
        patient_id = self.patients_tree.item(selected_item[0])['tags'][0]
        
        # Create patient details window
        self.show_patient_details_window(patient_id)
    
    def show_patient_details_window(self, patient_id):
        """Show patient details in a new window"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get patient details
            query = """
            SELECT p.*, u.full_name, u.email, u.phone
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.patient_id = %s
            """
            
            result = db_manager.execute_query(query, (patient_id,), fetch=True)
            
            if not result:
                messagebox.showerror("Error", "Patient not found")
                return
            
            patient = result[0]
            
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Patient Details - {patient['full_name']}")
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
            ttk.Label(main_frame, text=f"Patient: {patient['full_name']}", 
                     font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            # Basic information
            basic_info = [
                ("Email", patient['email']),
                ("Phone", patient['phone']),
                ("Date of Birth", patient['date_of_birth']),
                ("Gender", patient['gender']),
                ("Blood Group", patient['blood_group']),
                ("Emergency Contact", patient['emergency_contact']),
                ("Emergency Phone", patient['emergency_phone'])
            ]
            
            for label, value in basic_info:
                if value:
                    frame = ttk.Frame(main_frame)
                    frame.pack(fill=tk.X, pady=2)
                    ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                    ttk.Label(frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
            
            # Address
            if patient['address']:
                ttk.Label(main_frame, text="Address:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
                address_text = tk.Text(main_frame, height=3, width=60)
                address_text.pack(fill=tk.X, pady=(0, 10))
                address_text.insert("1.0", patient['address'])
                address_text.config(state=tk.DISABLED)
            
            # Medical history
            if patient['medical_history']:
                ttk.Label(main_frame, text="Medical History:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
                history_text = tk.Text(main_frame, height=6, width=60)
                history_text.pack(fill=tk.X, pady=(0, 10))
                history_text.insert("1.0", patient['medical_history'])
                history_text.config(state=tk.DISABLED)
            
            # Allergies
            if patient['allergies']:
                ttk.Label(main_frame, text="Allergies:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
                allergies_text = tk.Text(main_frame, height=4, width=60)
                allergies_text.pack(fill=tk.X, pady=(0, 10))
                allergies_text.insert("1.0", patient['allergies'])
                allergies_text.config(state=tk.DISABLED)
            
            # Recent vitals
            vitals = VitalsManager.get_patient_vitals(patient_id, limit=5)
            if vitals:
                ttk.Label(main_frame, text="Recent Vitals:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
                
                vitals_frame = ttk.Frame(main_frame)
                vitals_frame.pack(fill=tk.X, pady=(0, 10))
                
                for vital in vitals:
                    vital_text = f"{vital['recorded_at']} - BP: {vital['blood_pressure_systolic'] or 'N/A'}/{vital['blood_pressure_diastolic'] or 'N/A'}, HR: {vital['heart_rate'] or 'N/A'}, Temp: {vital['temperature'] or 'N/A'}°F"
                    ttk.Label(vitals_frame, text=vital_text, font=("Arial", 9)).pack(anchor=tk.W)
            
            # Close button
            ttk.Button(main_frame, text="Close", 
                      command=details_window.destroy).pack(pady=20)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            db_manager.disconnect()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading patient details: {str(e)}")
    
    def new_prescription(self):
        """Create new prescription"""
        self.show_prescription_form()
    
    def edit_prescription(self):
        """Edit selected prescription"""
        selected_item = self.prescriptions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a prescription to edit")
            return
        
        prescription_id = self.prescriptions_tree.item(selected_item[0])['tags'][0]
        self.show_prescription_form(prescription_id)
    
    def show_prescription_form(self, prescription_id=None):
        """Show prescription form window"""
        # Create prescription window
        prescription_window = tk.Toplevel(self.root)
        title = "Edit Prescription" if prescription_id else "New Prescription"
        prescription_window.title(title)
        prescription_window.geometry("600x700")
        prescription_window.grab_set()
        
        # Center the window
        prescription_window.update_idletasks()
        width = prescription_window.winfo_width()
        height = prescription_window.winfo_height()
        x = (prescription_window.winfo_screenwidth() // 2) - (width // 2)
        y = (prescription_window.winfo_screenheight() // 2) - (height // 2)
        prescription_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main container
        main_container = tk.Frame(prescription_window)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable content area
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
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
        
        # Create buttons frame outside scrollable area
        button_container = tk.Frame(prescription_window, bg='#f8f9fa', relief='solid', bd=1)
        button_container.pack(fill=tk.X, pady=10, padx=5)
        
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text=title, font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Patient selection
        ttk.Label(main_frame, text="Patient:").pack(anchor=tk.W)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(main_frame, textvariable=patient_var, width=50, state="readonly")
        patient_combo.pack(fill=tk.X, pady=(5, 15))
        
        # Load patients for this doctor
        self.load_doctor_patients(patient_combo)
        
        # Form fields
        form_vars = {}
        
        # Date
        ttk.Label(main_frame, text="Prescription Date:").pack(anchor=tk.W)
        form_vars['prescription_date'] = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        ttk.Entry(main_frame, textvariable=form_vars['prescription_date'], width=50).pack(fill=tk.X, pady=(5, 15))
        
        # Diagnosis
        ttk.Label(main_frame, text="Diagnosis:").pack(anchor=tk.W)
        diagnosis_text = tk.Text(main_frame, height=4, width=50)
        diagnosis_text.pack(fill=tk.X, pady=(5, 15))
        
        # Medications
        ttk.Label(main_frame, text="Medications:").pack(anchor=tk.W)
        medications_text = tk.Text(main_frame, height=8, width=50)
        medications_text.pack(fill=tk.X, pady=(5, 15))
        
        # Dosage instructions
        ttk.Label(main_frame, text="Dosage Instructions:").pack(anchor=tk.W)
        instructions_text = tk.Text(main_frame, height=6, width=50)
        instructions_text.pack(fill=tk.X, pady=(5, 15))
        
        # Notes
        ttk.Label(main_frame, text="Notes:").pack(anchor=tk.W)
        notes_text = tk.Text(main_frame, height=4, width=50)
        notes_text.pack(fill=tk.X, pady=(5, 15))
        
        # Status (for editing)
        if prescription_id:
            ttk.Label(main_frame, text="Status:").pack(anchor=tk.W)
            status_var = tk.StringVar(value="Active")
            status_combo = ttk.Combobox(main_frame, textvariable=status_var, 
                                       values=["Active", "Completed", "Cancelled"], 
                                       width=47, state="readonly")
            status_combo.pack(fill=tk.X, pady=(5, 15))
        
        # Load existing data if editing
        if prescription_id:
            self.load_prescription_data(prescription_id, patient_var, form_vars, 
                                      diagnosis_text, medications_text, instructions_text, 
                                      notes_text, status_var if prescription_id else None)
        
        # Buttons (using the button_container outside scrollable area)
        button_frame = button_container
        
        def save_prescription():
            # Get selected patient
            patient_text = patient_var.get()
            if not patient_text:
                messagebox.showerror("Error", "Please select a patient")
                return
            
            # Extract patient ID from combo text
            try:
                patient_id = int(patient_text.split(" - ID: ")[1])
            except:
                messagebox.showerror("Error", "Invalid patient selection")
                return
            
            # Prepare prescription data
            prescription_data = {
                'patient_id': patient_id,
                'doctor_id': self.doctor_id,
                'appointment_id': None,  # Add appointment_id field (optional for now)
                'prescription_date': form_vars['prescription_date'].get(),
                'diagnosis': diagnosis_text.get("1.0", tk.END).strip() or None,
                'medications': medications_text.get("1.0", tk.END).strip(),
                'dosage_instructions': instructions_text.get("1.0", tk.END).strip() or None,
                'notes': notes_text.get("1.0", tk.END).strip() or None
            }
            
            if prescription_id:
                # Update existing prescription
                if prescription_id:
                    prescription_data['status'] = status_var.get()
                
                if PrescriptionManager.update_prescription(prescription_id, prescription_data):
                    messagebox.showinfo("Success", "Prescription updated successfully")
                    prescription_window.destroy()
                    self.refresh_prescriptions()
                else:
                    messagebox.showerror("Error", "Failed to update prescription")
            else:
                # Create new prescription
                if PrescriptionManager.create_prescription(prescription_data):
                    messagebox.showinfo("Success", "Prescription created successfully")
                    prescription_window.destroy()
                    self.refresh_prescriptions()
                else:
                    messagebox.showerror("Error", "Failed to create prescription")
        
        ttk.Button(button_frame, text="💾 Save Prescription", style="Modern.TButton", command=save_prescription).pack(side=tk.RIGHT, padx=(10, 5), pady=8)
        ttk.Button(button_frame, text="❌ Cancel", style="Secondary.TButton", command=prescription_window.destroy).pack(side=tk.RIGHT, padx=5, pady=8)
    
    def load_doctor_patients(self, combo_widget):
        """Load patients for this doctor in combo box"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get patients assigned to this doctor
            query = """
            SELECT DISTINCT p.patient_id, u.full_name
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            JOIN appointments a ON p.patient_id = a.patient_id
            WHERE a.doctor_id = %s
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, (self.doctor_id,), fetch=True)
            
            values = []
            for patient in result or []:
                values.append(f"{patient['full_name']} - ID: {patient['patient_id']}")
            
            combo_widget['values'] = values
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading patients: {e}")
    
    def load_prescription_data(self, prescription_id, patient_var, form_vars, 
                             diagnosis_text, medications_text, instructions_text, 
                             notes_text, status_var=None):
        """Load existing prescription data for editing"""
        try:
            prescriptions = PrescriptionManager.get_prescriptions()
            prescription = next((p for p in prescriptions if p['prescription_id'] == prescription_id), None)
            
            if prescription:
                # Set patient
                patient_var.set(f"{prescription['patient_name']} - ID: {prescription['patient_id']}")
                
                # Set form fields
                form_vars['prescription_date'].set(prescription['prescription_date'])
                
                # Set text fields
                if prescription['diagnosis']:
                    diagnosis_text.insert("1.0", prescription['diagnosis'])
                
                medications_text.insert("1.0", prescription['medications'])
                
                if prescription['dosage_instructions']:
                    instructions_text.insert("1.0", prescription['dosage_instructions'])
                
                if prescription['notes']:
                    notes_text.insert("1.0", prescription['notes'])
                
                if status_var:
                    status_var.set(prescription['status'])
            
        except Exception as e:
            print(f"Error loading prescription data: {e}")
    
    def delete_prescription(self):
        """Delete selected prescription"""
        selected_item = self.prescriptions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a prescription to delete")
            return
        
        prescription_id = self.prescriptions_tree.item(selected_item[0])['tags'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this prescription?"):
            if PrescriptionManager.update_prescription(prescription_id, {'status': 'Cancelled'}):
                messagebox.showinfo("Success", "Prescription deleted successfully")
                self.refresh_prescriptions()
            else:
                messagebox.showerror("Error", "Failed to delete prescription")
    
    def print_prescription_report(self):
        """Generate and print prescription report for selected patient"""
        selected_item = self.prescriptions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a prescription to generate report")
            return
        
        prescription_id = self.prescriptions_tree.item(selected_item[0])['tags'][0]
        
        # Get prescription details
        prescriptions = PrescriptionManager.get_prescriptions()
        prescription = next((p for p in prescriptions if p['prescription_id'] == prescription_id), None)
        
        if not prescription:
            messagebox.showerror("Error", "Prescription not found")
            return
        
        # Generate report
        self.generate_prescription_report(prescription)
    
    def generate_prescription_report(self, prescription):
        """Generate prescription report"""
        try:
            # Create report window
            report_window = tk.Toplevel(self.root)
            report_window.title("Prescription Report")
            report_window.geometry("800x600")
            
            # Center the window
            report_window.update_idletasks()
            width = report_window.winfo_width()
            height = report_window.winfo_height()
            x = (report_window.winfo_screenwidth() // 2) - (width // 2)
            y = (report_window.winfo_screenheight() // 2) - (height // 2)
            report_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Create report content
            main_frame = ttk.Frame(report_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Header
            header_text = f"""
PRESCRIPTION REPORT
Healthcare Management System

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Doctor: Dr. {self.user_data['full_name']}
Patient: {prescription['patient_name']}
Prescription Date: {prescription['prescription_date']}

----------------------------------------

DIAGNOSIS:
{prescription['diagnosis'] or 'N/A'}

MEDICATIONS:
{prescription['medications']}

DOSAGE INSTRUCTIONS:
{prescription['dosage_instructions'] or 'N/A'}

NOTES:
{prescription['notes'] or 'N/A'}

STATUS: {prescription['status']}

----------------------------------------
Generated by Healthcare Management System
            """
            
            # Text widget for report
            report_text = tk.Text(main_frame, height=30, width=80, font=("Courier", 10))
            report_text.pack(fill=tk.BOTH, expand=True)
            report_text.insert("1.0", header_text.strip())
            report_text.config(state=tk.DISABLED)
            
            # Buttons
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=10)
            
            def save_report():
                from tkinter import filedialog
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Save Prescription Report"
                )
                if filename:
                    try:
                        with open(filename, 'w') as f:
                            f.write(header_text.strip())
                        messagebox.showinfo("Success", f"Report saved to {filename}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save report: {str(e)}")
            
            ttk.Button(button_frame, text="Save Report", command=save_report).pack(side=tk.LEFT)
            ttk.Button(button_frame, text="Close", command=report_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def load_patient_list(self):
        """Load patient list for vitals recording"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get patients assigned to this doctor
            query = """
            SELECT DISTINCT p.patient_id, u.full_name
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            JOIN appointments a ON p.patient_id = a.patient_id
            WHERE a.doctor_id = %s
            ORDER BY u.full_name
            """
            
            result = db_manager.execute_query(query, (self.doctor_id,), fetch=True)
            
            values = []
            for patient in result or []:
                values.append(f"{patient['full_name']} - ID: {patient['patient_id']}")
            
            self.patient_combo['values'] = values
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading patient list: {e}")
    
    def on_patient_selected(self, event=None):
        """Handle patient selection for vitals"""
        patient_text = self.selected_patient_var.get()
        if not patient_text:
            return
        
        try:
            # Extract patient ID from combo text
            patient_id = int(patient_text.split(" - ID: ")[1])
            
            # Load patient vitals history and latest vitals for editing
            self.load_patient_vitals_history(patient_id)
            self.load_latest_vitals_for_editing(patient_id)
            
        except Exception as e:
            print(f"Error loading patient vitals: {e}")
    
    def load_patient_vitals_history(self, patient_id):
        """Load patient vitals history"""
        # Clear existing items
        for item in self.vitals_tree.get_children():
            self.vitals_tree.delete(item)
        
        # Get vitals
        vitals = VitalsManager.get_patient_vitals(patient_id, limit=20)
        
        for vital in vitals:
            bp = f"{vital['blood_pressure_systolic'] or '-'}/{vital['blood_pressure_diastolic'] or '-'}"
            
            self.vitals_tree.insert("", tk.END, values=(
                vital['recorded_at'],
                bp,
                vital['heart_rate'] or '-',
                vital['temperature'] or '-',
                vital['weight'] or '-',
                vital['height'] or '-',
                vital['oxygen_saturation'] or '-',
                vital['recorded_by_name']
            ))
    
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
            else:
                # No existing vitals, clear form
                for var in self.vitals_vars.values():
                    var.set('')
                self.vitals_notes_text.delete('1.0', tk.END)
            
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading latest vitals: {e}")
    
    def load_all_patients_for_scheduling(self, combo):
        """Load all patients for scheduling"""
        try:
            from database.db_config import db_manager
            if db_manager.connect():
                query = """
                SELECT p.patient_id, u.full_name, u.email, u.phone 
                FROM patients p 
                JOIN users u ON p.user_id = u.user_id 
                ORDER BY u.full_name
                """
                patients = db_manager.execute_query(query, fetch=True)
                if patients:
                    patient_values = [f"{p['full_name']} ({p['email']}) - ID: {p['patient_id']}" for p in patients]
                    combo['values'] = patient_values
                db_manager.disconnect()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading patients: {str(e)}")
    
    def load_all_doctors_for_scheduling(self, combo):
        """Load all doctors for scheduling"""
        try:
            from database.db_config import db_manager
            if db_manager.connect():
                query = """
                SELECT d.doctor_id, u.full_name, u.email, d.specialization 
                FROM doctors d 
                JOIN users u ON d.user_id = u.user_id 
                ORDER BY u.full_name
                """
                doctors = db_manager.execute_query(query, fetch=True)
                if doctors:
                    doctor_values = [f"{d['full_name']} - {d['specialization']} ({d['email']}) - ID: {d['doctor_id']}" for d in doctors]
                    combo['values'] = doctor_values
                db_manager.disconnect()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading doctors: {str(e)}")
    
    def record_vitals(self):
        """Record patient vitals"""
        patient_text = self.selected_patient_var.get()
        if not patient_text:
            messagebox.showerror("Error", "Please select a patient")
            return
        
        try:
            # Extract patient ID from combo text
            patient_id = int(patient_text.split(" - ID: ")[1])
            
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
            
            # Add vital measurements (convert to appropriate types)
            for field, var in self.vitals_vars.items():
                value = var.get().strip()
                if value:
                    try:
                        if field in ['blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'oxygen_saturation']:
                            vitals_data[field] = int(float(value))  # Convert to float first, then int
                        elif field in ['temperature', 'weight', 'height']:
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
            
            # Record vitals
            if VitalsManager.record_vitals(vitals_data):
                messagebox.showinfo("Success", "Vitals recorded successfully!")
                
                # Reload vitals history and latest vitals for immediate feedback
                self.load_patient_vitals_history(patient_id)
                self.load_latest_vitals_for_editing(patient_id)
            else:
                messagebox.showerror("Error", "Failed to record vitals")
                
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for measurements")
        except Exception as e:
            messagebox.showerror("Error", f"Error recording vitals: {str(e)}")
    
    def edit_appointment(self):
        """Edit selected appointment details"""
        # Get selected appointment from any tree that has focus
        selected_item = None
        appointment_id = None
        
        if self.notebook.tab(self.notebook.select(), "text") == "Today's Schedule":
            selected_item = self.today_tree.selection()
            if selected_item:
                appointment_id = self.today_tree.item(selected_item[0])['tags'][0]
        else:
            selected_item = self.appointments_tree.selection()
            if selected_item:
                appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to edit")
            return
        
        self.show_appointment_edit_form(appointment_id)
    
    def show_appointment_edit_form(self, appointment_id):
        """Show appointment editing form"""
        from database.db_config import db_manager
        
        if not db_manager.connect():
            return
        
        # Get current appointment data
        query = """
        SELECT a.*, p.full_name as patient_name, u.full_name as doctor_name
        FROM appointments a
        JOIN patients pt ON a.patient_id = pt.patient_id
        JOIN users p ON pt.user_id = p.user_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        JOIN users u ON d.user_id = u.user_id
        WHERE a.appointment_id = %s
        """
        
        result = db_manager.execute_query(query, (appointment_id,), fetch=True)
        
        if not result:
            messagebox.showerror("Error", "Appointment not found")
            return
        
        appointment = result[0]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Appointment - {appointment['patient_name']}")
        edit_window.geometry("500x600")
        edit_window.grab_set()
        
        # Center the window
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main container
        main_container = tk.Frame(edit_window)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Main frame for form content
        main_frame = ttk.Frame(main_container, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button container at bottom
        button_container = tk.Frame(edit_window, bg='#f8f9fa', relief='solid', bd=1)
        button_container.pack(fill=tk.X, pady=10, padx=5)
        
        # Title
        ttk.Label(main_frame, text=f"Edit Appointment", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Patient info (read-only)
        ttk.Label(main_frame, text="Patient:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(main_frame, text=appointment['patient_name'], 
                 font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 10))
        
        # Appointment date
        ttk.Label(main_frame, text="Date:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        date_var = tk.StringVar(value=appointment['appointment_date'].strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(main_frame, textvariable=date_var, width=50)
        date_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Appointment time
        ttk.Label(main_frame, text="Time:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        time_var = tk.StringVar(value=str(appointment['appointment_time']))
        time_entry = ttk.Entry(main_frame, textvariable=time_var, width=50)
        time_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Status
        ttk.Label(main_frame, text="Status:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        status_var = tk.StringVar(value=appointment['status'])
        status_combo = ttk.Combobox(main_frame, textvariable=status_var, 
                                   values=["Scheduled", "Completed", "Cancelled", "Rescheduled"], 
                                   width=47, state="readonly")
        status_combo.pack(fill=tk.X, pady=(5, 10))
        
        # Reason
        ttk.Label(main_frame, text="Reason for Visit:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        reason_text = tk.Text(main_frame, height=4, width=50)
        reason_text.pack(fill=tk.X, pady=(5, 10))
        reason_text.insert("1.0", appointment.get('reason_for_visit', '') or "")
        
        # Notes
        ttk.Label(main_frame, text="Doctor Notes:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        notes_text = tk.Text(main_frame, height=6, width=50)
        notes_text.pack(fill=tk.X, pady=(5, 15))
        notes_text.insert("1.0", appointment['notes'] or "")
        
        # Button frame (using the button_container at bottom)
        button_frame = button_container
        
        def save_appointment():
            try:
                # Validate inputs
                if not date_var.get() or not time_var.get():
                    messagebox.showerror("Error", "Please fill in all required fields")
                    return
                
                # Check for appointment conflicts (exclude current appointment)
                from utils.db_utils import AppointmentManager
                has_conflict, conflicting_appointments, suggested_times = AppointmentManager.check_appointment_conflict(
                    self.user_data['role_id'], date_var.get(), time_var.get(), exclude_appointment_id=appointment_id
                )
                
                if has_conflict:
                    conflict_msg = "⚠️ APPOINTMENT CONFLICT DETECTED\\n\\n"
                    conflict_msg += f"You already have an appointment at {time_var.get()} on {date_var.get()}.\\n"
                    conflict_msg += "This would violate the 30-minute buffer rule.\\n\\n"
                    
                    if conflicting_appointments:
                        conflict_msg += "Conflicting appointment(s):\\n"
                        for apt in conflicting_appointments:
                            conflict_msg += f"• {apt['appointment_time']} - {apt['patient_name']}\\n"
                    
                    if suggested_times:
                        conflict_msg += f"\\n🕐 Suggested alternative times:\\n"
                        for i, time in enumerate(suggested_times, 1):
                            conflict_msg += f"{i}. {time}\\n"
                    
                    conflict_msg += "\\n❓ Do you want to update anyway? (Not recommended)"
                    
                    response = messagebox.askyesno("Appointment Conflict", conflict_msg)
                    if not response:
                        return
                
                # Prepare update data
                update_data = {
                    'appointment_date': date_var.get(),
                    'appointment_time': time_var.get(),
                    'status': status_var.get(),
                    'reason_for_visit': reason_text.get("1.0", tk.END).strip() or None,
                    'notes': notes_text.get("1.0", tk.END).strip() or None
                }
                
                # Update appointment
                if AppointmentManager.update_appointment(appointment_id, update_data):
                    if has_conflict:
                        messagebox.showinfo("Success", "⚠️ Appointment updated with conflict warning!")
                    else:
                        messagebox.showinfo("Success", "✅ Appointment updated successfully!")
                    edit_window.destroy()
                    self.refresh_appointments()
                    self.refresh_today()
                else:
                    messagebox.showerror("Error", "Failed to update appointment")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error updating appointment: {str(e)}")
        
        # Buttons
        ttk.Button(button_frame, text="💾 Save Changes", style="Modern.TButton", command=save_appointment).pack(side=tk.LEFT, padx=(5, 10), pady=8)
        ttk.Button(button_frame, text="❌ Cancel", style="Secondary.TButton", command=edit_window.destroy).pack(side=tk.LEFT, padx=5, pady=8)

    def show_schedule_appointment_form(self):
        """Show the appointment scheduling form for doctors"""
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Schedule Follow-up Appointment")
        schedule_window.geometry("700x800")
        schedule_window.grab_set()
        
        # Apply TTK styling
        self.setup_ttk_styles(schedule_window)
        
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
        
        # Doctor selection - Doctors can schedule for themselves or other doctors
        ttk.Label(main_frame, text="Select Doctor:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(main_frame, textvariable=doctor_var, width=60, state="readonly")
        doctor_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Load patients and doctors
        self.load_all_patients_for_scheduling(patient_combo)
        self.load_all_doctors_for_scheduling(doctor_combo)
        
        # Set current doctor as default
        try:
            # Pre-select current doctor
            doctor_name = self.user_data.get('full_name', '')
            for value in doctor_combo['values']:
                if doctor_name in value:
                    doctor_var.set(value)
                    break
        except:
            pass
        
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
        day_combo['values'] = [str(d).zfill(2) for d in range(1, 32)]
        day_combo.pack(side=tk.LEFT, padx=(5, 0))
        
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
            if col >= 5:  # 5 columns for doctor view
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
                if not patient_var.get():
                    messagebox.showerror("Error", "Please select a patient")
                    return
                
                if not doctor_var.get():
                    messagebox.showerror("Error", "Please select a doctor")
                    return
                
                if not reason_text.get("1.0", tk.END).strip():
                    messagebox.showerror("Error", "Please enter a reason for visit")
                    return
                
                # Extract patient and doctor IDs from selection strings
                patient_id = patient_var.get().split("ID: ")[1]
                doctor_id = doctor_var.get().split("ID: ")[1]
                
                # Format date and time
                appointment_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
                appointment_time = f"{hour_var.get()}:{minute_var.get()}:00"
                
                # Check for appointment conflicts for the selected doctor
                from utils.db_utils import AppointmentManager
                has_conflict, conflicting_appointments, suggested_times = AppointmentManager.check_appointment_conflict(
                    int(doctor_id), appointment_date, appointment_time
                )
                
                if has_conflict:
                    doctor_name = doctor_var.get().split(" - ")[0]
                    conflict_msg = "⚠️ APPOINTMENT CONFLICT DETECTED\\n\\n"
                    conflict_msg += f"Dr. {doctor_name} already has an appointment at {appointment_time} on {appointment_date}.\\n"
                    conflict_msg += "This would violate the 30-minute buffer rule.\\n\\n"
                    
                    if conflicting_appointments:
                        conflict_msg += "Conflicting appointment(s):\\n"
                        for apt in conflicting_appointments:
                            conflict_msg += f"• {apt['appointment_time']} - {apt['patient_name']}\\n"
                    
                    if suggested_times:
                        conflict_msg += f"\\n🕐 Suggested alternative times:\\n"
                        for i, time in enumerate(suggested_times, 1):
                            conflict_msg += f"{i}. {time}\\n"
                    
                    conflict_msg += "\\n❓ Do you want to schedule anyway? (Not recommended)"
                    
                    response = messagebox.askyesno("Appointment Conflict", conflict_msg)
                    if not response:
                        return
                
                # Prepare appointment data
                appointment_data = {
                    'patient_id': int(patient_id),
                    'doctor_id': int(doctor_id),  # Selected doctor
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
                        messagebox.showinfo("Success", "✅ Follow-up appointment scheduled successfully!")
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
    
    def logout(self):
        """Logout and return to login window"""
        self.root.destroy()
        self.parent_window.deiconify()
    
    def on_closing(self):
        """Handle window closing"""
        self.parent_window.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    # Test the doctor dashboard (requires authentication first)
    pass