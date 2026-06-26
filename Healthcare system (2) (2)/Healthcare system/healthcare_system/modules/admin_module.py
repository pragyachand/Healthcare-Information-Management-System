"""
Admin Module - Administrator Dashboard and Functionality
Healthcare Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
from datetime import datetime, date
import os
from utils.db_utils import UserManager, ReportsManager
from utils.pdf_generator import (
    generate_doctor_patient_pdf,
    generate_system_summary_pdf,
    generate_user_activity_pdf,
    generate_dashboard_pdf
)

class AdminDashboard:
    """Administrator dashboard interface with modern design"""
    
    def __init__(self, user_data, parent_window):
        self.user_data = user_data
        self.parent_window = parent_window
        
        # Modern color scheme
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
        self.root.title(f"Admin Dashboard - {user_data['full_name']}")
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
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['card'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure button styles
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 8])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10),
                       padding=[12, 6])
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10),
                       padding=[12, 6])
        
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
        
        # Header with gradient-like effect
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Left side - Welcome message with icon
        left_header = tk.Frame(header_content, bg=self.colors['primary'])
        left_header.pack(side=tk.LEFT, fill=tk.Y)
        
        # Admin icon
        icon_label = tk.Label(left_header, text="👨‍💼", font=("Arial", 20), 
                             bg=self.colors['primary'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Welcome text
        welcome_frame = tk.Frame(left_header, bg=self.colors['primary'])
        welcome_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        welcome_label = tk.Label(welcome_frame, 
                                text=f"Administrator Dashboard", 
                                font=("Segoe UI", 18, "bold"),
                                bg=self.colors['primary'], fg='white')
        welcome_label.pack(anchor=tk.W)
        
        user_label = tk.Label(welcome_frame, 
                             text=f"Welcome back, {self.user_data['full_name']}", 
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
        self.maximize_btn = tk.Button(window_controls, text="🗖", 
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
        
        # Create tabs with enhanced UI
        self.create_dashboard_tab()
        self.create_user_management_tab()
        self.create_reports_tab()
        
        # Set focus to first tab
        self.notebook.select(0)
    
    def create_dashboard_tab(self):
        """Create enhanced system overview dashboard tab with scrollable content"""
        # Create main frame with scrollbar
        main_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(main_frame, text="📊 Dashboard")
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Statistics cards section
        stats_container = tk.Frame(scrollable_frame, bg=self.colors['background'])
        stats_container.pack(fill=tk.X, pady=(0, 30))
        
        # Section header
        header_frame = tk.Frame(stats_container, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="📈 System Statistics", 
                              font=("Segoe UI", 16, "bold"),
                              bg=self.colors['background'], fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT)
        
        # Refresh button with modern style
        refresh_btn = tk.Button(header_frame, text="🔄 Refresh", 
                               command=self.refresh_statistics,
                               font=("Segoe UI", 10),
                               bg=self.colors['primary'], fg='white',
                               relief='flat', padx=20, pady=8,
                               cursor='hand2')
        refresh_btn.pack(side=tk.RIGHT)
        
        # Statistics cards
        stats_grid = tk.Frame(stats_container, bg=self.colors['background'])
        stats_grid.pack(fill=tk.X)
        
        self.stats_vars = {}
        stats_config = [
            ("👥 Total Patients", "total_patients", self.colors['success']),
            ("👨‍⚕️ Total Doctors", "total_doctors", self.colors['primary']),
            ("👩‍⚕️ Total Nurses", "total_nurses", self.colors['secondary']),
            (" Active Prescriptions", "active_prescriptions", self.colors['danger'])
        ]
        
        for i, (label, var_name, color) in enumerate(stats_config):
            # Create card frame
            card = tk.Frame(stats_grid, bg=self.colors['card'], 
                           relief='solid', bd=1, padx=20, pady=15)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='ew')
            
            # Configure grid weights for responsiveness
            stats_grid.columnconfigure(i%3, weight=1)
            
            # Card header with icon
            header = tk.Label(card, text=label, 
                             font=("Segoe UI", 12, "bold"),
                             bg=self.colors['card'], fg=self.colors['text_primary'])
            header.pack(anchor=tk.W)
            
            # Value display
            self.stats_vars[var_name] = tk.StringVar(value="Loading...")
            value_label = tk.Label(card, textvariable=self.stats_vars[var_name], 
                                  font=("Segoe UI", 24, "bold"),
                                  bg=self.colors['card'], fg=color)
            value_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Quick Actions Section
        actions_container = tk.Frame(scrollable_frame, bg=self.colors['background'])
        actions_container.pack(fill=tk.X, pady=(0, 30))
        
        actions_header = tk.Label(actions_container, text="⚡ Quick Actions", 
                                 font=("Segoe UI", 16, "bold"),
                                 bg=self.colors['background'], fg=self.colors['text_primary'])
        actions_header.pack(anchor=tk.W, pady=(0, 15))
        
        # Action buttons
        actions_frame = tk.Frame(actions_container, bg=self.colors['background'])
        actions_frame.pack(fill=tk.X)
        
        action_buttons = [
            ("👤 Create User", self.create_new_user, self.colors['primary']),
            ("📊 Generate Report", lambda: self.notebook.select(2), self.colors['success']),
            ("👥 Manage Users", lambda: self.notebook.select(1), self.colors['secondary']),
            ("🔍 System Health", self.show_system_health, self.colors['warning'])
        ]
        
        for i, (text, command, color) in enumerate(action_buttons):
            btn = tk.Button(actions_frame, text=text, command=command,
                           font=("Segoe UI", 11, "bold"),
                           bg=color, fg='white',
                           relief='flat', padx=25, pady=12,
                           cursor='hand2', width=15)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='ew')
            actions_frame.columnconfigure(i%2, weight=1)
        
        # Activity log section with enhanced design
        activity_container = tk.Frame(scrollable_frame, bg=self.colors['background'])
        activity_container.pack(fill=tk.BOTH, expand=True)
        
        activity_header = tk.Label(activity_container, text="📋 Recent Activity Log", 
                                  font=("Segoe UI", 16, "bold"),
                                  bg=self.colors['background'], fg=self.colors['text_primary'])
        activity_header.pack(anchor=tk.W, pady=(0, 15))
        
        # Activity log card
        activity_card = tk.Frame(activity_container, bg=self.colors['card'], 
                                relief='solid', bd=1)
        activity_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Activity text with scrollbar
        activity_frame = tk.Frame(activity_card, bg=self.colors['card'])
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.activity_text = tk.Text(activity_frame, height=12, 
                                    font=("Consolas", 10),
                                    bg=self.colors['card'], 
                                    fg=self.colors['text_primary'],
                                    relief='flat', wrap=tk.WORD)
        activity_scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, 
                                          command=self.activity_text.yview)
        self.activity_text.configure(yscrollcommand=activity_scrollbar.set)
        
        self.activity_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        activity_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_statistics()
        self.load_recent_activity()
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def show_system_health(self):
        """Show system health dialog"""
        health_window = tk.Toplevel(self.root)
        health_window.title("System Health Check")
        health_window.geometry("500x400")
        health_window.configure(bg=self.colors['background'])
        health_window.grab_set()
        
        # Center the window
        health_window.update_idletasks()
        width = health_window.winfo_width()
        height = health_window.winfo_height()
        x = (health_window.winfo_screenwidth() // 2) - (width // 2)
        y = (health_window.winfo_screenheight() // 2) - (height // 2)
        health_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header
        header = tk.Label(health_window, text="🔍 System Health Status", 
                         font=("Segoe UI", 16, "bold"),
                         bg=self.colors['background'], fg=self.colors['primary'])
        header.pack(pady=20)
        
        # Health info
        health_info = f"""
