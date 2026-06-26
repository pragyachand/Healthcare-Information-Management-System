"""
Authentication System - Login and Registration
Healthcare Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from utils.db_utils import UserManager
from datetime import datetime

class LoginWindow:
    """Login window for the healthcare system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Healthcare Management System - Login")
        self.root.geometry("800x900")
        self.root.resizable(True, True)  # Make it resizable like registration
        self.root.minsize(600, 700)  # Set minimum size
        
        # Initialize window state tracking
        self.is_maximized = False
        self.normal_geometry = None
        
        # Modern color scheme
        self.colors = {
            'primary': '#2E86AB',      # Medical blue
            'secondary': '#A23B72',    # Accent purple
            'success': '#F18F01',      # Orange accent
            'background': '#F5F7FA',   # Light gray background
            'card': '#FFFFFF',         # White cards
            'text_primary': '#2D3748', # Dark gray text
            'text_secondary': '#718096', # Medium gray text
            'border': '#E2E8F0',       # Light border
            'hover': '#3182CE'         # Hover blue
        }
        
        # Configure root styling
        self.root.configure(bg=self.colors['background'])
        
        # Configure ttk styles
        self.setup_styles()
        
        # Center the window
        self.center_window()
        
        # User session data
        self.current_user = None
        
        self.create_login_interface()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('Modern.TNotebook', 
                       background=self.colors['background'])
        style.configure('Modern.TNotebook.Tab',
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['card'],
                       relief='flat',
                       borderwidth=2)
        
        # Configure button styles
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=[20, 10])
        
        style.configure('Secondary.TButton',
                       font=('Arial', 9),
                       padding=[15, 8])
        
        # Configure label styles
        style.configure('Title.TLabel',
                       font=('Arial', 18, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12),
                       background=self.colors['card'],
                       foreground=self.colors['text_secondary'])
        
        style.configure('Card.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['text_primary'])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       padding=[10, 8],
                       font=('Arial', 10))

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def maximize_window(self):
        """Maximize window to full screen"""
        if not self.is_maximized:
            self.normal_geometry = self.root.geometry()
            self.root.state('zoomed')
            self.is_maximized = True
            # Update maximize button text
            if hasattr(self, 'maximize_btn'):
                self.maximize_btn.config(text="🗗")
    
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
            # Update maximize button text
            if hasattr(self, 'maximize_btn'):
                self.maximize_btn.config(text="🗖")
    
    def toggle_maximize(self):
        """Toggle between maximized and normal state"""
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()
    
    def create_login_interface(self):
        """Create the modern login interface"""
        # Main container with background
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Modern header with window controls
        header_frame = tk.Frame(main_container, bg=self.colors['card'], height=60, relief='flat')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Header content frame
        header_content = tk.Frame(header_frame, bg=self.colors['card'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Application title
        left_frame = tk.Frame(header_content, bg=self.colors['card'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # App icon and title
        title_frame = tk.Frame(left_frame, bg=self.colors['card'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(title_frame, text="🏥", font=('Segoe UI', 20), 
                bg=self.colors['card'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 12))
        
        info_frame = tk.Frame(title_frame, bg=self.colors['card'])
        info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(info_frame, text="Healthcare Management System", 
                font=('Segoe UI', 14, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        tk.Label(info_frame, text="Secure Medical Records Management", 
                font=('Segoe UI', 9), bg=self.colors['card'], 
                fg=self.colors['text_secondary']).pack(anchor=tk.W)
        
        # Right side - Window controls
        right_frame = tk.Frame(header_content, bg=self.colors['card'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Window control buttons
        controls_frame = tk.Frame(right_frame, bg=self.colors['card'])
        controls_frame.pack(side=tk.RIGHT)
        
        # Minimize button
        minimize_btn = tk.Button(controls_frame, text="🗕", font=('Segoe UI', 11), 
                                bg=self.colors['card'], fg=self.colors['text_primary'],
                                bd=0, padx=8, pady=3, cursor='hand2',
                                command=self.minimize_window)
        minimize_btn.pack(side=tk.LEFT, padx=2)
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(controls_frame, text="🗖", font=('Segoe UI', 11), 
                                     bg=self.colors['card'], fg=self.colors['text_primary'],
                                     bd=0, padx=8, pady=3, cursor='hand2',
                                     command=self.toggle_maximize)
        self.maximize_btn.pack(side=tk.LEFT, padx=2)
        
        # Close button
        close_btn = tk.Button(controls_frame, text="🗙", font=('Segoe UI', 11), 
                             bg=self.colors['card'], fg=self.colors['secondary'],
                             bd=0, padx=8, pady=3, cursor='hand2',
                             command=self.root.quit)
        close_btn.pack(side=tk.LEFT, padx=2)
        
        # Content container with three columns layout using grid
        content_container = tk.Frame(main_container, bg=self.colors['background'])
        content_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for responsive design
        content_container.grid_columnconfigure(0, weight=2, minsize=320)  # Left column (wider)
        content_container.grid_columnconfigure(1, weight=4, minsize=500)  # Center column (wider)
        content_container.grid_columnconfigure(2, weight=2, minsize=320)  # Right column (wider)
        content_container.grid_rowconfigure(0, weight=1)
        
        # Create three columns using grid for better alignment
        left_column = tk.Frame(content_container, bg=self.colors['background'])
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        center_column = tk.Frame(content_container, bg=self.colors['background'])
        center_column.grid(row=0, column=1, sticky='nsew', padx=15)
        
        right_column = tk.Frame(content_container, bg=self.colors['background'])
        right_column.grid(row=0, column=2, sticky='nsew', padx=(15, 0))
        
        # Center column content wrapper for proper vertical centering
        center_wrapper = tk.Frame(center_column, bg=self.colors['background'])
        center_wrapper.place(relx=0.5, rely=0.5, anchor='center')
        
        # Login card with prominent styling - increased height to show signup
        login_card = tk.Frame(center_wrapper, bg=self.colors['card'], relief='solid', bd=2, width=450, height=520)
        login_card.pack(padx=15)
        login_card.pack_propagate(False)
        
        # Login card inner padding
        login_inner = tk.Frame(login_card, bg=self.colors['card'])
        login_inner.pack(fill=tk.BOTH, padx=25, pady=15)
        
        # Login header with icon
        login_header = tk.Label(login_inner, text="🏥 Healthcare System Login", 
                               font=('Arial', 15, 'bold'), 
                               bg=self.colors['card'], fg=self.colors['primary'])
        login_header.pack(pady=(0, 15))
        
        # Username field with modern styling
        tk.Label(login_inner, text="Username", 
                font=('Arial', 12, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0, 8))
        
        self.username_entry = tk.Entry(login_inner, font=('Arial', 12), 
                                      bg='white', fg=self.colors['text_primary'],
                                      relief='solid', bd=2, highlightthickness=1,
                                      highlightcolor=self.colors['primary'],
                                      insertbackground=self.colors['text_primary'])
        self.username_entry.pack(fill=tk.X, pady=(0, 10), ipady=6)
        self.username_entry.focus()
        
        # Password field
        tk.Label(login_inner, text="Password", 
                font=('Arial', 12, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0, 8))
        
        self.password_entry = tk.Entry(login_inner, show="*", font=('Arial', 12),
                                      bg='white', fg=self.colors['text_primary'],
                                      relief='solid', bd=2, highlightthickness=1,
                                      highlightcolor=self.colors['primary'],
                                      insertbackground=self.colors['text_primary'])
        self.password_entry.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # Login button with prominent styling
        login_btn = tk.Button(login_inner, text="🔑 Sign In", 
                             command=self.login,
                             font=('Arial', 14, 'bold'),
                             bg=self.colors['primary'], fg='white',
                             relief='flat', bd=0, cursor='hand2',
                             pady=15, activebackground=self.colors['hover'])
        login_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Divider
        divider = tk.Frame(login_inner, bg=self.colors['border'], height=1)
        divider.pack(fill=tk.X, pady=10)
        
        # Register section with maximum visibility
        register_frame = tk.Frame(login_inner, bg='#F0F8FF', relief='solid', bd=1)
        register_frame.pack(fill=tk.X, pady=(10, 0))
        
        register_inner = tk.Frame(register_frame, bg='#F0F8FF')
        register_inner.pack(fill=tk.X, padx=15, pady=15)
        
        register_text = tk.Label(register_inner, text="🆕 New to the system?", 
                               font=('Arial', 12, 'bold'), bg='#F0F8FF', 
                               fg=self.colors['text_primary'])
        register_text.pack()
        
        register_btn = tk.Button(register_inner, text="📝 CREATE NEW ACCOUNT", 
                               command=self.open_registration,
                               font=('Arial', 11, 'bold'),
                               bg=self.colors['secondary'], fg='white',
                               relief='flat', bd=0, cursor='hand2',
                               pady=10, activebackground='#8B2F5A')
        register_btn.pack(pady=(10, 0), fill=tk.X)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Add placeholder text to input fields
        self.username_entry.insert(0, "Enter username...")
        self.username_entry.bind('<FocusIn>', self.on_username_focus_in)
        self.username_entry.bind('<FocusOut>', self.on_username_focus_out)
        
        self.password_entry.bind('<FocusIn>', self.on_password_focus_in)
        

        
        # Store references to center column for info page display
        self.center_column = center_column
        self.center_wrapper = center_wrapper
        self.login_card = login_card
        self.login_card_parent = center_wrapper  # Store parent for proper restoration
        
        # Create info page container (initially hidden)
        self.info_page_container = tk.Frame(center_column, bg=self.colors['background'])
        
        # Left column - Clickable menu sidebar
        self.create_menu_sidebar(left_column)
        
        # Right column - Quick access info with vertical centering  
        right_wrapper = tk.Frame(right_column, bg=self.colors['background'])
        right_wrapper.place(relx=0.5, rely=0.5, anchor='center')
        self.create_quick_access_card(right_wrapper)
    
    def create_menu_sidebar(self, parent):
        """Create clickable menu sidebar for feature browsing"""
        # Menu sidebar card
        menu_card = tk.Frame(parent, bg=self.colors['card'], relief='solid', bd=1)
        menu_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Menu inner padding
        menu_inner = tk.Frame(menu_card, bg=self.colors['card'])
        menu_inner.pack(fill=tk.BOTH, padx=15, pady=20)
        
        # Menu header
        menu_header = tk.Label(menu_inner, text="📋 System Features", 
                                  font=('Arial', 16, 'bold'), 
                                  bg=self.colors['card'], fg=self.colors['primary'])
        menu_header.pack(anchor=tk.W, pady=(0, 20))
        
        # Menu items with clickable buttons
        menu_items = [
            ("📅", "Appointment Management", "appointment"),
            ("📋", "Medical Records", "medical_records"),
            ("💊", "Prescription Management", "prescription"),
            ("📊", "Vital Signs Monitoring", "vitals"),
            ("👥", "User Management", "user_management"),
            ("📈", "Reports & Analytics", "reports"),
            ("🔒", "Security & Access", "security")
        ]
        
        for icon, label, feature_key in menu_items:
            menu_btn = tk.Button(menu_inner, 
                                text=f"{icon} {label}",
                                   font=('Arial', 11), 
                                bg=self.colors['card'],
                                fg=self.colors['text_primary'],
                                relief='flat',
                                bd=1,
                                anchor='w',
                                cursor='hand2',
                                padx=15,
                                pady=12,
                                activebackground=self.colors['hover'],
                                activeforeground='white',
                                command=lambda key=feature_key: self.show_feature_info(key))
            menu_btn.pack(fill=tk.X, pady=5)
            menu_btn.bind('<Enter>', lambda e, btn=menu_btn: btn.config(bg=self.colors['hover'], fg='white'))
            menu_btn.bind('<Leave>', lambda e, btn=menu_btn: btn.config(bg=self.colors['card'], fg=self.colors['text_primary']))
    
    def show_feature_info(self, feature_key):
        """Show information page for selected feature"""
        # Hide login form
        self.login_card.pack_forget()
        
        # Clear previous info page if exists
        for widget in self.info_page_container.winfo_children():
            widget.destroy()
        
        # Show info page container
        self.info_page_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create info page content
        info_card = tk.Frame(self.info_page_container, bg=self.colors['card'], relief='solid', bd=2, width=500, height=600)
        info_card.pack()
        info_card.pack_propagate(False)
        
        info_inner = tk.Frame(info_card, bg=self.colors['card'])
        info_inner.pack(fill=tk.BOTH, padx=30, pady=30)
        
        # Feature information dictionary
        feature_info = {
            "appointment": {
                "icon": "📅",
                "title": "Appointment Management",
                "description": """Our Appointment Management system allows healthcare providers to efficiently schedule, track, and manage patient visits.

Key Features:
• Schedule appointments with doctors, nurses, and specialists
• View upcoming and past appointments
• Send appointment reminders
• Manage appointment cancellations and rescheduling
• Track appointment history and statistics
• Integration with patient and doctor calendars

This module ensures smooth coordination between patients and healthcare providers, reducing wait times and improving patient satisfaction.""",
                "access": "Available to: Doctors, Nurses, Patients, and Administrators"
            },
            "medical_records": {
                "icon": "📋",
                "title": "Medical Records",
                "description": """Our Medical Records system provides secure storage and management of patient health information using advanced encryption.

Key Features:
• Comprehensive patient medical history
• Secure document storage and retrieval
• Encrypted data transmission
• Access control based on user roles
• Medical history tracking
• Lab results and diagnostic reports
• Treatment plans and progress notes

All medical records are stored securely with encryption to protect patient privacy and comply with healthcare regulations.""",
                "access": "Available to: Doctors, Nurses, and Administrators (with patient consent)"
            },
            "prescription": {
                "icon": "💊",
                "title": "Prescription Management",
                "description": """The Prescription Management module streamlines the process of prescribing and tracking medications.

Key Features:
• Digital prescription creation and management
• Medication dosage and frequency tracking
• Prescription history for patients
• Drug interaction warnings
• Refill reminders and notifications
• Prescription status tracking (Active, Completed, Cancelled)
• Integration with pharmacy systems

This system helps prevent medication errors and ensures patients receive proper medication management.""",
                "access": "Available to: Doctors (prescribe), Nurses (view), Patients (view own)"
            },
            "vitals": {
                "icon": "📊",
                "title": "Vital Signs Monitoring",
                "description": """Vital Signs Monitoring allows healthcare providers to record and track essential patient health metrics.

Key Features:
• Record vital signs (Blood Pressure, Temperature, Heart Rate, etc.)
• Track vital signs over time with charts
• Set alert thresholds for abnormal values
• Generate vital signs reports
• Historical data analysis
• Integration with medical devices
• Real-time monitoring capabilities

This module helps healthcare providers monitor patient health status and detect potential issues early.""",
                "access": "Available to: Doctors, Nurses (record), Patients (view own)"
            },
            "user_management": {
                "icon": "👥",
                "title": "User Management",
                "description": """User Management provides administrators with comprehensive tools to manage system users and their access.

Key Features:
• Create and manage user accounts
• Role-based access control (Admin, Doctor, Nurse, Patient)
• User profile management
• Account activation and deactivation
• Password reset and security management
• User activity tracking
• Bulk user operations

Administrators can efficiently manage all system users while maintaining security and access control.""",
                "access": "Available to: Administrators only"
            },
            "reports": {
                "icon": "📈",
                "title": "Reports & Analytics",
                "description": """The Reports & Analytics module provides comprehensive insights into system usage and healthcare metrics.

Key Features:
• System usage statistics
• Patient and appointment reports
• Doctor performance analytics
• User activity reports
• Export reports to PDF format
• Custom report generation
• Data visualization and charts
• Scheduled report generation

This module helps administrators and healthcare providers make data-driven decisions and track system performance.""",
                "access": "Available to: Administrators and Doctors"
            },
            "security": {
                "icon": "🔒",
                "title": "Security & Access Control",
                "description": """Our Security & Access Control system ensures that patient data and system resources are protected.

Key Features:
• Role-based access control (RBAC)
• Secure authentication system
• Data encryption for sensitive information
• Audit logs for system activities
• Session management
• Password policies and requirements
• Multi-factor authentication support
• HIPAA compliance features

The system implements industry-standard security practices to protect patient privacy and ensure data integrity.""",
                "access": "Security features are active for all users"
            }
        }
        
        info = feature_info.get(feature_key, {
            "icon": "ℹ️",
            "title": "Feature Information",
            "description": "Information about this feature is not available.",
            "access": "Contact administrator for access information"
        })
        
        # Title
        title_label = tk.Label(info_inner, 
                              text=f"{info['icon']} {info['title']}",
                              font=('Arial', 18, 'bold'),
                              bg=self.colors['card'],
                              fg=self.colors['primary'],
                              wraplength=440,
                              justify='left')
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Description
        desc_label = tk.Label(info_inner,
                             text=info['description'],
                             font=('Arial', 10),
                             bg=self.colors['card'],
                             fg=self.colors['text_primary'],
                             wraplength=440,
                             justify='left',
                             anchor='w')
        desc_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Access info
        access_frame = tk.Frame(info_inner, bg='#F0F8FF', relief='solid', bd=1)
        access_frame.pack(fill=tk.X, pady=(10, 0))
        
        access_inner = tk.Frame(access_frame, bg='#F0F8FF')
        access_inner.pack(fill=tk.X, padx=15, pady=12)
        
        access_label = tk.Label(access_inner,
                               text=f"🔐 {info['access']}",
                               font=('Arial', 10, 'bold'),
                               bg='#F0F8FF',
                               fg=self.colors['text_primary'],
                               wraplength=410,
                               justify='left',
                               anchor='w')
        access_label.pack(anchor=tk.W)
        
        # Back to Login button
        back_btn = tk.Button(info_inner,
                             text="← Back to Login",
                             font=('Arial', 12, 'bold'),
                             bg=self.colors['primary'],
                             fg='white',
                             relief='flat',
                             bd=0,
                             cursor='hand2',
                             padx=20,
                             pady=12,
                             activebackground=self.colors['hover'],
                             command=self.back_to_login)
        back_btn.pack(pady=(20, 0))
    
    def back_to_login(self):
        """Return to login form"""
        # Hide info page
        self.info_page_container.place_forget()
        
        # Clear info page container
        for widget in self.info_page_container.winfo_children():
            widget.destroy()
        
        # Show login form
        self.login_card.pack(padx=15)
    
    def create_quick_access_card(self, parent):
        """Create quick access information card for right column"""
        return  # Temporarily disabled
        
        # Access card inner padding
        access_inner = tk.Frame(access_card, bg=self.colors['card'])
        access_inner.pack(fill=tk.BOTH, padx=25, pady=25)
        
        # Access header
        access_header = tk.Label(access_inner, text="🚀 Quick Access", 
                                font=('Arial', 16, 'bold'), 
                                bg=self.colors['card'], fg=self.colors['secondary'])
        access_header.pack(anchor=tk.W, pady=(0, 20))
        
        # Role buttons info
        roles_info = [
            ("👨‍💼 Admin Access", "admin / admin123"),
            ("👨‍⚕️ Doctor Login", "dr_smith / doctor123"),
            ("👩‍⚕️ Nurse Portal", "nurse_davis / nurse123"),
            ("🏥 Patient Area", "patient_jones / patient123")
        ]
        
        for role_name, credentials in roles_info:
            role_frame = tk.Frame(access_inner, bg=self.colors['card'])
            role_frame.pack(fill=tk.X, pady=8)
            
            role_label = tk.Label(role_frame, text=role_name, 
                                 font=('Arial', 11, 'bold'), 
                                 bg=self.colors['card'], fg=self.colors['text_primary'])
            role_label.pack(anchor=tk.W)
            
            cred_label = tk.Label(role_frame, text=credentials, 
                                 font=('Arial', 9), 
                                 bg=self.colors['card'], fg=self.colors['text_secondary'])
            cred_label.pack(anchor=tk.W)

    def on_username_focus_in(self, event):
        """Clear placeholder text when username field gets focus"""
        if self.username_entry.get() == "Enter username...":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg=self.colors['text_primary'])
    
    def on_username_focus_out(self, event):
        """Add placeholder text back if username field is empty"""
        if not self.username_entry.get():
            self.username_entry.insert(0, "Enter username...")
            self.username_entry.config(fg=self.colors['text_secondary'])
    
    def on_password_focus_in(self, event):
        """Handle password field focus"""
        pass  # Password field doesn't need placeholder due to show="*"

    def login(self):
        """Handle user login"""
        # Get values directly from Entry widgets
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Remove placeholder text from validation
        if username == "Enter username...":
            username = ""
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Authenticate user
        user = UserManager.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
            self.redirect_to_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
    
    def redirect_to_dashboard(self):
        """Redirect user to appropriate dashboard based on role"""
        if not self.current_user:
            return
        
        role = self.current_user['role']
        
        # Hide login window
        self.root.withdraw()
        
        try:
            if role == 'admin':
                from modules.admin_module import AdminDashboard
                AdminDashboard(self.current_user, self.root)
            elif role == 'doctor':
                from modules.doctor_module import DoctorDashboard
                DoctorDashboard(self.current_user, self.root)
            elif role == 'nurse':
                from modules.nurse_module import NurseDashboard
                NurseDashboard(self.current_user, self.root)
            elif role == 'patient':
                from modules.patient_module import PatientDashboard
                PatientDashboard(self.current_user, self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Module not found: {e}")
            self.root.deiconify()
    
    def open_registration(self):
        """Open registration window"""
        RegistrationWindow(self.root)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

class RegistrationWindow:
    """Registration window for new users"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("User Registration")
        self.window.geometry("600x750")
        self.window.resizable(True, True)  # Make it resizable
        self.window.minsize(500, 600)  # Set minimum size
        self.window.grab_set()  # Make window modal
        
        # Initialize window state tracking
        self.is_maximized = False
        self.normal_geometry = None
        
        # Setup modern styling
        self.setup_styles()
        
        # Center the window
        self.center_window()
        
        self.create_registration_interface()
    
    def setup_styles(self):
        """Setup modern styling and color scheme"""
        # Modern medical color palette
        self.colors = {
            'primary': '#2E86AB',      # Deep blue
            'secondary': '#A23B72',    # Deep pink
            'accent': '#F18F01',       # Orange
            'success': '#C73E1D',      # Red
            'background': '#F5F7FA',   # Light gray
            'card': '#FFFFFF',         # White
            'text_dark': '#2C3E50',    # Dark blue-gray
            'text_light': '#7F8C8D',   # Light gray
            'border': '#E1E8ED',       # Light border
            'hover': '#3498DB'         # Light blue
        }
        
        # Configure window
        self.window.configure(bg=self.colors['background'])
    
    def maximize_window(self):
        """Maximize window to full screen"""
        if not self.is_maximized:
            self.normal_geometry = self.window.geometry()
            self.window.state('zoomed')
            self.is_maximized = True
            # Update maximize button text
            if hasattr(self, 'maximize_btn'):
                self.maximize_btn.config(text="🗗")
    
    def minimize_window(self):
        """Minimize window to taskbar"""
        self.window.iconify()
    
    def restore_window(self):
        """Restore window from maximized state"""
        if self.is_maximized:
            self.window.state('normal')
            if self.normal_geometry:
                self.window.geometry(self.normal_geometry)
            self.is_maximized = False
            # Update maximize button text
            if hasattr(self, 'maximize_btn'):
                self.maximize_btn.config(text="🗖")
    
    def toggle_maximize(self):
        """Toggle between maximized and normal state"""
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_registration_interface(self):
        """Create registration form"""
        # Main container with padding
        main_container = tk.Frame(self.window, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Modern header with window controls
        header_frame = tk.Frame(main_container, bg=self.colors['card'], height=60, relief='flat')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Header content frame
        header_content = tk.Frame(header_frame, bg=self.colors['card'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Left side - Registration icon and title
        left_frame = tk.Frame(header_content, bg=self.colors['card'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Registration icon and title
        title_frame = tk.Frame(left_frame, bg=self.colors['card'])
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(title_frame, text="📝", font=('Segoe UI', 20), 
                bg=self.colors['card'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 10))
        
        info_frame = tk.Frame(title_frame, bg=self.colors['card'])
        info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(info_frame, text="User Registration", 
                font=('Segoe UI', 14, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text_dark']).pack(anchor=tk.W)
        
        tk.Label(info_frame, text="Create new account", 
                font=('Segoe UI', 9), bg=self.colors['card'], 
                fg=self.colors['text_light']).pack(anchor=tk.W)
        
        # Right side - Window controls
        right_frame = tk.Frame(header_content, bg=self.colors['card'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Window control buttons
        controls_frame = tk.Frame(right_frame, bg=self.colors['card'])
        controls_frame.pack(side=tk.RIGHT)
        
        # Minimize button
        minimize_btn = tk.Button(controls_frame, text="🗕", font=('Segoe UI', 10), 
                                bg=self.colors['card'], fg=self.colors['text_dark'],
                                bd=0, padx=8, pady=3, cursor='hand2',
                                command=self.minimize_window)
        minimize_btn.pack(side=tk.LEFT, padx=1)
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(controls_frame, text="🗖", font=('Segoe UI', 10), 
                                     bg=self.colors['card'], fg=self.colors['text_dark'],
                                     bd=0, padx=8, pady=3, cursor='hand2',
                                     command=self.toggle_maximize)
        self.maximize_btn.pack(side=tk.LEFT, padx=1)
        
        # Close button
        close_btn = tk.Button(controls_frame, text="🗙", font=('Segoe UI', 10), 
                             bg=self.colors['card'], fg=self.colors['accent'],
                             bd=0, padx=8, pady=3, cursor='hand2',
                             command=self.window.destroy)
        close_btn.pack(side=tk.LEFT, padx=1)
        
        # Content area with scrollbar
        content_frame = tk.Frame(main_container, bg=self.colors['card'], relief='flat')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main frame with scrollbar
        canvas = tk.Canvas(content_frame, bg=self.colors['background'])
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure canvas to center content horizontally
        def center_content():
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            scroll_width = scrollable_frame.winfo_reqwidth()
            if canvas_width > scroll_width:
                x_pos = (canvas_width - scroll_width) // 2
                canvas.create_window((x_pos, 0), window=scrollable_frame, anchor="n")
        
        canvas.bind("<Configure>", lambda e: center_content())
        
        # Add mouse wheel scrolling support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Center wrapper to center the form content
        center_wrapper = tk.Frame(scrollable_frame, bg=self.colors['background'])
        center_wrapper.pack(fill=tk.BOTH, expand=True)
        
        # Main form frame - centered with fixed width
        main_frame = ttk.Frame(center_wrapper, padding="20")
        main_frame.pack(anchor='center', padx=50, pady=20)
        
        # Title
        ttk.Label(main_frame, text="User Registration", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Basic info section
        basic_frame = ttk.LabelFrame(main_frame, text="Basic Information", padding="15")
        basic_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create variables for form fields
        self.form_vars = {}
        
        # Basic fields with improved labeling
        basic_fields = [
            ("Full Name *", "full_name", False, "Enter your full name (e.g., John Smith)"),
            ("Username *", "username", False, "Choose a username"),
            ("Password *", "password", True, ""),
            ("Confirm Password *", "confirm_password", True, ""),
            ("Email *", "email", False, "Enter your email address"),
            ("Phone", "phone", False, "Enter your phone number")
        ]
        
        for label, var_name, is_password, placeholder in basic_fields:
            # Create label with required field indicator
            label_frame = ttk.Frame(basic_frame)
            label_frame.pack(fill=tk.X, anchor=tk.W)
            
            ttk.Label(label_frame, text=f"{label}:", font=("Arial", 10, "bold" if "*" in label else "normal")).pack(anchor=tk.W)
            
            # Create StringVar and Entry widget
            self.form_vars[var_name] = tk.StringVar()
            entry = ttk.Entry(basic_frame, textvariable=self.form_vars[var_name], width=40, font=("Arial", 10))
            if is_password:
                entry.config(show="*")
            entry.pack(fill=tk.X, pady=(2, 10))
            
            # Store entry widget reference for debugging
            setattr(self, f"{var_name}_entry", entry)
            
            # Add placeholder as a hint label for non-password fields
            if placeholder and not is_password:
                hint_label = ttk.Label(basic_frame, text=placeholder, font=("Arial", 8), foreground="gray")
                hint_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Role selection
        ttk.Label(basic_frame, text="Role:").pack(anchor=tk.W)
        self.role_var = tk.StringVar(value="patient")
        role_frame = ttk.Frame(basic_frame)
        role_frame.pack(fill=tk.X, pady=(5, 10))
        
        roles = [("Patient", "patient"), ("Doctor", "doctor"), ("Nurse", "nurse")]
        for text, value in roles:
            ttk.Radiobutton(role_frame, text=text, variable=self.role_var, 
                           value=value, command=self.on_role_change).pack(side=tk.LEFT, padx=(0, 20))
        
        # Role-specific section
        self.role_frame = ttk.LabelFrame(main_frame, text="Role-Specific Information", padding="15")
        self.role_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Initialize with patient fields
        self.on_role_change()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Register", 
                  command=self.register_user).pack(side=tk.RIGHT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_role_change(self):
        """Handle role selection change"""
        # Clear existing role-specific fields
        for widget in self.role_frame.winfo_children():
            widget.destroy()
        
        role = self.role_var.get()
        
        if role == "patient":
            self.create_patient_fields()
        elif role == "doctor":
            self.create_doctor_fields()
        elif role == "nurse":
            self.create_nurse_fields()
    
    def create_patient_fields(self):
        """Create patient-specific fields"""
        fields = [
            ("Date of Birth (YYYY-MM-DD)", "date_of_birth"),
            ("Gender", "gender"),
            ("Address", "address"),
            ("Emergency Contact", "emergency_contact"),
            ("Emergency Phone", "emergency_phone"),
            ("Blood Group", "blood_group"),
            ("Medical History", "medical_history"),
            ("Allergies", "allergies")
        ]
        
        for label, var_name in fields:
            ttk.Label(self.role_frame, text=f"{label}:").pack(anchor=tk.W)
            
            if var_name == "gender":
                self.form_vars[var_name] = tk.StringVar(value="Male")
                gender_frame = ttk.Frame(self.role_frame)
                gender_frame.pack(fill=tk.X, pady=(5, 10))
                for gender in ["Male", "Female", "Other"]:
                    ttk.Radiobutton(gender_frame, text=gender, variable=self.form_vars[var_name], 
                                   value=gender).pack(side=tk.LEFT, padx=(0, 20))
            elif var_name in ["medical_history", "allergies", "address"]:
                self.form_vars[var_name] = tk.StringVar()
                text_widget = tk.Text(self.role_frame, height=3, width=40)
                text_widget.pack(fill=tk.X, pady=(5, 10))
                # Store text widget reference for later retrieval
                setattr(self, f"{var_name}_text", text_widget)
            else:
                self.form_vars[var_name] = tk.StringVar()
                ttk.Entry(self.role_frame, textvariable=self.form_vars[var_name], 
                         width=40).pack(fill=tk.X, pady=(5, 10))
    
    def create_doctor_fields(self):
        """Create doctor-specific fields"""
        fields = [
            ("Specialization", "specialization"),
            ("License Number", "license_number"),
            ("Department", "department"),
            ("Qualification", "qualification"),
            ("Experience (Years)", "experience_years"),
            ("Consultation Fee", "consultation_fee")
        ]
        
        for label, var_name in fields:
            ttk.Label(self.role_frame, text=f"{label}:").pack(anchor=tk.W)
            
            if var_name == "qualification":
                self.form_vars[var_name] = tk.StringVar()
                text_widget = tk.Text(self.role_frame, height=3, width=40)
                text_widget.pack(fill=tk.X, pady=(5, 10))
                setattr(self, f"{var_name}_text", text_widget)
            else:
                self.form_vars[var_name] = tk.StringVar()
                ttk.Entry(self.role_frame, textvariable=self.form_vars[var_name], 
                         width=40).pack(fill=tk.X, pady=(5, 10))
    
    def create_nurse_fields(self):
        """Create nurse-specific fields"""
        fields = [
            ("Department", "department"),
            ("License Number", "license_number"),
            ("Qualification", "qualification")
        ]
        
        for label, var_name in fields:
            ttk.Label(self.role_frame, text=f"{label}:").pack(anchor=tk.W)
            
            if var_name == "qualification":
                self.form_vars[var_name] = tk.StringVar()
                text_widget = tk.Text(self.role_frame, height=3, width=40)
                text_widget.pack(fill=tk.X, pady=(5, 10))
                setattr(self, f"{var_name}_text", text_widget)
            else:
                self.form_vars[var_name] = tk.StringVar()
                ttk.Entry(self.role_frame, textvariable=self.form_vars[var_name], 
                         width=40).pack(fill=tk.X, pady=(5, 10))
        
        # Shift type for nurse
        ttk.Label(self.role_frame, text="Shift Type:").pack(anchor=tk.W)
        self.form_vars["shift_type"] = tk.StringVar(value="Day")
        shift_frame = ttk.Frame(self.role_frame)
        shift_frame.pack(fill=tk.X, pady=(5, 10))
        for shift in ["Day", "Night", "Rotating"]:
            ttk.Radiobutton(shift_frame, text=shift, variable=self.form_vars["shift_type"], 
                           value=shift).pack(side=tk.LEFT, padx=(0, 20))
    
    def get_text_values(self):
        """Extract values from text widgets"""
        text_fields = ['medical_history', 'allergies', 'address', 'qualification']
        for field in text_fields:
            text_widget = getattr(self, f"{field}_text", None)
            if text_widget:
                self.form_vars[field] = tk.StringVar(value=text_widget.get("1.0", tk.END).strip())
    
    def register_user(self):
        """Register new user"""
        # Get text values
        self.get_text_values()
        
        # Debug: Print form values from StringVars
        print("Form values from StringVars:")
        for key, var in self.form_vars.items():
            print(f"  {key}: '{var.get()}'")
        
        # Debug: Try to get values directly from Entry widgets as backup
        print("Form values from Entry widgets:")
        basic_field_names = ['full_name', 'username', 'password', 'confirm_password', 'email', 'phone']
        for field in basic_field_names:
            entry_widget = getattr(self, f"{field}_entry", None)
            if entry_widget:
                direct_value = entry_widget.get()
                print(f"  {field}: '{direct_value}'")
                # If StringVar is empty but Entry has value, update StringVar
                if not self.form_vars[field].get().strip() and direct_value.strip():
                    self.form_vars[field].set(direct_value)
                    print(f"  Updated {field} StringVar with Entry value")
        
        # Validate basic fields
        required_fields = ['full_name', 'username', 'password', 'confirm_password', 'email']
        for field in required_fields:
            value = self.form_vars.get(field, tk.StringVar()).get().strip()
            if not value:
                field_name = field.replace('_', ' ').title()
                messagebox.showerror("Error", f"Please fill in {field_name}")
                return
        
        # Validate password match
        if self.form_vars['password'].get() != self.form_vars['confirm_password'].get():
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Prepare user data
        user_data = {
            'username': self.form_vars['username'].get().strip(),
            'password': self.form_vars['password'].get(),
            'email': self.form_vars['email'].get().strip(),
            'full_name': self.form_vars['full_name'].get().strip(),
            'phone': self.form_vars['phone'].get().strip(),
            'role': self.role_var.get()
        }
        
        # Prepare role-specific data
        role_specific_data = {}
        role = self.role_var.get()
        
        if role == 'patient':
            role_specific_data = {
                'date_of_birth': self.form_vars.get('date_of_birth', tk.StringVar()).get() or None,
                'gender': self.form_vars.get('gender', tk.StringVar()).get() or None,
                'address': self.form_vars.get('address', tk.StringVar()).get() or None,
                'emergency_contact': self.form_vars.get('emergency_contact', tk.StringVar()).get() or None,
                'emergency_phone': self.form_vars.get('emergency_phone', tk.StringVar()).get() or None,
                'blood_group': self.form_vars.get('blood_group', tk.StringVar()).get() or None,
                'medical_history': self.form_vars.get('medical_history', tk.StringVar()).get() or None,
                'allergies': self.form_vars.get('allergies', tk.StringVar()).get() or None
            }
        elif role == 'doctor':
            role_specific_data = {
                'specialization': self.form_vars.get('specialization', tk.StringVar()).get() or None,
                'license_number': self.form_vars.get('license_number', tk.StringVar()).get() or None,
                'department': self.form_vars.get('department', tk.StringVar()).get() or None,
                'qualification': self.form_vars.get('qualification', tk.StringVar()).get() or None,
                'experience_years': int(self.form_vars.get('experience_years', tk.StringVar()).get() or 0),
                'consultation_fee': float(self.form_vars.get('consultation_fee', tk.StringVar()).get() or 0)
            }
        elif role == 'nurse':
            role_specific_data = {
                'department': self.form_vars.get('department', tk.StringVar()).get() or None,
                'shift_type': self.form_vars.get('shift_type', tk.StringVar()).get() or None,
                'qualification': self.form_vars.get('qualification', tk.StringVar()).get() or None,
                'license_number': self.form_vars.get('license_number', tk.StringVar()).get() or None
            }
        
        # Create user
        try:
            if UserManager.create_user(user_data, role_specific_data):
                messagebox.showinfo("Success", "User registered successfully!")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to register user. Username or email may already exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

if __name__ == "__main__":
    app = LoginWindow()
    app.run()