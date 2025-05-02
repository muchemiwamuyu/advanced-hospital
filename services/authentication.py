from dotenv import load_dotenv
import os
import requests

load_dotenv()

register_url = os.getenv("REGISTER_URL")
login_url = os.getenv("LOGIN_URL")

def register(user_data):
     response = requests.post(register_url, json=user_data)
     if response.status_code == 201:
          print("Registration successful")
          return True
     else:
          print("Registration failed")
          return False
     
def login_user(credentials):
    """
    Sends a POST request to login the user and returns the token if successful
    """
    response = requests.post(login_url, json=credentials)
    if response.status_code == 200:

        role = response.json().get('role')  # Get role to decide which dashboard to show
        return role
    else:
        print(f"Login failed: {response.json()}")
        return None, None