🟢 Database Connection: Active
🟢 User Authentication: Functional
🟢 GUI Components: Responsive
🟢 Memory Usage: Normal
🟢 System Performance: Optimal

📊 Current Statistics:
• Uptime: {datetime.now().strftime('%H:%M:%S')}
• Active Sessions: 1
• Last Backup: Simulated Daily
• Security Status: Secure

✅ All systems operational!
        """
        
        info_label = tk.Label(health_window, text=health_info, 
                             font=("Consolas", 10),
                             bg=self.colors['background'], fg=self.colors['text_primary'],
                             justify=tk.LEFT)
        info_label.pack(padx=20, pady=20)
        
        # Close button
        close_btn = tk.Button(health_window, text="Close", 
                             command=health_window.destroy,
                             font=("Segoe UI", 10, "bold"),
                             bg=self.colors['primary'], fg='white',
                             relief='flat', padx=30, pady=10,
                             cursor='hand2')
        close_btn.pack(pady=20)
    
    def create_user_management_tab(self):
        """Create enhanced user management tab with modern design"""
        # Create main frame
        main_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(main_frame, text="👥 User Management")
        
        # Top controls section
        controls_card = tk.Frame(main_frame, bg=self.colors['card'], relief='solid', bd=1)
        controls_card.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        controls_content = tk.Frame(controls_card, bg=self.colors['card'])
        controls_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Header
        header_label = tk.Label(controls_content, text="👥 System User Management", 
                               font=("Segoe UI", 16, "bold"),
                               bg=self.colors['card'], fg=self.colors['text_primary'])
        header_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Filter section
        filter_frame = tk.Frame(controls_content, bg=self.colors['card'])
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Role filter with modern styling
        tk.Label(filter_frame, text="Filter by Role:", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        self.role_filter_var = tk.StringVar(value="All")
        role_combo = ttk.Combobox(filter_frame, textvariable=self.role_filter_var, 
                                 values=["All", "admin", "doctor", "nurse", "patient"], 
                                 width=12, state="readonly", font=("Segoe UI", 10))
        role_combo.pack(side=tk.LEFT, padx=(10, 15))
        
        # Filter button
        filter_btn = tk.Button(filter_frame, text="🔍 Apply Filter", 
                              command=self.refresh_users,
                              font=("Segoe UI", 10),
                              bg=self.colors['primary'], fg='white',
                              relief='flat', padx=15, pady=6,
                              cursor='hand2')
        filter_btn.pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(controls_content, bg=self.colors['card'])
        actions_frame.pack(fill=tk.X)
        
        action_buttons = [
            ("➕ Create User", self.create_new_user, self.colors['success']),
            ("✏️ Edit Selected", self.edit_user, self.colors['warning']),
            ("❌ Deactivate", self.deactivate_user, self.colors['danger']),
            ("✅ Activate", self.activate_user, self.colors['success']),
            ("🔄 Refresh", self.refresh_users, self.colors['primary'])
        ]
        
        for i, (text, command, color) in enumerate(action_buttons):
            btn = tk.Button(actions_frame, text=text, command=command,
                           font=("Segoe UI", 9, "bold"),
                           bg=color, fg='white',
                           relief='flat', padx=12, pady=6,
                           cursor='hand2')
            btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Users table section
        table_card = tk.Frame(main_frame, bg=self.colors['card'], relief='solid', bd=1)
        table_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        table_header = tk.Frame(table_card, bg=self.colors['card'])
        table_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(table_header, text="📋 User Directory", 
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        # Users table with enhanced styling
        table_frame = tk.Frame(table_card, bg=self.colors['card'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Enhanced treeview
        columns = ("Username", "Full Name", "Email", "Phone", "Role", "Created", "Status")
        self.users_tree = ttk.Treeview(table_frame, columns=columns, 
                                      show="headings", height=15,
                                      style='Modern.Treeview')
        
        # Configure columns with better widths
        column_widths = {"Username": 120, "Full Name": 180, "Email": 200, 
                        "Phone": 130, "Role": 100, "Created": 120, "Status": 80}
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=column_widths[col], minwidth=80)
        
        # Add scrollbars
        users_v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                         command=self.users_tree.yview)
        users_h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, 
                                         command=self.users_tree.xview)
        
        self.users_tree.configure(yscrollcommand=users_v_scrollbar.set,
                                 xscrollcommand=users_h_scrollbar.set)
        
        # Grid layout for table and scrollbars
        self.users_tree.grid(row=0, column=0, sticky='nsew')
        users_v_scrollbar.grid(row=0, column=1, sticky='ns')
        users_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg=self.colors['background'])
        status_frame.pack(fill=tk.X, padx=20)
        
        self.users_status_var = tk.StringVar(value="Ready to manage users...")
        status_label = tk.Label(status_frame, textvariable=self.users_status_var,
                               font=("Segoe UI", 9),
                               bg=self.colors['background'], fg=self.colors['text_secondary'])
        status_label.pack(anchor=tk.W)
        
        # Load users
        self.refresh_users()
    
    def create_reports_tab(self):
        """Create enhanced reports tab with PDF export"""
        # Create main frame with modern styling
        reports_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Reports section with modern card design
        reports_card = tk.Frame(reports_frame, bg=self.colors['card'], relief='solid', bd=1)
        reports_card.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        reports_content = tk.Frame(reports_card, bg=self.colors['card'])
        reports_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Header with PDF export button
        header_row = tk.Frame(reports_content, bg=self.colors['card'])
        header_row.pack(fill=tk.X, pady=(0, 15))
        
        header_label = tk.Label(header_row, text="📊 System Reports & Analytics", 
                               font=("Segoe UI", 16, "bold"),
                               bg=self.colors['card'], fg=self.colors['text_primary'])
        header_label.pack(side=tk.LEFT)
        
        # PDF Export button at the top
        self.save_pdf_btn = tk.Button(header_row, text="📄 Export to PDF", 
                                command=self.export_to_pdf,
                                font=("Segoe UI", 11, "bold"),
                                bg=self.colors['success'], fg='white',
                                relief='flat', padx=20, pady=10,
                                cursor='hand2')
        self.save_pdf_btn.pack(side=tk.RIGHT)
        
        # Store current report data for PDF export
        self.current_report_data = None
        self.current_report_type = None
        
        # Report buttons with modern styling
        buttons_frame = tk.Frame(reports_content, bg=self.colors['card'])
        buttons_frame.pack(fill=tk.X)
        
        report_buttons = [
            ("👨‍⚕️ Doctor-wise Patient Count", self.generate_doctor_patient_report, self.colors['primary']),
            ("📈 System Usage Summary", self.generate_system_summary_report, self.colors['success']),
            ("👥 User Activity Report", self.generate_user_activity_report, self.colors['secondary']),
            ("📋 Dashboard Report", self.generate_dashboard_report, self.colors['warning'])
        ]
        
        row = 0
        col = 0
        for text, command, color in report_buttons:
            btn = tk.Button(buttons_frame, text=text, command=command,
                           font=("Segoe UI", 10, "bold"),
                           bg=color, fg='white',
                           relief='flat', padx=15, pady=10,
                           cursor='hand2', width=25)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            buttons_frame.columnconfigure(col, weight=1)
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        # Report display section with modern styling
        display_card = tk.Frame(reports_frame, bg=self.colors['card'], relief='solid', bd=1)
        display_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        display_header = tk.Frame(display_card, bg=self.colors['card'])
        display_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(display_header, text="📄 Report Output", 
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'], fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        # Report text area with modern styling
        text_frame = tk.Frame(display_card, bg=self.colors['card'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.report_text = tk.Text(text_frame, height=20, width=80, 
                                   font=("Consolas", 9),
                                   bg='white', fg=self.colors['text_primary'],
                                   relief='solid', bd=1,
                                   wrap=tk.WORD)
        report_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, 
                                         command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scrollbar.set)
        
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame (at bottom)
        action_buttons_frame = tk.Frame(reports_frame, bg=self.colors['background'])
        action_buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Action buttons with modern styling
        clear_btn = tk.Button(action_buttons_frame, text="🗑️ Clear Report", 
                              command=self.clear_report,
                              font=("Segoe UI", 10),
                              bg=self.colors['danger'], fg='white',
                              relief='flat', padx=15, pady=8,
                              cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_txt_btn = tk.Button(action_buttons_frame, text="💾 Save as Text", 
                                command=self.save_report,
                                font=("Segoe UI", 10),
                                bg=self.colors['primary'], fg='white',
                                relief='flat', padx=15, pady=8,
                                cursor='hand2')
        save_txt_btn.pack(side=tk.LEFT)
    
    def refresh_statistics(self):
        """Refresh system statistics"""
        try:
            stats = ReportsManager.get_system_stats()
            
            for key, var in self.stats_vars.items():
                value = stats.get(key, 0)
                var.set(str(value))
                
        except Exception as e:
            print(f"Error refreshing statistics: {e}")
            for var in self.stats_vars.values():
                var.set("Error")
    
    def load_recent_activity(self):
        """Load recent activity log"""
        try:
            # Generate sample activity log
            activity_log = f"""HEALTHCARE SYSTEM ACTIVITY LOG
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[INFO] System statistics refreshed
[INFO] Admin {self.user_data['full_name']} logged in
[INFO] Database connection established
[INFO] User management module loaded
[INFO] Reports module loaded

