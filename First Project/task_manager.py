from datetime import date
from datetime import datetime

# For added readability in the terminal
separator = "--------------------------------------------"


def validate_user(user_list, username, password):
    """Validates the username and password of users from data in
    user_list.

    Parameters:
    user_list: A dictionary with usernames as key and passwords as
    values.
    username: The username to validate
    password: The password to validate

    Returns:
    bool: True if username and password match, otherwise False.
    """

    if username in user_list:
        if user_list[username] == password:
            return True
        else:
            print("Password is incorrect")
        return False

    else:
        print("Username not found.")
        return False


def load_user_data(filename):
    """
    Load user data from a specified file and return it as a dictionary.

    Parameters:
    filename (str): The name of the file to read from.

    Returns:
    dict: A dictionary with usernames as keys and passwords as values.
    """
    user_list = {}
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                user, password = line.strip().split(",")
                user_list[user.strip()] = password.strip()

    except FileNotFoundError:
        print(separator)
        print(f'Error. "{filename}" not found')
        print("Cannot proceed with login")
        print(separator)
        exit()

    return user_list


def date_format(date):
    """Takes date from datetime module and converts format to ddmmyy
    Parameters
    a: date in yyyymmdd format

    Output
    date in ddmmyy format"""
    formatted_date = date.strftime("%d %b %y")
    return formatted_date


def get_due_date():
    """
    Prompt the user for a task due date in 'DD/MM/YY' format and
    return it as a datetime object.

    Returns:
    datetime: The user-provided date as a datetime object.
    """
    while True:
        user_input = input("Enter task due date (DD/MM/YY): ")
        try:
            # Parse the user input to a datetime object
            user_date = datetime.strptime(user_input, "%d/%m/%y")
            # Change to match format in tasks.txt
            user_date = user_date.strftime("%d %b %y")
            return user_date

        except ValueError:
            print("Invalid date format. Please enter the date as DD/MM/YY.")


def get_valid_input(prompt):
    """Prevents user from using a comma in input."""
    while True:
        user_input = input(prompt)
        if "," in user_input:
            print("Invalid input. Commas are not allowed. Please try again.")
        else:
            return user_input


def replace_commas(input_string):
    """Replaces commas with |"""
    return input_string.replace(",", "|")


def data_count(file_path):
    """Count the number of non-empty lines in a text file
    Parameters:
    file_path: The path to the text file
    Returns:
    The number of non-empty lines (int)
    """
    count = 0
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():
                    count += 1
        return count

    except FileNotFoundError:
        print(separator)
        print(f"{file_path} not found")
        print(separator)
        return 0


def get_tasks(file_path):
    """Reads tasks from a file and prints them
    Parameter:
    file_path: path to tasks file
    """
    try:
        with open("tasks.txt", "r") as t:
            for line in t.readlines():
                (
                    user,
                    title,
                    description,
                    current_date,
                    due_date,
                    completed,
                ) = [field.strip() for field in line.strip().split(",")]

                print(separator)
                print(f"{'Task:':<20}{title}")
                print(f"{'Assigned to:':<20}{user}")
                print(f"{'Date assigned:':<20}{current_date}")
                print(f"{'Due date:':<20}{due_date}")
                print(f"{'Task Complete?':<20}{completed}")
                print(f"{'Task description:':<20}{description}")
            print(separator)

    except FileNotFoundError:
        print(separator)
        print('Error. "tasks.txt" not found')
        print(separator)


def get_user_tasks(file_path):
    """Reads tasks from a file and prints tasks assigned to the current
    user.
    Parameter:
    file_path: path to tasks file
    """
    try:
        with open("tasks.txt", "r") as t:
            for line in t.readlines():
                (
                    user,
                    title,
                    description,
                    current_date,
                    due_date,
                    completed,
                ) = [field.strip() for field in line.strip().split(",")]
                if user == username:
                    print(separator)
                    print(f"{'Task:':<20}{title}")
                    print(f"{'Assigned to:':<20}{user}")
                    print(f"{'Date assigned:':<20}{current_date}")
                    print(f"{'Due date:':<20}{due_date}")
                    print(f"{'Task Complete?':<20}{completed}")
                    print(f"{'Task description:':<20}{description}")
            print(separator)

    except FileNotFoundError:
        print(separator)
        print('Error. "tasks.txt" not found')
        print(separator)


