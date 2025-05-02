import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# DB Connection
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        blood_pressure TEXT,
        heart_rate TEXT,
        temperature TEXT,
        date TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
""")
conn.commit()


class NurseDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nurse Dashboard")
        self.geometry("1000x650")
        self.configure(bg="#1e1e1e")
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar = tk.Frame(self, width=220, bg="#2A9D8F", padx=15, pady=20)
        sidebar.pack(side="left", fill="y")

        title = tk.Label(sidebar, text="Nurse Panel", font=("Helvetica", 16, "bold"), bg="#2A9D8F", fg="white")
        title.pack(pady=10)

        btn_vitals = tk.Button(sidebar, text="🩺  Update Vitals", bg="#E9C46A", font=("Arial", 12), command=self.update_vitals)
        btn_vitals.pack(pady=15, fill="x")

        # Content
        self.content = tk.Frame(self, bg="#264653", padx=30, pady=30)
        self.content.pack(side="right", expand=True, fill="both")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def update_vitals(self):
        self.clear_content()
        tk.Label(self.content, text="Update Patient Vitals", font=("Arial", 20, "bold"), bg="#264653", fg="white").pack(pady=10)

        form = tk.Frame(self.content, bg="#264653")
        form.pack(pady=20)

        # Form fields
        fields = {
            "Patient ID": tk.Entry(form, width=30, font=("Arial", 12)),
            "Blood Pressure": tk.Entry(form, width=30, font=("Arial", 12)),
            "Heart Rate": tk.Entry(form, width=30, font=("Arial", 12)),
            "Temperature": tk.Entry(form, width=30, font=("Arial", 12)),
            "Date (YYYY-MM-DD)": tk.Entry(form, width=30, font=("Arial", 12)),
        }

        for idx, (label, entry) in enumerate(fields.items()):
            tk.Label(form, text=label + ":", bg="#264653", fg="white", font=("Arial", 12)).grid(row=idx, column=0, pady=5, sticky="w")
            entry.grid(row=idx, column=1, pady=5)

        notes_label = tk.Label(form, text="Care Notes:", bg="#264653", fg="white", font=("Arial", 12))
        notes_label.grid(row=5, column=0, sticky="nw", pady=5)
        notes_entry = tk.Text(form, width=40, height=4, font=("Arial", 12))
        notes_entry.grid(row=5, column=1, pady=5)

        def save_vitals():
            data = {label: entry.get() for label, entry in fields.items()}
            notes = notes_entry.get("1.0", tk.END).strip()

            if not all(data.values()) or not notes:
                messagebox.showwarning("Missing Data", "Please fill all fields.")
                return

            cursor.execute("""
                INSERT INTO vitals (patient_id, blood_pressure, heart_rate, temperature, date, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["Patient ID"],
                data["Blood Pressure"],
                data["Heart Rate"],
                data["Temperature"],
                data["Date (YYYY-MM-DD)"],
                notes
            ))
            conn.commit()

            for entry in fields.values():
                entry.delete(0, tk.END)
            notes_entry.delete("1.0", tk.END)
            load_vitals()
            messagebox.showinfo("Saved", "Vitals and care notes updated.")

        tk.Button(form, text="Submit", command=save_vitals, bg="#2A9D8F", fg="white", font=("Arial", 12)).grid(row=6, columnspan=2, pady=10)

        # Table
        table_frame = tk.Frame(self.content)
        table_frame.pack(pady=20, fill="both", expand=True)

        table_scroll = tk.Scrollbar(table_frame)
        table_scroll.pack(side="right", fill="y")

        self.vitals_table = ttk.Treeview(table_frame, columns=("ID", "Patient ID", "BP", "HR", "Temp", "Date", "Notes"), show="headings", yscrollcommand=table_scroll.set)
        table_scroll.config(command=self.vitals_table.yview)

        for col in ("ID", "Patient ID", "BP", "HR", "Temp", "Date", "Notes"):
            self.vitals_table.heading(col, text=col)
            self.vitals_table.column(col, anchor="center")

        self.vitals_table.pack(fill="both", expand=True)

        def load_vitals():
            self.vitals_table.delete(*self.vitals_table.get_children())
            for row in cursor.execute("SELECT * FROM vitals"):
                self.vitals_table.insert('', 'end', values=row)

        load_vitals()

if __name__ == "__main__":
    app = NurseDashboard()
    app.mainloop()