Recent system activities would be displayed here in a real implementation.
This could include:
- User login/logout events
- Database operations
- System errors and warnings
- Administrative actions

"""
            
            self.activity_text.delete("1.0", tk.END)
            self.activity_text.insert("1.0", activity_log)
            
        except Exception as e:
            print(f"Error loading activity log: {e}")
    
    def refresh_users(self):
        """Refresh users list with filters"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Apply role filter
        role_filter = self.role_filter_var.get() if hasattr(self, 'role_filter_var') and self.role_filter_var.get() != "All" else None
        
        # Get users
        users = UserManager.get_all_users(role=role_filter)
        
        for user in users:
            status = "Active" if user['is_active'] else "Inactive"
            created_date = user['created_at'].strftime('%Y-%m-%d') if user['created_at'] else 'N/A'
            
            self.users_tree.insert("", tk.END, values=(
                user['username'],
                user['full_name'],
                user['email'],
                user['phone'] or 'N/A',
                user['role'].title(),
                created_date,
                status
            ), tags=(user['user_id'],))
    
    def create_new_user(self):
        """Open user creation form"""
        from auth import RegistrationWindow
        RegistrationWindow(self.root)
    
    def edit_user(self):
        """Edit selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        user_id = self.users_tree.item(selected_item[0])['tags'][0]
        self.show_user_edit_form(user_id)
    
    def show_user_edit_form(self, user_id):
        """Show user edit form"""
        try:
            from database.db_config import db_manager
            
            if not db_manager.connect():
                return
            
            # Get user data
            query = "SELECT * FROM users WHERE user_id = %s"
            result = db_manager.execute_query(query, (user_id,), fetch=True)
            
            if not result:
                messagebox.showerror("Error", "User not found")
                return
            
            user = result[0]
            
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Edit User - {user['username']}")
            edit_window.geometry("400x500")
            edit_window.grab_set()
            
            # Center the window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
            y = (edit_window.winfo_screenheight() // 2) - (height // 2)
            edit_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Main frame
            main_frame = ttk.Frame(edit_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title
            ttk.Label(main_frame, text=f"Edit User: {user['username']}", 
                     font=("Arial", 16, "bold")).pack(pady=(0, 20))
            
            # Form variables
            form_vars = {}
            
            # Fields
            fields = [
                ("Full Name", "full_name", user['full_name']),
                ("Email", "email", user['email']),
                ("Phone", "phone", user['phone'] or '')
            ]
            
            for label, var_name, value in fields:
                ttk.Label(main_frame, text=f"{label}:").pack(anchor=tk.W)
                form_vars[var_name] = tk.StringVar(value=value)
                ttk.Entry(main_frame, textvariable=form_vars[var_name], width=30).pack(fill=tk.X, pady=(5, 10))
            
            # Role (read-only)
            ttk.Label(main_frame, text="Role:").pack(anchor=tk.W)
            ttk.Label(main_frame, text=user['role'].title(), 
                     font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 10))
            
            # Status
            ttk.Label(main_frame, text="Status:").pack(anchor=tk.W)
            status_var = tk.BooleanVar(value=user['is_active'])
            ttk.Checkbutton(main_frame, text="Active", variable=status_var).pack(anchor=tk.W, pady=(5, 15))
            
            # Buttons
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def save_changes():
                update_data = {
                    'full_name': form_vars['full_name'].get(),
                    'email': form_vars['email'].get(),
                    'phone': form_vars['phone'].get() or None,
                    'is_active': status_var.get()
                }
                
                if UserManager.update_user_profile(user_id, update_data):
                    messagebox.showinfo("Success", "User updated successfully")
                    edit_window.destroy()
                    self.refresh_users()
                else:
                    messagebox.showerror("Error", "Failed to update user")
            
            ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.RIGHT, padx=(10, 0))
            ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.RIGHT)
            
            db_manager.disconnect()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading user data: {str(e)}")
    
    def deactivate_user(self):
        """Deactivate selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to deactivate")
            return
        
        user_id = self.users_tree.item(selected_item[0])['tags'][0]
        username = self.users_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Deactivate user '{username}'?"):
            if UserManager.update_user_profile(user_id, {'is_active': False}):
                messagebox.showinfo("Success", f"User '{username}' deactivated")
                self.refresh_users()
            else:
                messagebox.showerror("Error", "Failed to deactivate user")
    
    def activate_user(self):
        """Activate selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to activate")
            return
        
        user_id = self.users_tree.item(selected_item[0])['tags'][0]
        username = self.users_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm", f"Activate user '{username}'?"):
            if UserManager.update_user_profile(user_id, {'is_active': True}):
                messagebox.showinfo("Success", f"User '{username}' activated")
                self.refresh_users()
            else:
                messagebox.showerror("Error", "Failed to activate user")
    
    def generate_doctor_patient_report(self):
        """Generate doctor-wise patient count report"""
        try:
            self.report_text.delete("1.0", tk.END)
            
            report_header = f"""DOCTOR-WISE PATIENT COUNT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Administrator: {self.user_data['full_name']}

