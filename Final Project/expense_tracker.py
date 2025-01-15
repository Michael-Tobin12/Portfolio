import sqlite3
from datetime import datetime
import re

separator = "---------------------------------"


class expense_db:
    """
    A class used to represent a connection to the database.

    Attributes
    ----------
    connection : sqlite3.Connection
    a connection to the database
    cursor : sqlite3.Cursor
    a cursor for the database connection
    Methods
    -------
    create_table(table_name: str) -> None
        Creates a table in the database if it does not exist.
    add_to_table(table_name: str, values: list) -> None
        Adds a transaction record to the specified table.
    close_connection() -> None
        Closes the database connection.
    commit() -> None
        Commits the changes to the database.
    get_next_id(table_name: str, id_column: str) -> int
        Returns the next transaction ID for the specified table.
    view_all(table_name: str) -> None
        Prints all records from the specified table ordered by
        transaction date.
    view_by_cat(table_name: str, dictionary: dict) -> None
        Prints all records from the specified table filtered by category
        and ordered by transaction date.
    show_budgets() -> None
        Prints all budget records.
    select_budget() -> None
        Prompts the user to amend a budget.
    search_expenses() -> tuple
        Searches for and returns an expense category record.
    show_budget_cats() -> None
        Prints all budget categories.
    disp_budget_by_cat(self) -> None
        Displays the budget information for a selected category.
    budget_search_by_cat(self) -> None
        Searches and displays budget information by category.
    new_goal(self, goal_name, target_amount, saved_amount, deadline)
        -> None
        Creates a new savings goal in the database.
    add_to_goal(self) -> None
        Adds funds to an existing savings goal.
    """

    def __init__(self, db_name):
        """Initialised the database connection.

        Parameters:
        db_name (str): The name of the database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name):
        """
        Creates a table in the database if it does not exist.

        Parameters:
        table_name (str): The name of the table to be created.
        """
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        TransactID int PRIMARY KEY,
        TransactName VARCHAR(20),
        TransactDate DATE,
        Amount DECIMAL(10, 2), 
        Category VARCHAR(20) );"""
        self.cursor.execute(create_table_sql)
        self.commit()

    def add_to_table(self, table_name, values):
        """
        Adds a transaction record to the specified table.

        Parameters:
        table_name (str): The name of the table.
        values (list): A list of the transaction details to be added.
        """
        """Adds list of variables to a table."""
        query = f"""INSERT INTO {table_name} (TransactID, TransactName,
        TransactDate, Amount, Category)VALUES (?, ?, ?, ?, ?);"""
        self.cursor.execute(query, values)
        print(separator)
        print("Transaction successfully added!")
        self.commit()

    def close_connection(self):
        """Closes the database connection."""
        self.connection.close()

    def commit(self):
        """Commit the changes to the database."""
        self.connection.commit()

    def get_next_id(self, table_name, id_column):
        """
        Returns the next transaction ID for the specified table.

        Arguments:
            table_name -- The name of the table.
            id_column -- The column name for the ID.

        Returns:
            int: The next transaction ID.
        """
        query = f"SELECT MAX({id_column}) FROM {table_name};"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            last_id = result[0] + 1 if result[0] is not None else 1
            return last_id
        except sqlite3.Error as e:
            print(f"An error has occurred: {e}")
            return None

    def view_all(self, table_name):
        """
        Prints all records from the specified table ordered by
        transaction date.

        Arguments:
            table_name -- The name of the table
        """
        query = f"SELECT * FROM {table_name} ORDER BY TransactDate;"
        headers = [
            "ID",
            "TransactName",
            "TransactDate",
            "GBP",
            "Category",
        ]
        print("{:<5} {:<20} {:<10} {:>8}    {:<15}".format(*headers))
        try:
            self.cursor.execute(query)
            for result in self.cursor.fetchall():
                id, name, date, amount, category = result
                print(
                    f"{id:<5} {name:<20} {date:<10} {amount:>10}    {category:<15}".format(
                        *result
                    )
                )
        except sqlite3.Error as e:
            print(f"An error has occurred: {e}")
            return None

    def view_by_cat(self, table_name, dictionary):
        """
        Prints all records from the specified table filtered by category
        and ordered by transaction date.

        Arguments:
            table_name -- The name of the table.
            dictionary -- A dictionary of categories.
        """
        category_selection = select_category(
            dictionary, "Please select a category to view: "
        )
        query = f"SELECT * FROM {table_name} WHERE Category = '{category_selection}' ORDER BY TransactDate;"
        headers = [
            "ID",
            "TransactName",
            "TransactDate",
            "GBP",
            "Category",
        ]
        print(separator)
        print("{:<5} {:<20} {:<15} {:<10} {:<9}".format(*headers))
        try:
            self.cursor.execute(query)
            for result in self.cursor.fetchall():
                id, name, date, amount, category = result

                print(
                    f"{id:<5} {name:<20} {date:<15} {amount:<10} {category:<9}".format(
                        *result
                    )
                )
        except sqlite3.Error as e:
            print(f"An error has occurred: {e}")
            return None

    def show_budgets(self):
        """Prints all budget records."""
        query = """SELECT * FROM budgets"""
        headers = [
            "ID",
            "TYPE",
            "CATEGORY",
            "BUDGET",
        ]
        print(separator)
        print("CURRENT BUDGETS")
        print(separator)
        print("{:<5} {:<10} {:<20} {:>12}".format(*headers))
        try:
            self.cursor.execute(query)
            for result in self.cursor.fetchall():
                id, cat_type, category, budget = result
                if budget == None:
                    budget = "No budget set"
                else:
                    pass
                print(
                    f"{id:<5} {cat_type:<10} {category:<25} {budget:<15}".format(
                        *result
                    )
                )
        except sqlite3.Error as e:
            print(f"An error has occurred: {e}")

    def select_budget(self):
        """Prompts user to amend a budget."""
        while True:
            results = db.search_expenses()
            try:
                id, category, budget = results
                confirm = (
                    input(f"Amend budget for {category}? (Yes/No): ")
                    .lower()
                    .strip()
                )
                if confirm == "yes" or confirm == "y":
                    try:
                        print(separator)
                        new_values = round(
                            float(
                                input("Please enter the new budget value: ")
                            ),
                            2,
                        )
                    except ValueError:
                        print("Please enter value as a number.")
                        continue
                query = """UPDATE Budgets SET budget = ? WHERE ID = ?;"""
                values = [new_values, id]
                self.cursor.execute(query, values)
                self.commit()
                print(separator)
                print("Budget successfully updated!")
                return
            except TypeError:
                pass

    def search_expenses(self):
        """
        Searches for and returns an expense category record.

        Returns:
            A tuple containing the ID, category, and budget of the
            record.
        """
        search_input = str(input("Please enter expense category: "))
        search_query = " SELECT * FROM budgets WHERE category LIKE ?"
        search_term = "%" + search_input + "%"
        self.cursor.execute(search_query, (search_term,))
        result = db.cursor.fetchone()
        if result:
            id, cat_type, category, budget = result
            if budget == None:
                budget = "No budget set"
            return id, category, budget
        else:
            print("No result found.")

    def show_budget_cats(self):
        """Prints all budget categories."""
        query = """SELECT ID, Category FROM budgets"""
        headers = [
            "ID",
            "CATEGORY",
        ]
        print(separator)
        print("Categories")
        print(separator)
        print("{:<5} {:<10}".format(*headers))
        try:
            self.cursor.execute(query)
            for result in self.cursor.fetchall():
                (
                    id,
                    category,
                ) = result
                print(f"{id:<3}{category:<25}".format(*result))
            print(separator)
        except sqlite3.Error as e:
            print(f"An error has occurred: {e}")

    def disp_budget_by_cat(self):
        """
        Displays the budget information for a selected category.

        Prompts the use to select a category by ID and prints the
        corresponding budget details.
        """
        self.show_budget_cats()
        cat_selection = input("Please enter ID of category to view: ")
        query = """SELECT * FROM budgets WHERE ID = ? """
        headers = [
            "ID",
            "TYPE",
            "CATEGORY",
            "BUDGET",
        ]
        self.cursor.execute(query, (cat_selection,))
        result = self.cursor.fetchone()
        if result:
            id, cat_type, category, budget = result
            if budget == None:
                budget = "No budget set"
            else:
                pass
            print(separator)
            print("{:<5} {:<10} {:<20} {:>12}".format(*headers))
            print(
                f"{id:<5} {cat_type:<10} {category:<25} {budget:<12}".format(
                    *result
                )
            )
            print(separator)
        else:
            print("No result for given ID.")

    def budget_search_by_cat(self):
        """
        Searches and displays budget information by category.

        Prompts the user to enter a category name, searches for matching
        records and prints the details of the first matching budget.
        """
        search_query = "SELECT * FROM budgets WHERE Category LIKE ?"
        headers = [
            "ID",
            "TYPE",
            "CATEGORY",
            "BUDGET",
        ]
        user_search = str(input("Category search: "))
        search_term = "%" + user_search + "%"
        self.cursor.execute(search_query, (search_term,))
        result = self.cursor.fetchone()
        if result:
            id, cat_type, category, budget = result
            if budget == None:
                budget = "No budget set"
            else:
                pass
            print(separator)
            print("{:<5} {:<10} {:<20} {:>12}".format(*headers))
            print(
                f"{id:<5} {cat_type:<10} {category:<25} {budget:<12}".format(
                    *result
                )
            )
            print(separator)
        else:
            print("No result for given ID.")

    def new_goal(self, goal_name, target_amount, saved_amount, deadline):
        """
        Creates a new savings goal in the database.

        Arguments:
            goal_name -- The name of the goal.
            target_amount -- The target amount to be saved.
            saved_amount -- The amount already saved towards the goal.
            deadline -- The deadline for achieving the goal.
        """
        query = """INSERT INTO Goals (goal, target_amount, saved_amount, deadline)
        VALUES (?, ?, ?, ?);
        """
        new_goal_values = goal_name, target_amount, saved_amount, deadline
        self.cursor.execute(query, new_goal_values)
        self.commit()

    def add_to_goal(self):
        """
        Adds funds to an existing savings goal.

        Prompts the user to select a goal and enter the amount to add.
        Updated the goal's saved amount in the database.
        """
        while True:
            result = search_goals()
            id, goal, target_amount, saved_amount, deadline = result
            confirm = (
                input(f"Do you want to add funds to '{goal}'?: ")
                .lower()
                .strip()
            )
            if confirm == "yes" or confirm == "y":
                try:
                    amount_to_add = float(
                        input("Please enter amount to add towards goal: £")
                    )
                    new_total = amount_to_add + saved_amount
                    add_query = """
                        UPDATE Goals SET saved_amount = ? WHERE ID = ?;
                        """
                    try:
                        self.cursor.execute(add_query, (new_total, id))
                        self.commit()
                        print("Goal updated!")
                        break
                    except sqlite3.Error as e:
                        print(f"Error: {e}")

                except ValueError:
                    print("Input must be a number.")

            elif confirm == "no" or confirm == "n":
                print("Please try search again.")
                # or print list of all goals?
            else:
                print("Input not recognised.")


