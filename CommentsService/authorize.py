# to validate the users and their roles (it connects with the comments.py)
import requests
import pyodbc
from config import Config

# get user info from api
def get_api_user(api_key):
    headers = {"UserIDAuth": api_key}
    response = requests.get(Config.AUTH_API, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None

def validate_api(api_key, required_scopes=None):
    if not api_key:
        return None
    # For testing, treat api_key as email
    local_user = get_local_user(api_key)
    if local_user:
        return local_user
    return None

# i have api user, i have sql user role uh! get user role (treats email as api key)
def validate_user(email, password):
    try:
        url = Config.AUTH_API
        thedeets = {'Email': email, 'Password': password}
        response = requests.post(url, json=thedeets)

        if response.status_code == 200:
            user =  response.json()
            return user
        else:
            return None
    
    except Exception as e:
        print(f"Auth Error: {e}")
        return None
    
    # SQL helpers
def _get_conn():
    return pyodbc.connect(Config.pyodbc_conn_str())
    
def get_user_by_id(user_id):
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT User_ID, Email, Role FROM CW2.[User] WHERE User_ID = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return {'User_ID': int(row[0]), 'Email': row[1], 'Role': row[2]}
        return None
    
def get_local_user(email):
    with _get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT User_ID, Email, Role FROM CW2.[User] WHERE Email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return {'User_ID': int(row[0]), 'Email': row[1], 'Role': row[2]}
        return None

# returns True if token_info corresponds to admin role in authenticator or in local DB
def is_admin_from_tokeninfo(token_info):
    if not token_info:
        return False
    # If the authenticator returns Role in token_info, check it
    role = token_info.get("Role") or token_info.get("role")
    if role and str(role).lower() == "admin":
        return True

    # fallback: check local DB email->role
    email = token_info.get("Email") or token_info.get("email")
    if email:
        local = get_local_user(email)
        if local and local.get("Role") and str(local["Role"]).lower() == "admin":
            return True
    return False