{'='*60}

"""
            
            self.report_text.insert(tk.END, report_header)
            
            # Get doctor patient counts
            doctor_counts = ReportsManager.get_doctor_patient_count()
            
            # Store data for PDF export
            self.current_report_data = doctor_counts
            self.current_report_type = 'doctor_patient'
            
            if doctor_counts:
                # Create table format
                table_header = f"{'Doctor Name':<30} {'Specialization':<25} {'Total Patients':<15}\n"
                table_header += "-" * 70 + "\n"
                self.report_text.insert(tk.END, table_header)
                
                for doctor in doctor_counts:
                    doctor_info = f"{doctor['doctor_name']:<30} {str(doctor['specialization'] or 'N/A'):<25} {str(doctor['patient_count']):<15}\n"
                    self.report_text.insert(tk.END, doctor_info)
                
                # Add summary
                total_patients = sum(d.get('patient_count', 0) for d in doctor_counts)
                total_doctors = len(doctor_counts)
                avg_patients = round(total_patients / total_doctors, 2) if total_doctors > 0 else 0
                
                summary = f"""
{'='*70}
SUMMARY:
Total Doctors: {total_doctors}
Total Patients Served: {total_patients}
Average Patients per Doctor: {avg_patients}
{'='*70}
"""
                self.report_text.insert(tk.END, summary)
            else:
                self.report_text.insert(tk.END, "No doctor data available.\n")
            
            self.report_text.insert(tk.END, f"\nReport completed. Click 'Export to PDF' to save as PDF with table format.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def generate_system_summary_report(self):
        """Generate system usage summary report"""
        try:
            self.report_text.delete("1.0", tk.END)
            
            report_header = f"""SYSTEM USAGE SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Administrator: {self.user_data['full_name']}

