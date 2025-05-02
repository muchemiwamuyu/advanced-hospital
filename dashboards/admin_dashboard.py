import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("staff.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        email TEXT
    )
""")
conn.commit()

class StaffDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Staff Management Dashboard")
        self.geometry("900x600")
        self.configure(bg="#606c38")
        self.create_widgets()

    def create_widgets(self):
        # Sidebar Navigation
        sidebar = tk.Frame(self, width=200, bg="#2A9D8F", padx=20)
        sidebar.pack(side="left", fill="y")

        btn_staff = tk.Button(sidebar, text="Manage Staff", bg="#E9C46A", fg="black", command=self.show_manage_staff)
        btn_shifts = tk.Button(sidebar, text="Manage Shifts", bg="#F4A261", fg="black", command=self.show_manage_shifts)
        btn_reports = tk.Button(sidebar, text="Attendance Reports", bg="#E76F51", fg="black", command=self.show_attendance_reports)

        btn_staff.pack(pady=20, fill="x")
        btn_shifts.pack(pady=20, fill="x")
        btn_reports.pack(pady=20, fill="x")

        # Main content area
        self.content = tk.Frame(self, bg="#264653")
        self.content.pack(side="right", expand=True, fill="both")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_manage_staff(self):
        self.clear_content()

        tk.Label(self.content, text="Manage Staff", font=("Arial", 20), bg="#264653", fg="white").pack(pady=10)

        form_frame = tk.Frame(self.content, bg="#264653")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Name", bg="#264653", fg="white").grid(row=0, column=0)
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Position", bg="#264653", fg="white").grid(row=1, column=0)
        position_entry = tk.Entry(form_frame)
        position_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Email", bg="#264653", fg="white").grid(row=2, column=0)
        email_entry = tk.Entry(form_frame)
        email_entry.grid(row=2, column=1)

        def add_staff():
            name = name_entry.get()
            position = position_entry.get()
            email = email_entry.get()
            if not name or not position or not email:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            cursor.execute("INSERT INTO staff (name, position, email) VALUES (?, ?, ?)", (name, position, email))
            conn.commit()
            load_staff()
            name_entry.delete(0, tk.END)
            position_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

        def delete_selected():
            selected = table.selection()
            if not selected:
                return
            staff_id = table.item(selected[0])['values'][0]
            cursor.execute("DELETE FROM staff WHERE id=?", (staff_id,))
            conn.commit()
            load_staff()

        def update_selected():
            selected = table.selection()
            if not selected:
                return
            staff_id = table.item(selected[0])['values'][0]
            name = name_entry.get()
            position = position_entry.get()
            email = email_entry.get()
            if not name or not position or not email:
                messagebox.showwarning("Input Error", "All fields are required to update.")
                return
            cursor.execute("UPDATE staff SET name=?, position=?, email=? WHERE id=?", (name, position, email, staff_id))
            conn.commit()
            load_staff()

        def fill_form(event):
            selected = table.selection()
            if selected:
                values = table.item(selected[0])['values']
                name_entry.delete(0, tk.END)
                name_entry.insert(0, values[1])
                position_entry.delete(0, tk.END)
                position_entry.insert(0, values[2])
                email_entry.delete(0, tk.END)
                email_entry.insert(0, values[3])

        # Buttons
        btn_frame = tk.Frame(self.content, bg="#264653")
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Staff", command=add_staff, bg="#2A9D8F", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Selected", command=update_selected, bg="#F4A261", fg="black").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=delete_selected, bg="#E76F51", fg="white").pack(side="left", padx=5)

        # Treeview
        table = ttk.Treeview(self.content, columns=("ID", "Name", "Position", "Email"), show="headings")
        table.heading("ID", text="ID")
        table.heading("Name", text="Name")
        table.heading("Position", text="Position")
        table.heading("Email", text="Email")
        table.pack(fill="both", expand=True, pady=10)
        table.bind("<<TreeviewSelect>>", fill_form)

        def load_staff():
            table.delete(*table.get_children())
            for row in cursor.execute("SELECT * FROM staff"):
                table.insert('', 'end', values=row)

        load_staff()

    def show_manage_shifts(self):
        self.clear_content()
        tk.Label(self.content, text="Manage Shifts", font=("Arial", 20), bg="#264653", fg="white").pack(pady=20)

    def show_attendance_reports(self):
        self.clear_content()
        tk.Label(self.content, text="Attendance Reports", font=("Arial", 20), bg="#264653", fg="white").pack(pady=20)

if __name__ == "__main__":
    app = StaffDashboard()
    app.mainloop()
