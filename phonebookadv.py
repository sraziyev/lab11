import sqlite3

# Database connection
conn = sqlite3.connect('phonebook.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS PhoneBook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    phone_number TEXT UNIQUE NOT NULL
)
""")
conn.commit()

# Function to query by pattern
def query_by_pattern(pattern):
    query = """
    SELECT * FROM PhoneBook
    WHERE first_name LIKE ? OR last_name LIKE ? OR phone_number LIKE ?
    """
    cursor.execute(query, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
    results = cursor.fetchall()
    for row in results:
        print(row)

# Procedure to insert or update user
def insert_or_update_user(name, phone):
    try:
        # Check if the user exists
        cursor.execute("""
        SELECT * FROM PhoneBook WHERE first_name = ?
        """, (name,))
        user = cursor.fetchone()

        if user:
            # Update the phone number
            cursor.execute("""
            UPDATE PhoneBook SET phone_number = ? WHERE first_name = ?
            """, (phone, name))
            print(f"Updated phone number for {name}.")
        else:
            # Insert new user
            cursor.execute("""
            INSERT INTO PhoneBook (first_name, phone_number) VALUES (?, ?)
            """, (name, phone))
            print(f"Inserted new user: {name}.")
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Error:", e)

# Procedure to insert many users
def insert_many_users(users):
    invalid_data = []
    for user in users:
        name, phone = user.get('name'), user.get('phone')
        if not name or not phone or not phone.isdigit():  # Basic validation
            invalid_data.append(user)
            continue

        try:
            cursor.execute("""
            INSERT INTO PhoneBook (first_name, phone_number)
            VALUES (?, ?)
            """, (name, phone))
        except sqlite3.IntegrityError:
            invalid_data.append(user)

    conn.commit()
    print("Batch insertion complete.")
    if invalid_data:
        print("Invalid records:", invalid_data)

# Function to query data with pagination
def query_with_pagination(limit, offset):
    query = """
    SELECT * FROM PhoneBook LIMIT ? OFFSET ?
    """
    cursor.execute(query, (limit, offset))
    results = cursor.fetchall()
    for row in results:
        print(row)

# Procedure to delete data
def delete_by_identifier(identifier):
    cursor.execute("""
    DELETE FROM PhoneBook WHERE first_name = ? OR phone_number = ?
    """, (identifier, identifier))
    conn.commit()
    print("Record deleted successfully!")

# Menu for interaction
def menu():
    while True:
        print("\nPhoneBook Menu")
        print("1. Query by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("4. Query with pagination")
        print("5. Delete record")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            pattern = input("Enter pattern to search: ")
            query_by_pattern(pattern)
        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            insert_or_update_user(name, phone)
        elif choice == "3":
            print("Enter user details as a list of dictionaries:")
            print("Example: [{'name': 'John', 'phone': '12345'}, {'name': 'Jane', 'phone': '67890'}]")
            user_list = eval(input("Enter list: "))  # Note: Use caution with eval in production!
            insert_many_users(user_list)
        elif choice == "4":
            limit = int(input("Enter number of records to fetch (limit): "))
            offset = int(input("Enter offset: "))
            query_with_pagination(limit, offset)
        elif choice == "5":
            identifier = input("Enter username or phone number to delete: ")
            delete_by_identifier(identifier)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the menu
menu()

# Close database connection
conn.close()