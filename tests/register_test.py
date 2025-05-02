import tkinter 
from tkinter import ttk
window = tkinter.Tk()
window.title("Staff registration")

frame = tkinter.Frame(window)
frame.pack()

# first frame for registering staff
staff_info_frame = tkinter.LabelFrame(frame, text="Staff information")
staff_info_frame.grid(row=0, column=0, padx=20, pady=20)

first_name_label = tkinter.Label(staff_info_frame, text="First name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(staff_info_frame, text="Last name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(staff_info_frame)
last_name_entry = tkinter.Entry(staff_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

role_label = tkinter.Label(staff_info_frame, text="Role")
role_entry = ttk.Combobox(staff_info_frame, values=["Admin", "Doctor", "Nurse", "lab-tech", "Environment", "Support"])
role_label.grid(row=0, column=2)
role_entry.grid(row=1, column=2)

number_label = tkinter.Label(staff_info_frame, text="Phone number")
number_entry = tkinter.Entry(staff_info_frame)
number_label.grid(row=2, column=0)
number_entry.grid(row=3, column=0)

staff_id_label = tkinter.Label(staff_info_frame, text="Staff id")
staff_id_entry = tkinter.Entry(staff_info_frame)
staff_id_label.grid(row=2, column=1)
staff_id_entry.grid(row=3, column=1)

password_label = tkinter.Label(staff_info_frame, text="password")
password_entry = tkinter.Entry(staff_info_frame, show="*")
password_label.grid(row=2, column=2)
password_entry.grid(row=3, column=2)

login_button = tkinter.Button(staff_info_frame, text="Register")
login_button.grid(row=4, column=0)

for widget in staff_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()