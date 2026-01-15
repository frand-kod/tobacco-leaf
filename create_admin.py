import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.repository.user_repository import UserRepository
import getpass

def create_admin_cli():
    print("--- Create Admin User ---")
    name = input("Nama: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    
    if not name or not email or not password:
        print("Error: Semua field harus diisi!")
        return

    db = SessionLocal()
    try:
        # Cek apakah email sudah ada
        if UserRepository.get_user_by_email(db, email):
            print(f"Error: Email {email} sudah terdaftar!")
            return

        # Buat user admin
        new_admin = User(
            name=name,
            email=email,
            password=hash_password(password),
            role="admin"
        )
        
        UserRepository.create_user(db, new_admin)
        print(f"Berhasil! Admin {name} telah dibuat.")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_cli()