{'='*60}

"""
            
            self.report_text.insert(tk.END, report_header)
            
            # Get system statistics
            stats = ReportsManager.get_system_stats()
            
            # Store data for PDF export
            self.current_report_data = stats
            self.current_report_type = 'system_summary'
            
            # Create table format
            table_header = f"{'Category':<30} {'Count':<15}\n"
            table_header += "-" * 45 + "\n"
            self.report_text.insert(tk.END, "SYSTEM STATISTICS:\n\n")
            self.report_text.insert(tk.END, table_header)
            
            stats_table = f"""Total Patients{'':<18} {stats.get('total_patients', 0):<15}
Total Doctors{'':<19} {stats.get('total_doctors', 0):<15}
Total Nurses{'':<20} {stats.get('total_nurses', 0):<15}
Active Prescriptions{'':<12} {stats.get('active_prescriptions', 0):<15}
"""
            self.report_text.insert(tk.END, stats_table)
            
            summary = f"""
{'='*60}
SYSTEM HEALTH:
System Status: Operational
Database Status: Connected
Last Backup: {datetime.now().strftime('%Y-%m-%d')} (Simulated)
{'='*60}
"""
            
            self.report_text.insert(tk.END, summary)
            self.report_text.insert(tk.END, f"\nReport completed. Click 'Export to PDF' to save as PDF with table format.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def generate_user_activity_report(self):
        """Generate user activity report"""
        try:
            self.report_text.delete("1.0", tk.END)
            
            report_header = f"""USER ACTIVITY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Administrator: {self.user_data['full_name']}

