"""
Test Registration Window
Quick test for the new registration window with window management
"""

import tkinter as tk
from auth import RegistrationWindow

def test_registration_window():
    """Test the registration window directly"""
    root = tk.Tk()
    root.title("Test Parent Window")
    root.geometry("300x200")
    
    # Create test button to open registration
    def open_registration():
        RegistrationWindow(root)
    
    btn = tk.Button(root, text="Open Registration", command=open_registration,
                   font=('Arial', 12), pady=10)
    btn.pack(expand=True)
    
    # Also create the registration window immediately
    RegistrationWindow(root)
    
    root.mainloop()

if __name__ == "__main__":
    print("Testing Registration Window with Window Management...")
    test_registration_window()