def get_goal_name():
    """Prompts user to input name of new savings goal

    Returns:
        The name of the new savings goal.
    """
    while True:
        goal_name = (
            str(input("What are you saving for?: ")).strip().capitalize()
        )
        if len(goal_name) < 4:
            print(
                "Please enter at least 4 characters for the name of the goal."
            )
        else:
            return goal_name


def get_goal_target():
    """Prompts user to input the amount they wish to set as a target for
    the goal.

    Returns:
        The target amount of the goal.
    """
    while True:
        try:
            target_amount = float(input("How much would you like to save?: £"))
            if target_amount == 0:
                print("Target amount cannot be equal to zero.")
            elif target_amount < 0:
                print("Target amount cannot be a negative number.")
            else:
                return target_amount
        except ValueError:
            print("Target amount must be a number.")


def get_goal_saved():
    """Prompts the user to input the amount they have already saved
    towards the goal before logging on the app.

    Returns:
        The total amount already saved towards the goal.
    """
    while True:
        try:
            saved_amount = float(input("How much have you saved already?: £"))
            if saved_amount < 0:
                print("Saved amount cannot be less than zero.")
            else:
                return saved_amount
        except ValueError:
            print("Target amount must be a number.")


def get_goal_deadline():
    """Prompts the user to input a deadline for their savings goal.

    The user must input a date in the DD-MM-YYYY format to set a
    deadline for the savings goal.

    Returns:
        The deadline date for completing the goal.
    """
    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
    while True:
        deadline = input("Please enter the deadline (DD-MM-YYYY): ")
        if date_pattern.match(deadline):
            deadline_date = datetime.strptime(deadline, "%d-%m-%Y").date()
            formatted_date = deadline_date.strftime("%d-%m-%Y")
            return formatted_date
        else:
            print("Please enter date in the format DD-MM-YYYY.")


