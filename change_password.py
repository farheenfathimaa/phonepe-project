import sqlalchemy
import urllib.parse
from sqlalchemy import text
import config

def change_password(new_password):
    # Connect using the current password from config.py
    current_password_encoded = urllib.parse.quote_plus(config.DB_PASSWORD)
    engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{config.DB_USER}:{current_password_encoded}@{config.DB_HOST}/')
    
    try:
        with engine.connect() as conn:
            # Change the password
            query = text(f"ALTER USER '{config.DB_USER}'@'{config.DB_HOST}' IDENTIFIED BY '{new_password}';")
            conn.execute(query)
            
            # Flush privileges
            conn.execute(text("FLUSH PRIVILEGES;"))
            conn.commit()
            print("✅ Password changed successfully in MySQL!")
            print(f"⚠️  IMPORTANT: Please update config.py with your new password: '{new_password}'")
    except Exception as e:
        print(f"❌ Error changing password: {e}")

if __name__ == "__main__":
    # ---------------------------------------------------------
    # TYPE YOUR NEW PASSWORD BELOW (inside the quotes)
    # ---------------------------------------------------------
    NEW_PASSWORD = "Omega7$6"
    
    change_password(NEW_PASSWORD)
