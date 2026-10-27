
import sqlite3
import hashlib
import hmac
import secrets
import re
import time
import tkinter as tk
from tkinter import simpledialog

# ==========================================
# CODEALPHA CYBER SECURITY INTERNSHIP
# TASK 3: SECURE CODING REVIEW
# ==========================================

DATABASE = "secure_users.db"
ITERATIONS = 600000
MAX_ATTEMPTS = 5
LOCK_TIME = 60


# ==========================================
# PASSWORD INPUT WINDOW
# ==========================================

def read_password(prompt):
    root = tk.Tk()
    root.withdraw()

    try:
        root.attributes("-topmost", True)

        password = simpledialog.askstring(
            "Secure Password Input",
            prompt,
            show="*",
            parent=root
        )

        return password
    finally:
        root.destroy()


# ==========================================
# DATABASE CREATION
# ==========================================

def create_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                locked_until REAL DEFAULT 0
            )
        """)


# ==========================================
# USERNAME VALIDATION
# ==========================================

def validate_username(username):
    return bool(
        re.fullmatch(r"[A-Za-z0-9_]{3,30}", username)
    )


# ==========================================
# PASSWORD VALIDATION
# ==========================================

def validate_password(password):
    if len(password) < 12:
        print("Password must contain at least 12 characters.")
        return False

    if len(password) > 128:
        print("Password must not exceed 128 characters.")
        return False

    return True


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return salt.hex(), hashed.hex()


# ==========================================
# PASSWORD VERIFICATION
# ==========================================

def verify_password(password, salt_hex, stored_hash):
    salt = bytes.fromhex(salt_hex)

    _, calculated_hash = hash_password(
        password,
        salt
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_hash
    )


# ==========================================
# USER REGISTRATION
# ==========================================

def register_user():
    print("\n" + "=" * 45)
    print("           USER REGISTRATION")
    print("=" * 45)

    username = input("Create Username: ").strip()

    if not validate_username(username):
        print("Invalid username!")
        print("Use 3-30 letters, numbers or underscores.")
        return

    print("Opening password window...")

    password = read_password("Create Password:")

    if password is None:
        print("Registration cancelled.")
        return

    if not validate_password(password):
        return

    confirm_password = read_password(
        "Confirm Password:"
    )

    if confirm_password is None:
        print("Registration cancelled.")
        return

    if not hmac.compare_digest(
        password,
        confirm_password
    ):
        print("Passwords do not match!")
        return

    salt, password_hash = hash_password(password)

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                INSERT INTO users
                (username, salt, password_hash)
                VALUES (?, ?, ?)
            """, (
                username,
                salt,
                password_hash
            ))

        print("\nRegistration Successful!")
        print("You can now login.")

    except sqlite3.IntegrityError:
        print("Username already exists!")

    except sqlite3.Error:
        print("Registration failed. Please try again.")


# ==========================================
# USER LOGIN
# ==========================================

def login_user():
    print("\n" + "=" * 45)
    print("               USER LOGIN")
    print("=" * 45)

    username = input("Enter Username: ").strip()

    print("Opening password window...")

    password = read_password("Enter Password:")

    if password is None:
        print("Login cancelled.")
        return False

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute("""
                SELECT id, salt, password_hash,
                       failed_attempts, locked_until
                FROM users
                WHERE username = ?
            """, (username,))

            user = cursor.fetchone()

            if user is None:
                print("Invalid username or password!")
                return False

            user_id, salt, stored_hash, attempts, locked_until = user

            now = time.time()

            if now < locked_until:
                remaining = int(locked_until - now) + 1

                print(
                    f"Account temporarily locked. "
                    f"Try again in {remaining} seconds."
                )
                return False

            if verify_password(
                password,
                salt,
                stored_hash
            ):
                conn.execute("""
                    UPDATE users
                    SET failed_attempts = 0,
                        locked_until = 0
                    WHERE id = ?
                """, (user_id,))

                print("\nLogin Successful!")
                print("Welcome,", username)
                return True

            attempts += 1

            if attempts >= MAX_ATTEMPTS:
                conn.execute("""
                    UPDATE users
                    SET failed_attempts = 0,
                        locked_until = ?
                    WHERE id = ?
                """, (
                    now + LOCK_TIME,
                    user_id
                ))

                print("\nToo many failed attempts!")
                print("Account locked for 60 seconds.")

            else:
                conn.execute("""
                    UPDATE users
                    SET failed_attempts = ?
                    WHERE id = ?
                """, (
                    attempts,
                    user_id
                ))

                print("\nInvalid username or password!")
                print(
                    "Remaining attempts:",
                    MAX_ATTEMPTS - attempts
                )

            return False

    except sqlite3.Error:
        print("Login failed. Please try again.")
        return False


# ==========================================
# MAIN MENU
# ==========================================

def main():
    try:
        create_database()
    except sqlite3.Error:
        print("Database initialization failed.")
        return

    while True:
        print("\n" + "=" * 50)
        print("        SECURE AUTHENTICATION SYSTEM")
        print("=" * 50)

        print("1. Register New User")
        print("2. Login")
        print("3. Exit")

        print("=" * 50)

        choice = input(
            "Enter your choice (1-3): "
        ).strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            login_user()

        elif choice == "3":
            print("\nApplication Closed Successfully.")
            break

        else:
            print("Invalid choice! Try again.")


# ==========================================
# PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram terminated.")