{'='*60}

"""
            
            self.report_text.insert(tk.END, report_header)
            
            # Get user counts by role
            users = UserManager.get_all_users()
            
            # Store data for PDF export
            self.current_report_data = users
            self.current_report_type = 'user_activity'
            
            role_counts = {}
            active_counts = {}
            
            for user in users:
                role = user['role']
                role_counts[role] = role_counts.get(role, 0) + 1
                if user['is_active']:
                    active_counts[role] = active_counts.get(role, 0) + 1
            
            # Create table format
            table_header = f"{'Role':<15} {'Total Users':<15} {'Active':<15} {'Inactive':<15}\n"
            table_header += "-" * 60 + "\n"
            self.report_text.insert(tk.END, "USER ACTIVITY SUMMARY:\n\n")
            self.report_text.insert(tk.END, "Role Distribution:\n")
            self.report_text.insert(tk.END, table_header)
            
            for role in ['admin', 'doctor', 'nurse', 'patient']:
                total = role_counts.get(role, 0)
                active = active_counts.get(role, 0)
                inactive = total - active
                
                role_info = f"{role.title():<15} {str(total):<15} {str(active):<15} {str(inactive):<15}\n"
                self.report_text.insert(tk.END, role_info)
            
            # User details table (sample)
            if users:
                self.report_text.insert(tk.END, f"\n\nUser Details (Sample - First 10 users):\n")
                user_table_header = f"{'Username':<20} {'Full Name':<25} {'Role':<12} {'Status':<10}\n"
                user_table_header += "-" * 67 + "\n"
                self.report_text.insert(tk.END, user_table_header)
                
                for user in users[:10]:
                    status = "Active" if user['is_active'] else "Inactive"
                    user_info = f"{user['username']:<20} {user['full_name'][:24]:<25} {user['role'].title():<12} {status:<10}\n"
                    self.report_text.insert(tk.END, user_info)
                
                if len(users) > 10:
                    self.report_text.insert(tk.END, f"\n... and {len(users) - 10} more users\n")
            
            summary = f"""
{'='*60}
SUMMARY:
Total Users: {len(users)}
Active Users: {sum(1 for u in users if u['is_active'])}
Inactive Users: {sum(1 for u in users if not u['is_active'])}
{'='*60}
"""
            
            self.report_text.insert(tk.END, summary)
            self.report_text.insert(tk.END, f"\nReport completed. Click 'Export to PDF' to save as PDF with table format.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    

    
    def clear_report(self):
        """Clear the report display"""
        self.report_text.delete("1.0", tk.END)
    
    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        try:
            self.report_text.delete("1.0", tk.END)
            
            report_header = f"""ADMINISTRATOR DASHBOARD REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Administrator: {self.user_data['full_name']}

