from functions import verify_user, tax_prompt, save_to_csv, read_from_csv

user_sessions = {}

def main_menu():
    while True:
        print("\n===== Malaysia Tax Input Program =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            username, ic = register_user()
            if username:
                logged_in_menu(username, ic)
        elif choice == '2':
            username, ic = login_user()
            if username:
                logged_in_menu(username, ic)
        elif choice == '3':
            print("Thank you for using the Malaysia Tax Input Program.")
            break
        else:
            print("Invalid choice. Try again.")

def register_user():
    print("\n=== User Registration ===")
    username = input("Enter your name (used as ID): ").strip().upper()
    ic_number = input("Enter your 12-digit IC Number: ").strip()
    password = ic_number[-4:]

    if verify_user(ic_number, password):
        confirm = input("Please confirm your password (last 4 digits of IC): ").strip()
        if confirm == password:
            print("Registration successful and logged in.")
            user_sessions[username] = {'ic': ic_number}
            return username, ic_number
        else:
            print("Password confirmation failed.")
    else:
        print("Invalid IC number format.")
    return None, None

def login_user():
    print("\n=== User Login ===")
    username = input("Enter your username: ").strip().upper()
    ic_number = input("Enter your 12-digit IC number: ").strip()
    password = input("Enter your password (last 4 digits of IC): ").strip()

    if verify_user(ic_number, password):
        print("Login successful.")
        user_sessions[username] = {'ic': ic_number}
        return username, ic_number
    else:
        print("Login failed. Incorrect credentials.")
        return None, None

def logged_in_menu(username, ic):
    while True:
        print(f"\n===== Welcome, {username} =====")
        print("1. Enter Taxing Year & Annual Income")
        print("2. Enter Tax Reliefs")
        print("3. Calculate Tax Payable")
        print("4. View Tax Record")
        print("5. Logout")
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            tax_year = input("Enter the taxing year (e.g., 2024): ").strip()
            try:
                income = float(input("Enter annual income for that year (RM): "))
                user_sessions[username]['year'] = tax_year
                user_sessions[username]['income'] = income
                print("Annual income saved.")
            except ValueError:
                print("Invalid input. Please enter numbers.")
        elif choice == '2':
            reliefs = {}
            reliefs['Individual'] = get_relief("Individual Tax Relief", 0, 9000)
            reliefs['Spouse'] = get_relief("Spouse Tax Relief", 0, 4000)
            num_children = int(input("Enter number of children (max 12): "))
            reliefs['Medical'] = get_relief("Medical Expenses Relief", 0, 8000)
            reliefs['Lifestyle'] = get_relief("Lifestyle Relief", 0, 2500)
            reliefs['Education'] = get_relief("Education Fees Relief", 0, 7000)
            reliefs['Parental'] = get_relief("Parental Care Relief", 0, 5000)

            user_sessions[username]['reliefs'] = reliefs
            user_sessions[username]['num_children'] = num_children
            print("Tax reliefs saved successfully.")
        elif choice == '3':
            if 'income' not in user_sessions[username] or 'reliefs' not in user_sessions[username]:
                print("Please enter your income and tax reliefs first.")
                continue
            year = user_sessions[username]['year']
            income = user_sessions[username]['income']
            relief_dict = user_sessions[username]['reliefs']
            num_kids = user_sessions[username]['num_children']
            reliefs, total_relief, tax_payable = tax_prompt(income, year, relief_dict, num_kids)

            save = input("Save result to file? (Y/N): ").strip().upper()
            if save == 'Y':
                save_to_csv(username, user_sessions[username]['ic'], year, income, total_relief, tax_payable)
        elif choice == '4':
            read_from_csv(username)
        elif choice == '5':
            print(f"Logging out {username}.")
            break
        else:
            print("Invalid option. Please try again.")

def get_relief(label, min_val, max_val):
    while True:
        try:
            val = float(input(f"{label} (RM {min_val} - {max_val}): RM "))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Value must be between RM {min_val} and RM {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main_menu()
