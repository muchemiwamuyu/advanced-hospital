from flask import Flask
from flask_pymongo import PyMongo
from controllers.patient_control import patient_bp
from controllers.user_register import user_bp
import tkinter as tk
from dashboards.register_staff import register

app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app)

# making other modules visible by the database
from controllers import patient_control
patient_control.mongo = mongo

# Register Blueprint for patient routes
app.register_blueprint(patient_bp)
app.register_blueprint(user_bp)

def main():
    root = tk.Tk()
    root.geometry("650x500")
    register(root)
    root.mainloop()

# Run the Flask app
if __name__ == "__main__":
    main()
    app.run(debug=True)

    