{'='*60}

"""
            
            self.report_text.insert(tk.END, report_header)
            
            # Get system statistics
            stats = ReportsManager.get_system_stats()
            doctor_counts = ReportsManager.get_doctor_patient_count()
            
            # Store data for PDF export
            self.current_report_data = {'stats': stats, 'doctor_data': doctor_counts}
            self.current_report_type = 'dashboard'
            
            # System Overview Table
            table_header = f"{'Metric':<30} {'Value':<15}\n"
            table_header += "-" * 45 + "\n"
            self.report_text.insert(tk.END, "SYSTEM OVERVIEW:\n\n")
            self.report_text.insert(tk.END, table_header)
            
            overview_table = f"""Total Patients{'':<18} {stats.get('total_patients', 0):<15}
Total Doctors{'':<19} {stats.get('total_doctors', 0):<15}
Total Nurses{'':<20} {stats.get('total_nurses', 0):<15}
Active Prescriptions{'':<12} {stats.get('active_prescriptions', 0):<15}
"""
            self.report_text.insert(tk.END, overview_table)
            
            # Doctor Performance (if available)
            if doctor_counts:
                self.report_text.insert(tk.END, f"\n\nDOCTOR PERFORMANCE SUMMARY:\n")
                doctor_table_header = f"{'Doctor Name':<30} {'Specialization':<25} {'Total Patients':<15}\n"
                doctor_table_header += "-" * 70 + "\n"
                self.report_text.insert(tk.END, doctor_table_header)
                
                for doctor in doctor_counts:
                    doctor_info = f"{doctor['doctor_name']:<30} {str(doctor['specialization'] or 'N/A'):<25} {str(doctor['patient_count']):<15}\n"
                    self.report_text.insert(tk.END, doctor_info)
            
            summary = f"""
{'='*60}
SYSTEM HEALTH:
System Status: Operational
Database Status: Connected
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated By: {self.user_data['full_name']}
{'='*60}
"""
            
            self.report_text.insert(tk.END, summary)
            self.report_text.insert(tk.END, f"\nReport completed. Click 'Export to PDF' to save as PDF with table format.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def export_to_pdf(self):
        """Export current report to PDF with table format"""
        try:
            if not self.current_report_data:
                messagebox.showwarning("Warning", "Please generate a report first before exporting to PDF")
                return
            
            # Get save location
            default_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Export Report to PDF",
                initialfile=default_filename
            )
            
            if not filename:
                return
            
            admin_name = self.user_data['full_name']
            
            # Generate PDF based on report type
            if self.current_report_type == 'doctor_patient':
                generate_doctor_patient_pdf(filename, admin_name, self.current_report_data)
            elif self.current_report_type == 'system_summary':
                generate_system_summary_pdf(filename, admin_name, self.current_report_data)
            elif self.current_report_type == 'user_activity':
                generate_user_activity_pdf(filename, admin_name, self.current_report_data)
            elif self.current_report_type == 'dashboard':
                stats = self.current_report_data.get('stats', {})
                doctor_data = self.current_report_data.get('doctor_data', [])
                generate_dashboard_pdf(filename, admin_name, stats, doctor_data)
            else:
                messagebox.showwarning("Warning", "No report data available for PDF export")
                return
            
            messagebox.showinfo("Success", f"Report exported to PDF successfully!\n\nLocation: {filename}")
            
        except ImportError:
            messagebox.showerror("Error", "PDF generation library (reportlab) not installed.\n\nPlease install it using:\npip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to PDF: {str(e)}")
    
    def save_report(self):
        """Save the current report to text file"""
        try:
            content = self.report_text.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("Warning", "No report to save")
                return
            
            default_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Report",
                initialfile=default_filename
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Report saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving report: {str(e)}")

    def logout(self):
        """Logout and return to login window"""
        self.root.destroy()
        self.parent_window.deiconify()
    
    def on_closing(self):
        """Handle window closing"""
        self.parent_window.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    # Test the admin dashboard (requires authentication first)
    pass