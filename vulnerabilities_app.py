
import sqlite3

# ==========================================
# VULNERABLE LOGIN AUTHENTICATION SYSTEM
# ==========================================

DATABASE = "vulnerable_users.db"

# Vulnerability 1: Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Vulnerability 2: Plaintext password storage
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password)
        VALUES (?, ?)
    """, (ADMIN_USERNAME, ADMIN_PASSWORD))

    connection.commit()
    connection.close()


# ==========================================
# USER REGISTRATION
# ==========================================

def register_user():
    print("\n========== USER REGISTRATION ==========")

    username = input("Create Username: ")
    password = input("Create Password: ")

    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        # Password stored without hashing
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        connection.commit()
        connection.close()

        print("\nRegistration Successful!")

    except sqlite3.IntegrityError:
        print("Username already exists!")


# ==========================================
# VULNERABLE LOGIN
# ==========================================

def login_user():
    print("\n========== USER LOGIN ==========")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Vulnerability 3: SQL Injection
    # Unsafe string concatenation
    query = (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    try:
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            print("\nLogin Successful!")
            print("Welcome,", user[1])
        else:
            print("\nInvalid Username or Password!")

    except sqlite3.Error as error:
        # Vulnerability 4: Error information disclosure
        print("Database Error:", error)

    finally:
        connection.close()


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    create_database()

    print("\n" + "=" * 50)
    print("       VULNERABLE AUTHENTICATION SYSTEM")
    print("=" * 50)

    while True:
        print("\n1. Register New User")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            register_user()

        elif choice == "2":
            login_user()

        elif choice == "3":
            print("\nApplication Closed.")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()
