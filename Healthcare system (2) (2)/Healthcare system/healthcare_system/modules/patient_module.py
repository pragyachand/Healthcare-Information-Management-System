"""
Patient Module - Patient Dashboard and Functionality
Healthcare Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from datetime import datetime, date
from utils.db_utils import AppointmentManager, PrescriptionManager, VitalsManager, UserManager

class PatientDashboard:
    """Patient dashboard interface"""
    
    def __init__(self, user_data, parent_window):
        self.user_data = user_data
        self.parent_window = parent_window
        
        # Complete modern color scheme
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
            'text_secondary': '#6B7280', # Gray text
            'surface': '#F3F4F6',      # Light surface
            'accent': '#DC2626',       # Red accent
            'text_dark': '#1F2937',    # Dark text
            'text_light': '#6B7280',   # Light text
            'hover': '#E5E7EB'         # Hover state
        }
        
        # Create main window
        self.root = tk.Toplevel()
        self.root.title(f"Patient Dashboard - {user_data['full_name']}")
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
        
        # Get patient-specific data
        self.patient_id = user_data.get('role_id')
        
        self.create_dashboard()
    
    def setup_styles(self):
        """Configure modern TTK styles with enhanced visual theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Enhanced fonts
        self.fonts = {
            'header': ('Segoe UI', 18, 'bold'),
            'subheader': ('Segoe UI', 14, 'bold'), 
            'body': ('Segoe UI', 10),
            'button': ('Segoe UI', 10, 'bold'),
            'small': ('Segoe UI', 8)
        }
        
        # Modern button styles
        style.configure('Modern.TButton',
                       font=self.fonts['button'],
                       padding=(20, 10),
                       relief='flat',
                       borderwidth=0,
                       background=self.colors['primary'],
                       foreground='white')
        style.map('Modern.TButton',
                 background=[('active', '#1E40AF'), ('pressed', '#1E3A8A')])
        
        style.configure('Secondary.TButton',
                       font=self.fonts['button'],
                       padding=(20, 10),
                       relief='flat',
                       borderwidth=0,
                       background=self.colors['secondary'],
                       foreground='white')
        style.map('Secondary.TButton',
                 background=[('active', '#7C2D5B'), ('pressed', '#701A47')])
        
        style.configure('Success.TButton',
                       font=self.fonts['button'],
                       padding=(20, 10),
                       relief='flat',
                       borderwidth=0,
                       background=self.colors['success'],
                       foreground='white')
        style.map('Success.TButton',
                 background=[('active', '#059669'), ('pressed', '#047857')])
        
        style.configure('Danger.TButton',
                       font=self.fonts['button'],
                       padding=(20, 10),
                       relief='flat',
                       borderwidth=0,
                       background=self.colors['danger'],
                       foreground='white')
        style.map('Danger.TButton',
                 background=[('active', '#DC2626'), ('pressed', '#B91C1C')])
        
        # Enhanced notebook style
        style.configure('Modern.TNotebook', 
                       background=self.colors['background'],
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        style.configure('Modern.TNotebook.Tab',
                       padding=[25, 15],
                       font=('Segoe UI', 11, 'bold'),
                       focuscolor='none',
                       borderwidth=0)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['hover']),
                           ('!active', self.colors['surface'])],
                 foreground=[('selected', 'white'),
                           ('active', self.colors['text_dark']),
                           ('!active', self.colors['text_light'])])
        
        # Enhanced treeview style
        style.configure('Modern.Treeview',
                       background=self.colors['card'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['card'],
                       font=('Segoe UI', 9),
                       borderwidth=1,
                       relief='solid')
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['surface'],
                       foreground=self.colors['text_dark'],
                       borderwidth=1,
                       relief='flat')
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['hover'])])
        
        # Enhanced labelframe style
        style.configure('Modern.TLabelframe',
                       background=self.colors['card'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['card'],
                       foreground=self.colors['text_dark'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Enhanced entry style
        style.configure('Modern.TEntry',
                       font=self.fonts['body'],
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=10)
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['primary']),
                            ('!focus', self.colors['border'])])
        
        # Enhanced radiobutton style
        style.configure('Modern.TRadiobutton',
                       background=self.colors['card'],
                       foreground=self.colors['text_dark'],
                       font=self.fonts['body'],
                       focuscolor='none')
        
        # Enhanced combobox style
        style.configure('Modern.TCombobox',
                       font=self.fonts['body'],
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=10)
        style.map('Modern.TCombobox',
                 bordercolor=[('focus', self.colors['primary']),
                            ('!focus', self.colors['border'])])
    
    # Window management methods
    def maximize_window(self):
        """Maximize the window"""
        if not self.is_maximized:
            self.normal_geometry = self.root.geometry()
            self.root.state('zoomed')  # Windows-specific maximize
            self.maximize_btn.config(text="❐")
            self.is_maximized = True
    
    def minimize_window(self):
        """Minimize the window"""
        self.root.iconify()
    
    def restore_window(self):
        """Restore window from maximized state"""
        if self.is_maximized:
            self.root.state('normal')
            self.root.geometry(self.normal_geometry)
            self.maximize_btn.config(text="☐")
            self.is_maximized = False
    
    def toggle_maximize(self):
        """Toggle between maximized and normal state"""
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()

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
        else:
            self.maximize_window()
    
    def minimize_window(self):
        """Minimize window to taskbar"""
        self.root.iconify()
    
    def restore_window(self):
        """Restore window from maximized state"""
        if self.is_maximized:
            self.root.state('normal')
            if self.normal_geometry:
                self.root.geometry(self.normal_geometry)
            self.is_maximized = False
    
    def toggle_maximize(self):
        """Toggle between maximized and normal state"""
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_dashboard(self):
        """Create the main dashboard interface with modern styling"""
        # Main container with enhanced styling
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Modern header with enhanced styling
        header_frame = tk.Frame(main_container, bg=self.colors['card'], height=80, relief='flat', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Header content frame with better padding
        header_content = tk.Frame(header_frame, bg=self.colors['card'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Left side - Enhanced patient icon and info
        left_frame = tk.Frame(header_content, bg=self.colors['card'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Enhanced patient icon and title
        title_frame = tk.Frame(left_frame, bg=self.colors['card'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Larger, more prominent icon
        tk.Label(title_frame, text="👤", font=('Segoe UI', 28), 
                bg=self.colors['card'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 15))
        
        info_frame = tk.Frame(title_frame, bg=self.colors['card'])
        info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Enhanced title styling
        tk.Label(info_frame, text="Patient Portal", 
                font=('Segoe UI', 20, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text_dark']).pack(anchor=tk.W)
        
        # Styled welcome message
        tk.Label(info_frame, text=f"Welcome back, {self.user_data['full_name']}", 
                font=('Segoe UI', 12), bg=self.colors['card'], 
                fg=self.colors['text_light']).pack(anchor=tk.W, pady=(2, 0))
        
        # Right side - Enhanced window controls and logout
        right_frame = tk.Frame(header_content, bg=self.colors['card'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enhanced window control buttons
        controls_frame = tk.Frame(right_frame, bg=self.colors['card'])
        controls_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Styled minimize button
        minimize_btn = tk.Button(controls_frame, text="—", font=('Segoe UI', 14, 'bold'), 
                                bg=self.colors['surface'], fg=self.colors['text_dark'],
                                bd=0, padx=12, pady=6, cursor='hand2',
                                command=self.minimize_window, relief='flat')
        minimize_btn.pack(side=tk.LEFT, padx=2)
        
        # Enhanced maximize/restore button
        self.maximize_btn = tk.Button(controls_frame, text="☐", font=('Segoe UI', 14), 
                                     bg=self.colors['surface'], fg=self.colors['text_dark'],
                                     bd=0, padx=12, pady=6, cursor='hand2',
                                     command=self.toggle_maximize, relief='flat')
        self.maximize_btn.pack(side=tk.LEFT, padx=2)
        
        # Enhanced close button
        close_btn = tk.Button(controls_frame, text="✕", font=('Segoe UI', 14, 'bold'), 
                             bg=self.colors['accent'], fg='white',
                             bd=0, padx=12, pady=6, cursor='hand2',
                             command=self.on_closing, relief='flat')
        close_btn.pack(side=tk.LEFT, padx=2)
        
        # Modern logout button with TTK styling
        logout_btn = ttk.Button(right_frame, text="🚪 Logout", 
                               style="Secondary.TButton", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Create modern notebook with enhanced styling
        notebook_frame = tk.Frame(main_container, bg=self.colors['card'], relief='solid', bd=1)
        notebook_frame.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced notebook with custom styling
        self.notebook = ttk.Notebook(notebook_frame, style="Modern.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create tabs with enhanced functionality
        self.create_appointments_tab()
        self.create_prescriptions_tab()
        self.create_profile_tab()
        
        # Set focus to first tab
        self.notebook.select(0)
    
    def create_appointments_tab(self):
        """Create appointments management tab with modern styling"""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="📅 My Appointments")
        
        # Enhanced buttons frame - Positioned at top for visibility
        buttons_container = ttk.Frame(appointments_frame)
        buttons_container.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        appointments_buttons = ttk.Frame(buttons_container)
        appointments_buttons.pack(fill=tk.X)
        
        # Large, prominent scheduling button at top
        schedule_btn = ttk.Button(appointments_buttons, text="📅 Schedule New Appointment", 
                                 style="Modern.TButton", command=self.show_schedule_appointment_form)
        schedule_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary buttons
        ttk.Button(appointments_buttons, text="🔄 Refresh", 
                  style="Secondary.TButton", command=self.refresh_appointments).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(appointments_buttons, text="❌ Cancel Selected", 
                  style="Danger.TButton", command=self.cancel_appointment).pack(side=tk.LEFT, padx=(0, 10))
        
        # Add separator
        separator = ttk.Separator(appointments_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=15, pady=5)
        
        # Enhanced appointments section
        appointments_section = ttk.LabelFrame(appointments_frame, text="Current Appointments", 
                                            padding="15", style="Modern.TLabelframe")
        appointments_section.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))
        
        # Enhanced appointments treeview
        columns = ("Date", "Time", "Doctor", "Specialization", "Status", "Reason")
        self.appointments_tree = ttk.Treeview(appointments_section, columns=columns, 
                                            show="headings", height=15, style="Modern.Treeview")
        
        # Configure columns with better widths
        column_widths = {
            "Date": 120,
            "Time": 100,
            "Doctor": 180,
            "Specialization": 150,
            "Status": 100,
            "Reason": 200
        }
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=column_widths.get(col, 150))
        
        # Add scrollbar with modern styling
        appointments_scrollbar = ttk.Scrollbar(appointments_section, orient=tk.VERTICAL, 
                                             command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=appointments_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        appointments_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load appointments
        self.refresh_appointments()
    
    def create_prescriptions_tab(self):
        """Create prescriptions/medications tab with modern styling"""
        prescriptions_frame = ttk.Frame(self.notebook)
        self.notebook.add(prescriptions_frame, text="💊 My Medications")
        
        # Enhanced active prescriptions section
        active_section = ttk.LabelFrame(prescriptions_frame, text="Active Medications", 
                                      padding="15", style="Modern.TLabelframe")
        active_section.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Enhanced prescriptions treeview
        columns = ("Date", "Doctor", "Diagnosis", "Medications", "Instructions", "Status")
        self.prescriptions_tree = ttk.Treeview(active_section, columns=columns, 
                                             show="headings", height=15, style="Modern.Treeview")
        
        # Configure columns with better widths
        column_widths = {
            "Date": 120,
            "Doctor": 150,
            "Diagnosis": 180,
            "Medications": 200,
            "Instructions": 250,
            "Status": 100
        }
        
        for col in columns:
            self.prescriptions_tree.heading(col, text=col)
            self.prescriptions_tree.column(col, width=column_widths.get(col, 150))
        
        # Add scrollbar with modern styling
        prescriptions_scrollbar = ttk.Scrollbar(active_section, orient=tk.VERTICAL, 
                                              command=self.prescriptions_tree.yview)
        self.prescriptions_tree.configure(yscrollcommand=prescriptions_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.prescriptions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        prescriptions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enhanced buttons frame
        prescriptions_buttons = ttk.Frame(prescriptions_frame)
        prescriptions_buttons.pack(fill=tk.X, padx=15, pady=10)
        
        # Modern styled buttons
        ttk.Button(prescriptions_buttons, text="🔄 Refresh", 
                  style="Secondary.TButton", command=self.refresh_prescriptions).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(prescriptions_buttons, text="📋 View Details", 
                  style="Modern.TButton", command=self.view_prescription_details).pack(side=tk.LEFT, padx=(0, 10))
        
        # Load prescriptions
        self.refresh_prescriptions()
    
    def create_profile_tab(self):
        """Create profile management tab with modern styling"""
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="👤 My Profile")
        
        # Create scrollable frame with modern styling
        canvas = tk.Canvas(profile_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(profile_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main content frame with enhanced styling
        main_frame = ttk.Frame(scrollable_frame, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced basic information section
        basic_section = ttk.LabelFrame(main_frame, text="📋 Basic Information", 
                                     padding="20", style="Modern.TLabelframe")
        basic_section.pack(fill=tk.X, pady=(0, 20))
        
        # Create form variables
        self.profile_vars = {}
        
        # Basic fields with modern styling
        basic_fields = [
            ("Full Name", "full_name", self.user_data.get('full_name', '')),
            ("Email", "email", self.user_data.get('email', '')),
            ("Phone", "phone", self.user_data.get('phone', ''))
        ]
        
        for label, var_name, default_value in basic_fields:
            field_frame = ttk.Frame(basic_section)
            field_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(field_frame, text=f"{label}:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
            self.profile_vars[var_name] = tk.StringVar(value=default_value)
            entry = ttk.Entry(field_frame, textvariable=self.profile_vars[var_name], 
                             width=50, style="Modern.TEntry")
            entry.pack(fill=tk.X, pady=(5, 0))
        
        # Enhanced medical information section
        medical_section = ttk.LabelFrame(main_frame, text="🏥 Medical Information", 
                                       padding="20", style="Modern.TLabelframe")
        medical_section.pack(fill=tk.X, pady=(0, 20))
        
        # Load current patient data
        self.load_patient_profile()
        
        # Medical fields with modern styling
        medical_fields = [
            ("Date of Birth (YYYY-MM-DD)", "date_of_birth"),
            ("Blood Group", "blood_group"),
            ("Emergency Contact", "emergency_contact"),
            ("Emergency Phone", "emergency_phone")
        ]
        
        for label, var_name in medical_fields:
            field_frame = ttk.Frame(medical_section)
            field_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(field_frame, text=f"{label}:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
            if var_name not in self.profile_vars:
                self.profile_vars[var_name] = tk.StringVar()
            entry = ttk.Entry(field_frame, textvariable=self.profile_vars[var_name], 
                             width=50, style="Modern.TEntry")
            entry.pack(fill=tk.X, pady=(5, 0))
        
        # Enhanced gender selection
        gender_frame = ttk.Frame(medical_section)
        gender_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(gender_frame, text="Gender:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        gender_buttons_frame = ttk.Frame(gender_frame)
        gender_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        if "gender" not in self.profile_vars:
            self.profile_vars["gender"] = tk.StringVar(value="Male")
        
        for gender in ["Male", "Female", "Other"]:
            ttk.Radiobutton(gender_buttons_frame, text=gender, variable=self.profile_vars["gender"], 
                           value=gender, style="Modern.TRadiobutton").pack(side=tk.LEFT, padx=(0, 25))
        
        # Enhanced text areas for address, medical history, allergies
        text_fields = [
            ("Address", "address"),
            ("Medical History", "medical_history"),
            ("Allergies", "allergies")
        ]
        
        self.text_widgets = {}
        
        for label, var_name in text_fields:
            field_frame = ttk.Frame(medical_section)
            field_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(field_frame, text=f"{label}:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
            text_widget = tk.Text(field_frame, height=4, width=50, 
                                font=('Segoe UI', 10), bg='white', fg=self.colors['text_dark'],
                                relief='solid', bd=1, padx=10, pady=8)
            text_widget.pack(fill=tk.X, pady=(5, 0))
            self.text_widgets[var_name] = text_widget
        
        # Enhanced update profile button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=25)
        
        ttk.Button(button_frame, text="💾 Update Profile", 
                  style="Success.TButton", command=self.update_profile).pack(pady=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_patient_profile(self):
        """Load current patient profile data"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            query = """
            SELECT p.*, u.full_name, u.email, u.phone
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.patient_id = %s
            """
            
            result = db_manager.execute_query(query, (self.patient_id,), fetch=True)
            
            if result:
                patient_data = result[0]
                
                # Update profile variables
                profile_mapping = {
                    'date_of_birth': 'date_of_birth',
                    'gender': 'gender',
                    'blood_group': 'blood_group',
                    'emergency_contact': 'emergency_contact',
                    'emergency_phone': 'emergency_phone'
                }
                
                for var_name, db_field in profile_mapping.items():
                    if var_name not in self.profile_vars:
                        self.profile_vars[var_name] = tk.StringVar()
                    
                    value = patient_data.get(db_field, '')
                    if value:
                        if var_name == 'date_of_birth' and isinstance(value, date):
                            value = value.strftime('%Y-%m-%d')
                        self.profile_vars[var_name].set(str(value))
                
                # Set text fields after widgets are created
                self.root.after(100, lambda: self.set_text_fields(patient_data))
            
            db_manager.disconnect()
            
        except Exception as e:
            print(f"Error loading patient profile: {e}")
    
    def set_text_fields(self, patient_data):
        """Set values for text widgets"""
        text_mapping = {
            'address': 'address',
            'medical_history': 'medical_history',
            'allergies': 'allergies'
        }
        
        for widget_name, db_field in text_mapping.items():
            if widget_name in self.text_widgets:
                value = patient_data.get(db_field, '')
                if value:
                    self.text_widgets[widget_name].delete("1.0", tk.END)
                    self.text_widgets[widget_name].insert("1.0", str(value))
    
    def refresh_appointments(self):
        """Refresh appointments list"""
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        if not self.patient_id:
            return
        
        # Get appointments
        appointments = AppointmentManager.get_appointments(patient_id=self.patient_id)
        
        for appointment in appointments:
            self.appointments_tree.insert("", tk.END, values=(
                appointment['appointment_date'],
                appointment['appointment_time'],
                appointment['doctor_name'],
                appointment['specialization'],
                appointment['status'],
                appointment['reason_for_visit'] or 'N/A'
            ), tags=(appointment['appointment_id'],))
    
    def refresh_prescriptions(self):
        """Refresh prescriptions list"""
        # Clear existing items
        for item in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(item)
        
        if not self.patient_id:
            return
        
        # Get active prescriptions
        prescriptions = PrescriptionManager.get_prescriptions(patient_id=self.patient_id, status='Active')
        
        for prescription in prescriptions:
            self.prescriptions_tree.insert("", tk.END, values=(
                prescription['prescription_date'],
                prescription['doctor_name'],
                prescription['diagnosis'] or 'N/A',
                prescription['medications'][:50] + "..." if len(prescription['medications']) > 50 else prescription['medications'],
                prescription['dosage_instructions'][:50] + "..." if prescription['dosage_instructions'] and len(prescription['dosage_instructions']) > 50 else prescription['dosage_instructions'] or 'N/A',
                prescription['status']
            ), tags=(prescription['prescription_id'],))
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        # Get appointment ID from tags
        appointment_id = self.appointments_tree.item(selected_item[0])['tags'][0]
        
        # Confirm cancellation
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            if AppointmentManager.update_appointment_status(appointment_id, 'Cancelled'):
                messagebox.showinfo("Success", "Appointment cancelled successfully")
                self.refresh_appointments()
            else:
                messagebox.showerror("Error", "Failed to cancel appointment")
    
    def view_prescription_details(self):
        """View detailed prescription information"""
        selected_item = self.prescriptions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a prescription to view details")
            return
        
        prescription_id = self.prescriptions_tree.item(selected_item[0])['tags'][0]
        
        # Get full prescription details
        prescriptions = PrescriptionManager.get_prescriptions()
        prescription = next((p for p in prescriptions if p['prescription_id'] == prescription_id), None)
        
        if not prescription:
            messagebox.showerror("Error", "Prescription not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Prescription Details")
        details_window.geometry("600x500")
        details_window.grab_set()
        
        # Center the window
        details_window.update_idletasks()
        width = details_window.winfo_width()
        height = details_window.winfo_height()
        x = (details_window.winfo_screenwidth() // 2) - (width // 2)
        y = (details_window.winfo_screenheight() // 2) - (height // 2)
        details_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create content
        main_frame = ttk.Frame(details_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Prescription Details", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Details
        details = [
            ("Date", prescription['prescription_date']),
            ("Doctor", prescription['doctor_name']),
            ("Diagnosis", prescription['diagnosis'] or 'N/A'),
            ("Status", prescription['status'])
        ]
        
        for label, value in details:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Medications
        ttk.Label(main_frame, text="Medications:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        medications_text = tk.Text(main_frame, height=8, width=60)
        medications_text.pack(fill=tk.BOTH, expand=True)
        medications_text.insert("1.0", prescription['medications'])
        medications_text.config(state=tk.DISABLED)
        
        # Dosage instructions
        if prescription['dosage_instructions']:
            ttk.Label(main_frame, text="Dosage Instructions:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
            instructions_text = tk.Text(main_frame, height=6, width=60)
            instructions_text.pack(fill=tk.BOTH, expand=True)
            instructions_text.insert("1.0", prescription['dosage_instructions'])
            instructions_text.config(state=tk.DISABLED)
        
        # Enhanced close button
        ttk.Button(main_frame, text="❌ Close", 
                  style="Secondary.TButton", command=details_window.destroy).pack(pady=20)
    
    def update_profile(self):
        """Update patient profile"""
        try:
            # Get text values
            text_values = {}
            for field_name, text_widget in self.text_widgets.items():
                text_values[field_name] = text_widget.get("1.0", tk.END).strip()
            
            # Prepare update data for users table
            user_update_data = {
                'full_name': self.profile_vars['full_name'].get(),
                'email': self.profile_vars['email'].get(),
                'phone': self.profile_vars['phone'].get()
            }
            
            # Update users table
            if UserManager.update_user_profile(self.user_data['user_id'], user_update_data):
                # Prepare update data for patients table
                from database.db_config import db_manager
                
                if db_manager.connect():
                    patient_update_data = {
                        'date_of_birth': self.profile_vars['date_of_birth'].get() or None,
                        'gender': self.profile_vars['gender'].get(),
                        'address': text_values.get('address') or None,
                        'emergency_contact': self.profile_vars['emergency_contact'].get() or None,
                        'emergency_phone': self.profile_vars['emergency_phone'].get() or None,
                        'blood_group': self.profile_vars['blood_group'].get() or None,
                        'medical_history': text_values.get('medical_history') or None,
                        'allergies': text_values.get('allergies') or None
                    }
                    
                    # Build dynamic update query for patients
                    set_clauses = []
                    params = {}
                    
                    for key, value in patient_update_data.items():
                        if value is not None:
                            set_clauses.append(f"{key} = %({key})s")
                            params[key] = value
                    
                    if set_clauses:
                        params['patient_id'] = self.patient_id
                        query = f"UPDATE patients SET {', '.join(set_clauses)} WHERE patient_id = %(patient_id)s"
                        db_manager.execute_query(query, params)
                    
                    db_manager.disconnect()
                
                messagebox.showinfo("Success", "Profile updated successfully!")
                
                # Update user data
                self.user_data['full_name'] = self.profile_vars['full_name'].get()
                self.user_data['email'] = self.profile_vars['email'].get()
                self.user_data['phone'] = self.profile_vars['phone'].get()
                
            else:
                messagebox.showerror("Error", "Failed to update profile")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error updating profile: {str(e)}")
    
    def show_schedule_appointment_form(self):
        """Show the appointment scheduling form for patients"""
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Schedule New Appointment")
        schedule_window.geometry("650x800")  # Increased height to ensure buttons are visible
        schedule_window.grab_set()
        schedule_window.resizable(True, True)  # Allow resizing
        
        # Main container with scrollable content
        main_container = ttk.Frame(schedule_window)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Canvas has been destroyed, ignore the event
        
        def cleanup_bindings():
            try:
                canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        schedule_window.protocol("WM_DELETE_WINDOW", lambda: [cleanup_bindings(), schedule_window.destroy()])
        
        # Title
        title_label = tk.Label(main_frame, text="Schedule New Appointment", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Doctor selection
        ttk.Label(main_frame, text="Select Doctor:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(main_frame, textvariable=doctor_var, width=60, state="readonly")
        doctor_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Load doctors
        try:
            from database.db_config import db_manager
            if db_manager.connect():
                query = """
                SELECT d.doctor_id, u.full_name, d.specialization
                FROM doctors d 
                JOIN users u ON d.user_id = u.user_id 
                ORDER BY d.specialization, u.full_name
                """
                doctors = db_manager.execute_query(query, fetch=True)
                doctor_values = [f"Dr. {d['full_name']} - {d['specialization']} - ID: {d['doctor_id']}" for d in doctors]
                doctor_combo['values'] = doctor_values
                db_manager.disconnect()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading doctors: {str(e)}")
        
        # Specialty filter (optional)
        ttk.Label(main_frame, text="Filter by Specialty (Optional):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        specialty_var = tk.StringVar()
        specialty_combo = ttk.Combobox(main_frame, textvariable=specialty_var, width=60, state="readonly")
        
        # Load specialties
        try:
            from database.db_config import db_manager
            if db_manager.connect():
                query = "SELECT DISTINCT specialization FROM doctors ORDER BY specialization"
                specialties = db_manager.execute_query(query, fetch=True)
                specialty_values = ["All Specialties"] + [s['specialization'] for s in specialties]
                specialty_combo['values'] = specialty_values
                specialty_combo.set("All Specialties")
                db_manager.disconnect()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading specialties: {str(e)}")
        
        specialty_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Function to filter doctors by specialty
        def filter_doctors():
            selected_specialty = specialty_var.get()
            if selected_specialty == "All Specialties":
                # Show all doctors
                doctor_combo['values'] = doctor_values
            else:
                # Filter by specialty
                filtered_values = [doc for doc in doctor_values if selected_specialty in doc]
                doctor_combo['values'] = filtered_values
            doctor_combo.set("")  # Clear selection
        
        specialty_combo.bind('<<ComboboxSelected>>', lambda e: filter_doctors())
        
        # Date selection
        ttk.Label(main_frame, text="Preferred Appointment Date:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        from datetime import datetime, timedelta
        
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
        # Default to tomorrow if today is not the last day of month, otherwise first day of next month
        tomorrow = datetime.now() + timedelta(days=1)
        day_var = tk.StringVar(value=str(tomorrow.day).zfill(2))
        ttk.Label(date_frame, text="Day:").pack(side=tk.LEFT)
        day_combo = ttk.Combobox(date_frame, textvariable=day_var, width=8, state="readonly")
        day_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Function to update day combobox based on selected year and month (disable past dates)
        def update_day_combobox():
            try:
                from calendar import monthrange
                
                selected_year = int(year_var.get())
                selected_month = int(month_var.get())
                current_date = datetime.now()
                
                # Get the number of days in the selected month
                _, max_days = monthrange(selected_year, selected_month)
                
                # If selected year/month is current year/month, only show days from today onwards
                if selected_year == current_date.year and selected_month == current_date.month:
                    current_day = current_date.day
                    valid_days = [str(d).zfill(2) for d in range(current_day + 1, max_days + 1)]  # +1 to exclude today
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
        ttk.Label(main_frame, text="Preferred Time:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
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
        
        # Reason for visit
        ttk.Label(main_frame, text="Reason for Visit:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        reason_text = tk.Text(main_frame, height=4, width=60)
        reason_text.pack(fill=tk.X, pady=(0, 10))
        
        # Additional notes (optional)
        ttk.Label(main_frame, text="Additional Information (Optional):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        notes_text = tk.Text(main_frame, height=3, width=60)
        notes_text.pack(fill=tk.X, pady=(0, 10))
        
        # Information note
        info_label = tk.Label(main_frame, 
                             text="📌 Note: Your appointment request will be scheduled if available.",
                             font=("Arial", 9), 
                             fg="blue", 
                             justify=tk.LEFT)
        info_label.pack(pady=(5, 15))
        
        # Buttons Frame - Always at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 20), side=tk.BOTTOM)
        
        def save_appointment():
            try:
                # Validate inputs
                if not doctor_var.get():
                    messagebox.showerror("Error", "Please select a doctor")
                    return
                
                if not reason_text.get("1.0", tk.END).strip():
                    messagebox.showerror("Error", "Please enter a reason for visit")
                    return
                
                # Extract doctor ID from selection string
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
                
                # Prepare appointment data
                appointment_data = {
                    'patient_id': self.patient_id,  # Current patient's ID (already set from role_id)
                    'doctor_id': int(doctor_id),
                    'appointment_date': appointment_date,
                    'appointment_time': appointment_time,
                    'reason_for_visit': reason_text.get("1.0", tk.END).strip(),
                    'notes': notes_text.get("1.0", tk.END).strip() or None
                }
                
                # Create the appointment
                from utils.db_utils import AppointmentManager
                if AppointmentManager.create_appointment(appointment_data):
                    messagebox.showinfo("Success", 
                                      "Appointment scheduled successfully!\n\n" +
                                      f"Doctor: {doctor_var.get().split(' - ID:')[0]}\n" +
                                      f"Date: {appointment_date}\n" +
                                      f"Time: {hour_var.get()}:{minute_var.get()}\n\n" +
                                      "You will receive confirmation shortly.")
                    schedule_window.destroy()
                    self.refresh_appointments()  # Refresh the appointments list
                else:
                    messagebox.showerror("Error", "Failed to schedule appointment. The time slot may already be taken.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error scheduling appointment: {str(e)}")
        
        ttk.Button(button_frame, text="💾 Schedule Appointment", 
                  style="Success.TButton", command=save_appointment).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancel", 
                  style="Secondary.TButton", command=schedule_window.destroy).pack(side=tk.LEFT)
    
    def logout(self):
        """Logout and return to login window"""
        self.root.destroy()
        self.parent_window.deiconify()
    
    def on_closing(self):
        """Handle window closing"""
        self.parent_window.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    # Test the patient dashboard (requires authentication first)
    pass