def savings_goal():
    """
    Creates a new savings goal by gathering user input for goal details.

    The function collects the name, target amount, amount already saved,
    and deadline for the savings goal from the user by calling
    respective functions: 'get_goal_name', 'get_goal_target',
    'get_goal_saved', and 'get_goal_deadline()'. It then uses these
    details to create a new goal entry in the database via the
    'db.new_goal' method.
    """
    goal_name = get_goal_name()
    target_amount = get_goal_target()
    saved_amount = get_goal_saved()
    deadline = get_goal_deadline()
    db.new_goal(goal_name, target_amount, saved_amount, deadline)


def search_goals():
    """
    Searches for a savings goal based on user input and returns the goal
    details.

    Prompts the user to enter a goal name, searches the 'Goals' table
    for matching records, and returns the details of the first matching
    goal. If not match is found it prints a message saying no results
    found.

    Returns:
        A tuple containing the goal ID, name, target amount, saved
        amount and deadline if a match is found.
    """
    goal_search_input = str(input("Please enter goal name: "))
    search_query = "SELECT * FROM Goals WHERE goal LIKE ?"
    goal_search_term = "%" + goal_search_input + "%"
    db.cursor.execute(search_query, (goal_search_term,))
    result = db.cursor.fetchone()
    if result:
        id, goal, target_amount, saved_amount, deadline = result
        return id, goal, target_amount, saved_amount, deadline
    else:
        print("No results found.")