def add_task_to_file(
    task_user, task_title, task_desc, task_due, file_path="tasks.txt"
):
    """Appends a task to the specified file."""
    current_date = date_format(date.today())
    task_data = (
        f"{task_user}, {task_title}, {task_desc}, "
        f"{current_date}, {task_due}, No \n"
    )
    try:
        with open(file_path, "a") as file:
            file.write(task_data)
            print(separator)
            print("Task successfully added!")

    except FileNotFoundError:
        print(separator)
        print(f'Error. "{file_path}" not found')
        print(separator)


def new_task(username_list):
    """Main function to assign tasks to users."""
    while True:
        task_user = input("Please assign the task to a user: ")
        if task_user not in username_list:
            print("User does not exist. Register user before assigning task")
            while True:
                menu_break = input("Revert to main menu? (Yes/No): ").lower()
                if menu_break == "yes":
                    return  # Exit the function to revert to main menu
                elif menu_break == "no":
                    break  # Break inner loop to re-prompt for user
                else:
                    print(separator)
                    print("Invalid input. Try again")
                    print(separator)
        else:
            task_title = get_valid_input("Please input title of task: ")
            input_desc = input("Please input description of task: ")
            task_desc = replace_commas(input_desc)
            task_due = get_due_date()
            add_task_to_file(task_user, task_title, task_desc, task_due)
            break


def admin_statistics(username):
    """Check user is admin and then displays number of users on
    user.txt and number of tasks on tasks.txt.

    Parameter:
    username: The current user logged into the programme.
    """
    if username != "admin":
        print(separator)
        print("You must be logged in as admin to access this section")
        print(separator)

    else:
        count_users = data_count("user.txt")
        count_tasks = data_count("tasks.txt")
        # Should count total tasks and number still incomplete
        print(separator)
        print(f"{'Number of users: ':<15}{count_users}")
        print(f"{'Number of tasks: ':<15}{count_tasks}")
        print(separator)


def add_user(username):
    """Checks if user is admin before registering new user

    Parameter:
    username: The current user logged in
    """
    if username != "admin":
        print(separator)
        print("Only admin is allowed to register new users.")

    else:
        while True:
            new_username = get_valid_input(("Pleas enter new username: "))
            if new_username in user_list:
                print("username already registered.")

            else:
                break

        while True:
            # Gets new password without commas.
            print(separator)
            new_password = get_valid_input(("Please enter new password: "))
            new_password_check = input("Please reenter password: ")
            if new_password != new_password_check:
                print("Passwords do not match. Please try again")
            else:
                break
        # Adds new username and password to user.txt
        try:
            with open("user.txt", "a") as file:
                file.write(f"{new_username}, {new_password}\n")
        except FileNotFoundError:
            print('Error "user.txt" not found')


def display_menu(username):
    """Checks username and displays menu of options. "admin" has an
    extra options on their menu.
    Parameter:
    username: Current logged in user.
    """
    if username != "admin":
        menu = input(
            "Select one of the following options: \n"
            "r - register a user \n"
            "a - add task \n"
            "va - view all tasks \n"
            "vm - view my tasks \n"
            "e - exit \n"
            ": "
        ).lower()

    else:
        menu = input(
            "Select one of the following options: \n"
            "r - register a user \n"
            "a - add task \n"
            "va - view all tasks \n"
            "vm - view my tasks \n"
            "s - view statistics \n"
            "e - exit \n"
            ": "
        ).lower()
    return menu


# Gets data for login
user_list = load_user_data("user.txt")

# Login section
while True:
    print(separator)
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if validate_user(user_list, username, password):
        print(separator)
        print("Login successful")
        break
    else:
        print("Login failed. Please try again")

# Provides menu - Requires username as admin has extra option.
while True:
    print(separator)
    menu = display_menu(username)

    # Registers new user - must be logged in as admin
    if menu == "r":
        add_user(username)

    # Adds new task and assigns to user on user_list.
    elif menu == "a":

        user_list = load_user_data("user.txt")
        username_list = list(user_list.keys())

        print(separator)
        new_task(username_list)

    # Displays all tasks on tasks.txt
    elif menu == "va":
        get_tasks("tasks.txt")

    # Displays tasks on tasks.txt which are assigned to current user
    elif menu == "vm":
        get_user_tasks("tasks.txt")

    # Shows statistics of number of users and tasks - Admin only
    elif menu == "s":
        admin_statistics(username)

    # Exits the programme
    elif menu == "e":
        print(separator)
        print("Successfully logged out")
        print("Goodbye!!!")
        print(separator)
        exit()

    # Invalid menu input
    else:
        print("You have entered an invalid input. Please try again")
