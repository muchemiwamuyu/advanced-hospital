import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# DB Setup
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS diagnosis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS encounters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        summary TEXT,
        date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
""")
conn.commit()

class DoctorDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Doctor Dashboard")
        self.geometry("1000x650")
        self.configure(bg="#1e1e1e")

        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar = tk.Frame(self, width=220, bg="#2A9D8F", padx=15, pady=20)
        sidebar.pack(side="left", fill="y")

        title = tk.Label(sidebar, text="Doctor Panel", font=("Helvetica", 16, "bold"), bg="#2A9D8F", fg="white")
        title.pack(pady=10)

        btn_patients = tk.Button(sidebar, text="🧑‍⚕️  Patients", bg="#E9C46A", font=("Arial", 12), command=self.show_patients)
        btn_diagnosis = tk.Button(sidebar, text="📝  Diagnosis", bg="#F4A261", font=("Arial", 12), command=self.show_diagnosis)
        btn_encounters = tk.Button(sidebar, text="📄  Encounter Records", bg="#E76F51", font=("Arial", 12), command=self.show_encounters)

        for btn in (btn_patients, btn_diagnosis, btn_encounters):
            btn.pack(pady=15, fill="x")

        # Main content
        self.content = tk.Frame(self, bg="#264653", padx=30, pady=30)
        self.content.pack(side="right", expand=True, fill="both")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_patients(self):
        self.clear_content()
        tk.Label(self.content, text="Patients", font=("Arial", 20, "bold"), bg="#264653", fg="white").pack(pady=10)

        form = tk.Frame(self.content, bg="#264653")
        form.pack(pady=15)

        labels = ["Name:", "Age:", "Gender:"]
        entries = []
        for idx, text in enumerate(labels):
            tk.Label(form, text=text, bg="#264653", fg="white", font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(form, width=30, font=("Arial", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries.append(entry)

        name_entry, age_entry, gender_entry = entries

        def add_patient():
            name = name_entry.get()
            age = age_entry.get()
            gender = gender_entry.get()
            if not name or not age or not gender:
                messagebox.showwarning("Input Error", "Please fill all fields.")
                return
            cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
            conn.commit()
            load_patients()
            for entry in entries:
                entry.delete(0, tk.END)

        tk.Button(form, text="Add Patient", command=add_patient, bg="#2A9D8F", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2, pady=10)

        table_frame = tk.Frame(self.content)
        table_frame.pack(pady=10, fill="both", expand=True)

        table_scroll = tk.Scrollbar(table_frame)
        table_scroll.pack(side="right", fill="y")

        table = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender"), show="headings", yscrollcommand=table_scroll.set)
        table_scroll.config(command=table.yview)

        for col in ("ID", "Name", "Age", "Gender"):
            table.heading(col, text=col)
            table.column(col, anchor="center")

        table.pack(fill="both", expand=True)

        def load_patients():
            table.delete(*table.get_children())
            for row in cursor.execute("SELECT * FROM patients"):
                table.insert('', 'end', values=row)

        load_patients()

    def show_diagnosis(self):
        self.clear_content()
        tk.Label(self.content, text="Add Diagnosis", font=("Arial", 20, "bold"), bg="#264653", fg="white").pack(pady=10)

        form = tk.Frame(self.content, bg="#264653")
        form.pack(pady=20)

        tk.Label(form, text="Patient ID:", bg="#264653", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        pid_entry = tk.Entry(form, width=30, font=("Arial", 12))
        pid_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Diagnosis Notes:", bg="#264653", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="nw", pady=5)
        notes_entry = tk.Text(form, width=40, height=6, font=("Arial", 12))
        notes_entry.grid(row=1, column=1, pady=5)

        def add_diagnosis():
            pid = pid_entry.get()
            notes = notes_entry.get("1.0", tk.END).strip()
            if not pid or not notes:
                messagebox.showwarning("Missing Data", "Fill in all fields.")
                return
            cursor.execute("INSERT INTO diagnosis (patient_id, notes) VALUES (?, ?)", (pid, notes))
            conn.commit()
            pid_entry.delete(0, tk.END)
            notes_entry.delete("1.0", tk.END)
            load_diagnoses()
            messagebox.showinfo("Saved", "Diagnosis record added.")

        tk.Button(form, text="Save Diagnosis", command=add_diagnosis, bg="#2A9D8F", fg="white", font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)

        # Diagnosis Table
        table_frame = tk.Frame(self.content)
        table_frame.pack(pady=10, fill="both", expand=True)

        table_scroll = tk.Scrollbar(table_frame)
        table_scroll.pack(side="right", fill="y")

        diagnosis_table = ttk.Treeview(table_frame, columns=("ID", "Patient ID", "Notes"), show="headings", yscrollcommand=table_scroll.set)
        table_scroll.config(command=diagnosis_table.yview)

        for col in ("ID", "Patient ID", "Notes"):
            diagnosis_table.heading(col, text=col)
            diagnosis_table.column(col, anchor="center")

        diagnosis_table.pack(fill="both", expand=True)

        def load_diagnoses():
            diagnosis_table.delete(*diagnosis_table.get_children())
            for row in cursor.execute("SELECT * FROM diagnosis"):
                diagnosis_table.insert('', 'end', values=row)

        load_diagnoses()

    def show_encounters(self):
        self.clear_content()
        tk.Label(self.content, text="Encounter Records", font=("Arial", 20, "bold"), bg="#264653", fg="white").pack(pady=10)

        form = tk.Frame(self.content, bg="#264653")
        form.pack(pady=20)

        tk.Label(form, text="Patient ID:", bg="#264653", fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        pid_entry = tk.Entry(form, width=30, font=("Arial", 12))
        pid_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Summary:", bg="#264653", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="nw", pady=5)
        summary_entry = tk.Text(form, width=40, height=6, font=("Arial", 12))
        summary_entry.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Date (YYYY-MM-DD):", bg="#264653", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(form, width=30, font=("Arial", 12))
        date_entry.grid(row=2, column=1, pady=5)

        def add_encounter():
            pid = pid_entry.get()
            summary = summary_entry.get("1.0", tk.END).strip()
            date = date_entry.get()
            if not pid or not summary or not date:
                messagebox.showwarning("Missing Data", "Please fill all fields.")
                return
            cursor.execute("INSERT INTO encounters (patient_id, summary, date) VALUES (?, ?, ?)", (pid, summary, date))
            conn.commit()
            pid_entry.delete(0, tk.END)
            summary_entry.delete("1.0", tk.END)
            date_entry.delete(0, tk.END)
            load_encounters()
            messagebox.showinfo("Saved", "Encounter record added.")

        tk.Button(form, text="Save Record", command=add_encounter, bg="#2A9D8F", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2, pady=15)

        # Encounter Table
        table_frame = tk.Frame(self.content)
        table_frame.pack(pady=10, fill="both", expand=True)

        table_scroll = tk.Scrollbar(table_frame)
        table_scroll.pack(side="right", fill="y")

        encounter_table = ttk.Treeview(table_frame, columns=("ID", "Patient ID", "Summary", "Date"), show="headings", yscrollcommand=table_scroll.set)
        table_scroll.config(command=encounter_table.yview)

        for col in ("ID", "Patient ID", "Summary", "Date"):
            encounter_table.heading(col, text=col)
            encounter_table.column(col, anchor="center")

        encounter_table.pack(fill="both", expand=True)

        def load_encounters():
            encounter_table.delete(*encounter_table.get_children())
            for row in cursor.execute("SELECT * FROM encounters"):
                encounter_table.insert('', 'end', values=row)

        load_encounters()

if __name__ == "__main__":
    app = DoctorDashboard()
    app.mainloop()