def check_goal_progress():
    """
    Checks and displays the progress of a savings goal.

    Searches for a goal using the 'search_goals' function and prints the
    current status, including target amount, total saved, amount
    remaining, and percentage progress.
    """
    try:
        result = search_goals()
        id, goal, target_amount, saved_amount, deadline = result
        print(separator)
        print(f"Current goal: {goal}")
        print(f"Target amount: £{target_amount}")
        print(f"Total saved: £{saved_amount}")
        remaining_total = target_amount - saved_amount
        percentage_progress = saved_amount / target_amount * 100
        rounded_percentage = round(percentage_progress, 2)
        print(f"Amount remaining: £{remaining_total} ({rounded_percentage}%)")
        print(separator)
    except TypeError:
        pass


def get_date_input():
    """
    Gets transaction date in format DD-MM-YYYY.

    Gets user to input date of the transaction in DD-MM-YYYY format to be
    used with SQL.
    """
    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
    while True:
        date_str = input("Enter transaction date (DD-MM-YYYY): ")
        if date_pattern.match(date_str):
            try:
                date = datetime.strptime(date_str, "%d-%m-%Y")
                return date.strftime("%d-%m-%Y")
            except ValueError:
                print(
                    "Invalid date value. Please enter a valid date in DD-MM-YYYY format."
                )
        else:
            print(
                "Invalid date format. Please enter the date in DD-MM-YYYY format."
            )


def get_expense_data():
    """
    Gathers user input for an expense transaction and returns the data
    as a list.

    Prompts the user to enter the transaction name, date, amount, and
    category. The transaction ID is automatically generated.

    Returns:
        A list containing the transaction ID, name, date, amount and
        category.
    """
    id = db.get_next_id("expenses", "TransactID")
    name = input("Please enter name of transaction: ")
    date = get_date_input()
    amount = float(input("Please enter amount in GBP: "))
    rounded_amount = str(round(amount, 2))
    category = select_category(
        expense_cats, "Please select an expense category: "
    )
    values = [id, name, date, rounded_amount, category]
    return values


def get_income_data():
    """
    Gathers user input for an income transaction and returns the data as
    a list.

    Prompts the user to enter the transaction name, date, amount and
    category. The transaction ID is automatically generated.

    Returns:
        A list containing the transaction ID, name, date, amount and
        category.
    """
    id = db.get_next_id("income", "TransactID")
    name = input("Please enter name of transaction: ")
    date = get_date_input()
    amount = float(input("Please enter amount in GBP: "))
    rounded_amount = str(round(amount, 2))
    # Categories should be kep on a list and checked at input stage
    category = select_category(
        income_cats, "Please select an expense category: "
    )
    values = [id, name, date, rounded_amount, category]
    return values


def menu():
    """
    Displays the menu for the programs functions and prompts the user
    for a selection.

    Returns:
        The number corresponding to the user's menu selection.
    """
    print(separator)
    print("1. Add expense")
    print("2. View expenses")
    print("3. View expenses by category")
    print("4. Add income")
    print("5. View income")
    print("6. View income by category")
    print("7. Set budget for a category")
    print("8. View budget for a category")
    print("9. Set financial goals")
    print("10. View progress towards financial goals")
    print("11. Quit")
    print(separator)
    try:
        menu_choice = int(
            input(
                "Please input the number of the option you wish to use: "
            ).strip()
        )
        if menu_choice <= 0 or menu_choice > 11:
            print("Invalid option. Please try again.")
        else:
            return menu_choice

    except ValueError:
        print("Invalid entry. Choice must be a number.")


