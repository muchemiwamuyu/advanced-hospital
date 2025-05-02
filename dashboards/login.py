import tkinter

window = tkinter.Tk()
window.title("Nova-care login form")
window.geometry('440x440')
window.configure(bg='#CAE9FF')

frame = tkinter.Frame(bg='#CAE9FF')

def login():
    print("Hello world")

# creating widgets
login_label = tkinter.Label(frame, text="Login", bg='#CAE9FF', fg="#001524", font=("Arial", 18))
staff_id_label = tkinter.Label(frame, text="Staff-id", bg='#CAE9FF', fg="#001524", font=("Arial", 12))
staff_id_entry = tkinter.Entry(frame,  font=("Arial", 12))
password_entry = tkinter.Entry(frame, show="*",  font=("Arial", 12))
password_label = tkinter.Label(frame, text="Password", bg='#CAE9FF', fg="#001524", font=("Arial", 12))
login_button = tkinter.Button(frame, text="login", bg='#1B4965', fg='#ffffff',  font=("Arial", 12), command=login)

# placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
staff_id_label.grid(row=1, column=0)
staff_id_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

window.mainloop()
# nothing can be executed over here