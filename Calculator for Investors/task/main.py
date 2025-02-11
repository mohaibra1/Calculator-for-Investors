import sqlite3
import csv


def create_database():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        sector TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS financial (
        ticker TEXT PRIMARY KEY,
        ebitda REAL,
        sales REAL,
        net_profit REAL,
        market_price REAL,
        net_debt REAL,
        assets REAL,
        equity REAL,
        cash_equivalents REAL,
        liabilities REAL
    )''')

    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0:
        with open('companies.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            data = [(row[0], row[1], row[2] if row[2] else None) for row in reader]
            cursor.executemany("INSERT INTO companies VALUES (?, ?, ?)", data)

        with open('financial.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            data = [(row[0],) + tuple(float(row[i]) if row[i] else None for i in range(1, 10)) for row in reader]
            cursor.executemany("INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

# # write your code here
def main_menu():
    while True:
        print("\nMAIN MENU")
        print("0 Exit")
        print("1 CRUD operations")
        print("2 Show top ten companies by criteria")

        option = input("\nEnter an option:\n ")

        if option == "0":
            print("Have a nice day!")
            break
        elif option == "1":
            crud_menu()
        elif option == "2":
            top_ten_menu()
        else:
            print("Invalid option!")


def crud_menu():
    while True:
        print("\nCRUD MENU")
        print("0 Back")
        print("1 Create a company")
        print("2 Read a company")
        print("3 Update a company")
        print("4 Delete a company")
        print("5 List all companies")

        option = input("\nEnter an option:\n ")

        if option == "0":
            break
        elif option == "1":
            create_company()
            break
        elif option == "2":
            read_company()
            break
        elif option == "3":
            update_company()
            break
        elif option == "4":
            delete_company()
            break
        elif option == "5":
            list_companies()
            break
        else:
            print("Invalid option!")


def top_ten_menu():
    while True:
        print("\nTOP TEN MENU")
        print("0 Back")
        print("1 List by ND/EBITDA")
        print("2 List by ROE")
        print("3 List by ROA")

        option = input("\nEnter an option:\n ")

        if option == "0":
            break
        elif option in {"1", "2", "3"}:
            print("Not implemented!")
            main_menu()
            exit()
        else:
            print("Invalid option!")


def create_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    ticker = input("Enter ticker (in the format 'Moon'): ")
    name = input("Enter company (in the format 'Moon Corp'): ")
    sector = input("Enter industries (in the format 'Technology'): ")

    ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    sales = float(input("Enter sales (in the format '987654321'): "))
    net_profit = float(input("Enter net profit (in the format '987654321'): "))
    market_price = float(input("Enter market price (in the format '987654321'): "))
    net_debt = float(input("Enter net debt (in the format '987654321'): "))
    assets = float(input("Enter assets (in the format '987654321'): "))
    equity = float(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = float(input("Enter liabilities (in the format '987654321'): "))

    cursor.execute("INSERT INTO companies VALUES (?, ?, ?)", (ticker, name, sector))
    cursor.execute("INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents,
                    liabilities))

    conn.commit()
    conn.close()
    print("Company created successfully!")


def read_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    # name = input("Enter company name: ")
    # cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ("%" + name + "%",))
    # companies = cursor.fetchall()
    # if not companies:
    #     print("Company not found!")
    # else:
    #     for index, company in enumerate(companies):
    #         print(f"{index} {company[1]}")
    # conn.close()
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    for idx, company in enumerate(companies):
        print(f"{idx} {company[1]}")

    company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    cursor.execute("SELECT * FROM financial WHERE ticker = ?", (ticker,))
    financial = cursor.fetchone()

    # Use correct fields for calculations
    ebitda = financial[1]
    sales = financial[2]
    net_profit = financial[3]
    market_price = financial[4]
    net_debt = financial[5]
    assets = financial[6]
    equity = financial[7]
    cash_equiv = financial[8]
    liabilities = financial[9]

    pe = round(market_price / net_profit, 2) if net_profit else None
    ps = round(market_price / sales, 2) if sales else None
    pb = round(market_price / assets, 2) if equity else None
    nd_ebitda = None if ebitda is None or ebitda == 0 else round(net_debt / ebitda, 2)
    roe = round(net_profit / equity, 2) if equity else None
    roa = round(net_profit / assets, 2) if assets else None
    la = round(liabilities / assets, 2) if assets else None

    # Printing results
    print(f"{ticker} {companies[company_number][1]}")
    print(f"P/E = {pe}")
    print(f"P/S = {ps}")
    print(f"P/B = {pb}")
    print(f"ND/EBITDA = {nd_ebitda}")
    print(f"ROE = {roe}")
    print(f"ROA = {roa}")
    print(f"L/A = {la}")


def update_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    # ticker = input("Enter company name: ")
    #
    # cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + ticker + '%',))
    # company = cursor.fetchall()
    # if not company:
    #     print("Company not found!")
    # else:
    #     for index, company in  enumerate(company):
    #         print(f"{index} {company[1]}")
    #     number = input("Enter company number: ")
    #     ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    #     sales = float(input("Enter sales (in the format '987654321'): "))
    #     net_profit = float(input("Enter net profit (in the format '987654321'): "))
    #     market_price = float(input("Enter market price (in the format '987654321'): "))
    #     net_debt = float(input("Enter net debt (in the format '987654321'): "))
    #     assets = float(input("Enter assets (in the format '987654321'): "))
    #     equity = float(input("Enter equity (in the format '987654321'): "))
    #     cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    #     liabilities = float(input("Enter liabilities (in the format '987654321'): "))
    #     new_name = input("Enter company name: ")
    #     new_sector = input("Enter new industry: ")
    #     cursor.execute("UPDATE companies SET name = ?, sector = ? WHERE ticker = ?", (new_name, new_sector, ticker))
    #     conn.commit()
    #     print("Company updated successfully!")
    # conn.close()
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    for idx, company in enumerate(companies):
        # Only output index and company name
        print(f"{idx} {company[1]}")

    company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    # New financial data
    ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    sales = float(input("Enter sales (in the format '987654321'): "))
    net_profit = float(input("Enter net profit (in the format '987654321'): "))
    market_price = float(input("Enter market price (in the format '987654321'): "))
    net_debt = float(input("Enter net debt (in the format '987654321'): "))
    assets = float(input("Enter assets (in the format '987654321'): "))
    equity = float(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = float(input("Enter liabilities (in the format '987654321'): "))

    # Update financial table
    cursor.execute('''UPDATE financial SET ebitda=?, sales=?, net_profit=?, market_price=?, 
                          net_debt=?, assets=?, equity=?, cash_equivalents=?, liabilities=? 
                          WHERE ticker=?''',
                   (ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities,
                    ticker))
    conn.commit()
    print("Company updated successfully!")

def delete_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    # Display only the company names, not the tickers
    for idx, company in enumerate(companies):
        print(f"{idx} {company[1]}")  # company[1] is the name

        company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    # Delete from companies and financial tables
    cursor.execute("DELETE FROM companies WHERE ticker=?", (ticker,))
    cursor.execute("DELETE FROM financial WHERE ticker=?", (ticker,))
    conn.commit()
    print("Company deleted successfully!")

def list_companies():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM companies ORDER BY ticker")
    # companies = cursor.fetchall()
    # conn.close()
    # print("\nCOMPANY LIST")
    # for company in companies:
    #     print(f"{company[0]} {company[1]} {company[2]}")
    print("COMPANY LIST")
    cursor.execute(
        "SELECT ticker, name, sector FROM companies ORDER BY ticker")  # Exclude the ticker from the SELECT statement
    for company in cursor.fetchall():
        # Ensure only the company name and sector are printed
        print(f"{company[0]} {company[1]} {company[2]}")


if __name__ == "__main__":
    create_database()
    print("Welcome to the Investor Program!")
    main_menu()
