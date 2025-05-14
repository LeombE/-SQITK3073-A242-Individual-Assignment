import pandas as pd
import os

BASE_PATH = './'

def verify_user(ic_number, password):
    return len(ic_number) == 12 and password == ic_number[-4:]

def save_to_csv(username, ic_number, tax_year, income, total_relief, tax_payable):
    file_path = os.path.join(BASE_PATH, 'tax_summary.csv')
    record = {
        "User ID": username,
        "IC Number": ic_number,
        "Tax Year": tax_year,
        "Annual Income (RM)": income,
        "Total Tax Relief (RM)": total_relief,
        "Tax Payable (RM)": tax_payable
    }
    df = pd.DataFrame([record])
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)
    print('Data successfully saved.')

def read_from_csv(username):
    file_path = os.path.join(BASE_PATH, 'tax_summary.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        user_df = df[df['User ID'] == username]
        if user_df.empty:
            print("No records found for this user.")
        else:
            print(f"\n=== Tax Records for {username} ===")
            print(user_df.to_string(index=False))
    else:
        print("No tax record file found.")

def tax_prompt(income, tax_year, reliefs, num_children):
    print('\n===== Calculating Tax Payable =====')
    reliefs['Child'] = min(num_children, 12) * 8000
    total_relief = sum(reliefs.values())
    taxable_income = max(0, income - total_relief)

    if taxable_income <= 5000:
        tax_rate = 0
        tax_payable = taxable_income * tax_rate
        category = 'A'
    elif taxable_income <= 20000:
        tax_rate = 0.01
        tax_payable = taxable_income * tax_rate
        category = 'B'
    elif taxable_income <= 35000:
        tax_rate = 0.03
        tax_payable = 150 + (taxable_income * tax_rate)
        category = 'C'
    elif taxable_income <= 50000:
        tax_rate = 0.06
        tax_payable = 600 + (taxable_income * tax_rate)
        category = 'D'
    elif taxable_income <= 70000:
        tax_rate = 0.11
        tax_payable = 1500 + (taxable_income * tax_rate)
        category = 'E'
    elif taxable_income <= 100000:
        tax_rate = 0.19
        tax_payable = 3700 + (taxable_income * tax_rate)
        category = 'F'
    elif taxable_income <= 400000:
        tax_rate = 0.25
        tax_payable = 9400 + (taxable_income * tax_rate)
        category = 'G'
    elif taxable_income <= 600000:
        tax_rate = 0.26
        tax_payable = 84400 + (taxable_income * tax_rate)
        category = 'H'
    elif taxable_income <= 2000000:
        tax_rate = 0.28
        tax_payable = 136400 + (taxable_income * tax_rate)
        category = 'I'
    else:
        tax_rate = 0.30
        tax_payable = 528400 + (taxable_income * tax_rate)
        category = 'J'

    print('\n===== Tax Summary =====')
    print(f"Tax (Year): {tax_year}")
    print(f"Gross Income (RM): {income}")
    print(f"Taxable Income (RM): {taxable_income}")
    print(f"Income Tax Category: Category {category}")
    print(f"Tax Payable (RM): {round(tax_payable, 2)}")
    print(f"Total Tax Relief (RM): {total_relief}")

    return reliefs, total_relief, round(tax_payable, 2)
