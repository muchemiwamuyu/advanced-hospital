import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# DB Setup
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS lab_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        test_type TEXT,
        results TEXT,
        date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
""")
conn.commit()

class LabTechDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab Technician Dashboard")
        self.geometry("1000x600")
        self.configure(bg="#1e1e1e")
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Upload Lab Test Results", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)

        form = tk.Frame(self, bg="#1e1e1e")
        form.pack(pady=10)

        # Patient ID
        tk.Label(form, text="Patient ID:", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.patient_id_entry = tk.Entry(form, font=("Arial", 12))
        self.patient_id_entry.grid(row=0, column=1, pady=5, padx=10)

        # Test Type
        tk.Label(form, text="Test Type:", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.test_type_entry = tk.Entry(form, font=("Arial", 12))
        self.test_type_entry.grid(row=1, column=1, pady=5, padx=10)

        # Results
        tk.Label(form, text="Results:", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=2, column=0, sticky="nw", pady=5)
        self.results_text = tk.Text(form, width=40, height=6, font=("Arial", 12))
        self.results_text.grid(row=2, column=1, pady=5, padx=10)

        # Date
        tk.Label(form, text="Date (YYYY-MM-DD):", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(form, font=("Arial", 12))
        self.date_entry.grid(row=3, column=1, pady=5, padx=10)

        # Upload Button
        tk.Button(form, text="Upload Result", command=self.upload_result, bg="#2A9D8F", fg="white", font=("Arial", 12)).grid(row=4, columnspan=2, pady=20)

        # Results Table
        self.create_table()

    def create_table(self):
        table_frame = tk.Frame(self, bg="#1e1e1e")
        table_frame.pack(pady=10, fill="both", expand=True)

        table_scroll = tk.Scrollbar(table_frame)
        table_scroll.pack(side="right", fill="y")

        self.table = ttk.Treeview(table_frame, columns=("ID", "Patient ID", "Test Type", "Results", "Date"), show="headings", yscrollcommand=table_scroll.set)
        table_scroll.config(command=self.table.yview)

        for col in ("ID", "Patient ID", "Test Type", "Results", "Date"):
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        self.table.pack(fill="both", expand=True)
        self.load_results()

    def upload_result(self):
        pid = self.patient_id_entry.get()
        test_type = self.test_type_entry.get()
        results = self.results_text.get("1.0", tk.END).strip()
        date = self.date_entry.get()

        if not pid or not test_type or not results or not date:
            messagebox.showwarning("Missing Data", "All fields are required.")
            return

        cursor.execute("INSERT INTO lab_results (patient_id, test_type, results, date) VALUES (?, ?, ?, ?)", (pid, test_type, results, date))
        conn.commit()
        self.load_results()
        self.patient_id_entry.delete(0, tk.END)
        self.test_type_entry.delete(0, tk.END)
        self.results_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Lab result uploaded.")

    def load_results(self):
        self.table.delete(*self.table.get_children())
        for row in cursor.execute("SELECT * FROM lab_results"):
            self.table.insert('', 'end', values=row)

if __name__ == "__main__":
    app = LabTechDashboard()
    app.mainloop()