def select_category(dictionary, question_str):
    """Allows user to select expense or income category from list.

    Arguments:
        dictionary -- The dictionary containing the category options.
        question_str -- The prompt to display to the user.

    Returns:
        The selected category name.
    """
    print(separator)
    show_categories(dictionary)
    while True:
        try:
            user_input = int(input(f"{question_str}"))
            if (
                dictionary == expense_cats
                and user_input >= 0
                and user_input <= 15
            ):
                category_selection = dictionary[user_input]
                return category_selection
            elif (
                dictionary == income_cats
                and user_input >= 0
                and user_input <= 8
            ):
                category_selection = dictionary[user_input]
                return category_selection
            else:
                print("Error. Invalid selection.")
        except TypeError:
            print("Error. Input must be a number.")


def show_categories(dictionary):
    """
    Displays the available categories from a given dictionary.

    Arguments:
        dictionary -- The dictionary containing category options.
    """
    for index, category in dictionary.items():
        print(f"{index:>2}: {category}")


def show_income_categories():
    """Displays the available income categories."""
    for index, category in income_cats.items():
        print(f"{index:>2}: {category}")


def view_budget_by_cat():
    """
    Provides a menu for viewing budget information by category.

    Allows the user to select from showing all budgets, picking a
    category from a list, searching for a category or returning to the
    main menu.
    """
    while True:
        print("1. Show all budgets")
        print("2. Pick Category from list")
        print("3. Search for Category")
        print("4. Return to menu")
        print(separator)
        user_input = int(input("Please select option: "))
        if user_input == 4:
            break
        elif user_input == 1:
            db.show_budgets()
        elif user_input == 2:
            db.disp_budget_by_cat()
        elif user_input == 3:
            db.budget_search_by_cat()
        else:
            print("Input not recognised: Please select from menu.")


db = expense_db("expenses.db")

db.create_table("Income")
db.create_table("Expenses")


expense_cats = {
    0: "Housing",
    1: "Childcare",
    2: "Transportation",
    3: "Utilities",
    4: "Food & Household supplies",
    5: "Pets",
    6: "Savings & Investments",
    7: "Entertainment",
    8: "Healthcare",
    9: "Insurance",
    10: "Personal care",
    11: "Debt",
    12: "Gifts",
    13: "Donations",
    14: "Clothing",
    15: "Other",
}

income_cats = {
    0: "Salary",
    1: "Bonus, Commission, Tips",
    2: "Pension",
    3: "Government Benefits",
    4: "Rental Income",
    5: "Investment returns",
    6: "Gifts",
    7: "Child support",
    8: "Other",
}


# Create budget table
query = """CREATE TABLE IF NOT EXISTS Budgets (
    ID int PRIMARY KEY,
    TYPE VARCHAR(20),
    Category VARCHAR(20),
    Budget DECIMAL(10, 2)
    );"""
db.cursor.execute(query)
db.commit()

# Create Goal table
goal_query = """CREATE TABLE IF NOT EXISTS Goals (
ID INTEGER PRIMARY KEY,
goal TEXT,
target_amount REAL,
saved_amount REAL,
deadline TEXT
)"""
db.cursor.execute(goal_query)
db.commit()

# Populate budget table with expense categories.

try:
    index = 0
    budget_values = []
    for category in expense_cats.items():
        index += 1
        cat_type = "Expense"
        category_name = category[1]
        budget_values = [index, cat_type, category_name]
        query_add = (
            """INSERT INTO Budgets (ID, TYPE, Category) VALUES (?, ?, ?);"""
        )
        db.cursor.execute(query_add, budget_values)
        db.commit()
except sqlite3.IntegrityError:
    pass


#### MAIN SECTION ####

while True:
    selection = menu()
    # Closes connection to database and closes programme
    if selection == 11:
        print("Goodbye!")
        db.close_connection()
        exit()

    elif selection == 1:
        values = get_expense_data()
        db.add_to_table("expenses", values)

    elif selection == 2:
        print(separator)
        db.view_all("expenses")
    elif selection == 3:
        print(separator)
        print("VIEW EXPENSES BY CATEGORY")
        db.view_by_cat("expenses", expense_cats)
    elif selection == 4:
        print("Add income")
        values = get_income_data()
        db.add_to_table("Income", values)
    elif selection == 5:
        print(separator)
        db.view_all("income")
    elif selection == 6:
        print(separator)
        print("VIEW INCOME BY CATEGORY")
        db.view_by_cat("income", income_cats)
    elif selection == 7:
        print("Set budget for category")
        db.select_budget()
    elif selection == 8:
        print("View budget for category")
        view_budget_by_cat()
    elif selection == 9:
        print("Set financial goals")
        savings_goal()
    elif selection == 10:
        print("View progress towards financial goals")
        check_goal_progress()
