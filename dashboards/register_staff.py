import tkinter as tk
from tkinter import ttk, messagebox
from services.authentication import register as register_user
from services.authentication import login_user

def register_screen(root):
    root.title("Staff Registration Form")
    root.configure(bg="#f0f4f7")

    frame = tk.Frame(root, bg="#f0f4f7")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Label(frame, text="Register Staff", font=("Arial", 18), bg="#f0f4f7", fg="#001524")\
        .grid(row=0, column=0, columnspan=3, pady=20)

    # --- Name fields ---
    tk.Label(frame, text="First Name:", bg="#f0f4f7").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Label(frame, text="Last Name:", bg="#f0f4f7").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    first_name_entry = tk.Entry(frame, width=25)
    last_name_entry = tk.Entry(frame, width=25)
    first_name_entry.grid(row=2, column=0, padx=5, pady=5)
    last_name_entry.grid(row=2, column=1, padx=5, pady=5)

    # --- Role ---
    tk.Label(frame, text="Role:", bg="#f0f4f7").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    title_combobox = ttk.Combobox(frame, values=["Admin", "Doctor", "Nurse", "Lab-Tech", "Environment", "Support"])
    title_combobox.grid(row=2, column=2, padx=5, pady=5)

    # --- Staff ID ---
    tk.Label(frame, text="Staff ID:", bg="#f0f4f7").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    staff_id_spinbox = tk.Spinbox(frame, from_=2222, to=9989, width=27)
    staff_id_spinbox.grid(row=4, column=0, padx=5, pady=5)

    # --- Address ---
    tk.Label(frame, text="Address:", bg="#f0f4f7").grid(row=3, column=1, padx=5, pady=5, sticky="w")
    address_combobox = ttk.Combobox(frame, values=[
        "Nairobi West (South C, South B)",
        "Pipeline",
        "Embakasi",
        "Kilimani",
        "Westlands",
        "Ruiru"
    ])
    address_combobox.grid(row=4, column=1, padx=5, pady=5)

    # --- Registered? ---
    tk.Label(frame, text="Currently Registered:", bg="#f0f4f7").grid(row=5, column=0, padx=5, pady=10, sticky="w")
    registered_var = tk.IntVar()
    registered_check = tk.Checkbutton(frame, text="Yes", bg="#f0f4f7", variable=registered_var)
    registered_check.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    # --- Submit Function ---
    def submit():
        user_data = {
            "first_name": first_name_entry.get(),
            "last_name": last_name_entry.get(),
            "staff_id": staff_id_spinbox.get(),
            "role": title_combobox.get(),
            "address": address_combobox.get()
        }

        if register_user(user_data):
            messagebox.showinfo("Success", "Registration successful!")
            root.destroy()  # Close registration window
            new_root = tk.Tk()
            login_user(new_root)  # Show login window
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Registration failed. Try again.")

    # --- Register Button ---
    register_button = tk.Button(
        frame,
        text="Register",
        bg="#1B4965",
        fg="white",
        font=("Arial", 12),
        command=submit
    )
    register_button.grid(row=7, column=0, columnspan=3, pady=30)

    return frame  # Optional
