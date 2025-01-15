import sqlite3

db = sqlite3.connect("ebookstore.db")

cursor = db.cursor()

separator = "------------------------------------"


def new_book():
    """
    Adds a new book to the database.

    Prompts the  user to manually enter the title, author, and stock
    quantity.
    """

    print(separator)
    while True:

        title = input(
            "Please enter title of the book (or leave blank to return to menu): "
        )
        if title.lower() == "":
            break
        else:
            author = input("Please enter author of book: ")
            while True:
                try:
                    stock_qty = int(input("Please enter stock quantity: "))
                    cursor.execute("""SELECT MAX(id) FROM book""")
                    id = cursor.fetchone()[0] + 1
                    cursor.execute(
                        """INSERT INTO book(id, title, author, qty)
                            VALUES (?,?,?,?)""",
                        (id, title, author, stock_qty),
                    )
                    db.commit()
                    print(separator)
                    print(
                        f"New book id {id}: {title} by"
                        f"{author} ({stock_qty}) Successfully added!"
                    )
                    print(separator)
                    break

                except ValueError:
                    print("Please enter stock value as a whole number.")


def menu():
    """Shows user the menu of options"""
    print(separator)
    print("MENU")
    print(separator)
    print("Please select from the following options")
    print("n - Enter new book")
    print("u - Update book information")
    print("d - Delete a book from the system")
    print("s - Search the system for a book")
    print("e - Exit")
    print(separator)


def menu_input():
    """Takes menu input and starts appropriate function."""
    while True:

        selection = input("Menu selection: ").lower()

        if selection == "e":
            print(separator)
            print("Goodbye!")
            break

        match selection:
            case "n":
                pass
            case "u":
                pass
            case "d":
                pass
            case "s":
                pass
            case _:
                print(separator)
                print("Input not recognised, please try again.")


def edit_menu():
    """Options menu for the edit section."""
    print("What would you like to edit?")
    print("t - Edit title")
    print("a - Edit author")
    print("q - Edit stock quantity")
    print("e - Exit")
    menu_input = input("Please enter selection: ").lower()
    return menu_input


def qty_menu():
    """
    Prints menu and returns input.

    Prints the menu options, gets user's input for their choice, and
    returns the selection.
    """
    print("What would you like to do?")
    print("a - Add stock")
    print("r - Remove stock")
    print("s - Set stock level")
    print("exit - return to main menu")
    menu_input = str(input("Please enter selection: ")).lower()
    return menu_input


def confirm_input(prompt):
    """
    Confirms prompt is correct.

    Allows user to check and confirm the prompt is correct and they want
    to proceed.

    Parameter:
        prompt (str): The string which is to be confirmed by the user.
    """
    while True:
        user_input = input(prompt)
        check = input(f"{user_input} - Is this correct? (yes/no): ").lower()

        if check == "yes":
            return user_input
        elif check == "no":
            print(separator)
            print("Please try again")
        else:
            print(separator)
            print("Invalid response. Please enter 'yes' or 'no'.")


def change_qty(id_to_edit, qty_change, operation, cursor, db):
    """
    Updates the quantity of a book on the database.

    Parameters:
        id_to_edit (int): The ID of book on database to edit.
        qty_change (int): The quantity to add, subtract or set as new value.
        operation (str): What change is to be done to the current quantity,
                        either 'add', 'subtract' or 'set'.
        cursor (sqlite3.cursor): The SQLite3 cursor object.
        db (sqlite3.connection): The SQLite3 database connection object.
    """

    try:
        cursor.execute("SELECT qty FROM book WHERE id=?", (id_to_edit,))
        current_qty = cursor.fetchone()[0]

        if operation == "add":
            new_qty = current_qty + qty_change
        elif operation == "subtract":
            new_qty = current_qty - qty_change
        elif operation == "set":
            new_qty = qty_change

        cursor.execute(
            "UPDATE book SET qty = ? WHERE id = ?", (new_qty, id_to_edit)
        )
        db.commit()
        print(separator)
        print("Quantity successfully updated")

    except sqlite3.Error as e:
        print(separator)
        print(f"An error occured: {e}")


def new_info(cursor, db, column, id_to_edit):
    """
    Updates title or author of book on database.

    Parameters:
        cursor (sqlite3.cursor): The SQLite3 cursor object.
        db (sqlite3.connection): The SQLite3 database connection object.
        column (str): Which attribute to update in the database,
                    either title or author.
        id_to_edit (int): The ID of the book to be edited.
    """
    while True:
        updated_info = input(f"Please enter new {column}: ")
        print(separator)
        confirm_update = input(
            f"{updated_info} - Is this correct? (Yes/No): "
        ).lower()
        print(separator)
        if confirm_update == "yes":
            try:
                query = f"UPDATE book SET {column} = ? WHERE id = ?"
                cursor.execute(
                    query,
                    (updated_info, id_to_edit),
                )
                db.commit()
                print(f"{column} Successfully changed!")
                break
            except sqlite3.Error as e:
                print(separator)
                print(f"An error has occured: {e}")
        elif confirm_update == "no":
            print(separator)
            print("Please try again.")
        else:
            print(separator)
            print("Input not recognised. Please type 'Yes' or 'No'")


def new_quantity(cursor, db, id_to_edit):
    """
    Changes quantity of book on database.

    Allows user to edit the stock quantity of a book on the database
    by selecting using book ID.

    Parameters:
        cursor (sqlite3.cursor): The SQLite3 cursor object.
        db (sqlite3.connection): The SQLite3 database connection object.
        id_to_edit (int): The ID of the book to be edited.
    """
    cursor.execute("SELECT qty FROM book WHERE id = ?", (id_to_edit,))
    current_qty = cursor.fetchone()[0]
    print(f"Current stock level: {current_qty}")
    while True:
        selection = qty_menu()
        if selection == "a":
            qty_change = int(input("What quantity would you like to add? : "))
            change_qty(id_to_edit, qty_change, "add", cursor, db)
            break

        elif selection == "r":
            qty_change = int(
                input("What quantity would you like to remove? : ")
            )
            change_qty(
                id_to_edit,
                qty_change,
                "subtract",
                cursor,
                db,
            )
            break

        elif selection == "s":
            qty_change = int(input("Please set new stock quantity : "))
            change_qty(id_to_edit, qty_change, "set", cursor, db)

        elif selection == "exit":
            break


def get_from_id(cursor):
    """
    Enter book ID and returns full details.

    Prompts user to enter a book ID and returns the title, author and
    quantity in stock from the database.

    Parameter:
        cursor (sqlite3.cursor): The database cursor used to execute SQL
        commands.

    Returns:
        tuple: A tuple containing (title, author, id) of the book.
    """
    while True:
        id_input = input(
            "Please enter book ID (to return to main menu type 'exit') : "
        )
        if id_input.lower() == "exit":
            return

        id_to_edit = int(id_input)
        cursor.execute(
            """SELECT title, author, id FROM book WHERE id=?""", (id_to_edit,)
        )
        selected_book = cursor.fetchone()

        if selected_book is None:
            print(separator)
            print("Error. ID not recognised.")
        else:
            return selected_book


def delete_menu():
    """
    Provides the user with a menu of options for selecting a book to
    delete by database ID or book title.

    Returns:
        str: The selection from the menu.
    """
    print("How would you like to select book for deletion: ")
    print("id - book ID")
    print("t - Book title")
    print("exit - return to previous menu")
    print(separator)
    menu_input = input("Please enter selection: ").lower()
    return menu_input


def search(cursor):
    """
    Performs a search on the database.

    Searches the database for user input to partially match either the
    title or author. Only displays a maximum of 10 results.

    Parameter:
        cursor (sqlite3.Cursor): The database cursor used to execute SQL
        commands.
    """
    while True:
        search_term = input("(Type exit to return)\nEnter search : ")
        if search_term == "exit":
            break
        else:
            pass
        counter = 0
        cursor.execute(
            "SELECT * FROM book WHERE title LIKE ? OR author LIKE ? LIMIT 10",
            ("%" + search_term + "%", "%" + search_term + "%"),
        )
        print(separator)
        for row in cursor.fetchall():
            id, title, author, qty = row
            print(f"ID: {id}. {title} by {author} ({qty})")
            counter += 1

        if counter == 0:

            print("No results found.")
            print(separator)

        elif counter > 0 and counter < 10:
            print(separator)
            print(f"Displaying {counter} results.")
            print(separator)
        else:
            print(separator)
            print("Displaying first 10 results only.")
            print(separator)

        cont_search = input("Would you like to search again? (yes/no): ")
        print(separator)
        if cont_search.lower() == "yes":
            pass
        elif cont_search.lower() == "no":
            break
        else:
            print("input not recognised. Please type 'yes' or 'no'")


def delete_book(db, cursor):
    """
    Allows user to delete a book from the system.

    User will be prompted to find book by either id or title, then
    confirm the selection is correct before deleting from the database.

    Parameters:
        db (sqlite3.Connection): The SQLite3 database connection object.
        cursor (sqlite3.Cursor): The database cursor used to execute SQL
        commands.
    """
    while True:
        # Menu for using id or title to select book
        print(separator)
        selection = delete_menu()
        print(separator)
        if selection == "id":
            selected_book = get_from_id(cursor)
            # Breaks loop if nothing found
            if selected_book == None:
                break
            else:
                result_title, result_author, id_to_edit = selected_book

            print(f"You want to delete '{result_title} by {result_author}'?: ")
            confirm = input("Continue? (yes/no): ")
            if confirm.lower() == "no":
                break
            elif confirm.lower() == "yes":
                cursor.execute("DELETE FROM book WHERE id=?", (id_to_edit,))
                db.commit()
                print(separator)
                print("Book successfully deleted!")
                break

        elif selection == "t":
            title = input("Please enter the title of the book: ")
            cursor.execute(
                "SELECT title, author FROM book WHERE title LIKE ?",
                (title + "%",),
            )
            selected_book = cursor.fetchone()
            try:
                del_title, del_author = selected_book

                print(f"You want to delete '{del_title} by {del_author}'?: ")
                confirm = input("Continue? (yes/no): ")

                if confirm.lower() == "no":
                    break
                elif confirm.lower() == "yes":
                    cursor.execute(
                        "DELETE FROM book WHERE title=?", (del_title,)
                    )
                    db.commit()
                    print(separator)
                    print("Book successfully deleted!")
                    break

            except TypeError:
                print("Error. Cannot find book")

            except sqlite3.Error as e:
                print(f"An Error has occured: {e}")

        elif selection == "exit" or "e":
            break

        else:
            print("Input not recognised. Please try again")


def update_book(db, cursor):
    """
    Manually updates book title, author or stock quantity by allowing
    user to select book by ID

    Parameters:
        db (sqlite3.Connection): The SQLite3 database connection object.
        cursor (sqlite3.Cursor): The database cursor used to execute SQL
        commands.
    """
    while True:
        try:
            print(separator)
            selected_book = get_from_id(cursor)
            if selected_book == None:
                break
            else:
                result_title, result_author, id_to_edit = selected_book

            print(f"You want to edit '{result_title} by {result_author}'?")
            print(separator)
            confirm = input("Continue? (yes/no): ")
            print(separator)
            if confirm.lower() == "no":
                break
            elif confirm.lower() == "yes":
                while True:
                    edit_selection = edit_menu().lower()
                    if edit_selection == "t":
                        new_info(cursor, db, "title", id_to_edit)

                    elif edit_selection == "a":
                        new_info(cursor, db, "author", id_to_edit)

                    elif edit_selection == "q":
                        new_quantity(cursor, db, id_to_edit)

                    elif edit_selection == "e" or "exit":
                        break

                    else:
                        print("Input not recognised. Please try again.")

            else:
                print("Input not recognised. Please type 'yes' or 'no'.")

        except ValueError:
            print("Error invalid format")

        except TypeError:
            print("Error. ID not recognised.")


# Create table
try:
    cursor.execute(
        """CREATE TABLE book(id INTEGER PRIMARY KEY, title, author, qty 
        INTEGER);"""
    )
    db.commit()
# Skips if table "book" already exists
except sqlite3.OperationalError:
    pass

# Current stock to be added to db
stock = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch, and the Wardrobe", "C.S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 40),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
]

# Adding stock to db
try:
    cursor.executemany(
        """INSERT INTO book (id, title, author, qty)
        VALUES (?,?,?,?)""",
        stock,
    )
    db.commit()
# Skips if already populated
except sqlite3.IntegrityError:
    pass

# -------- MAIN SECTION ---------
while True:
    menu()
    selection = input("Menu selection: ").lower()

    if selection == "e" or selection == "exit":
        print(separator)
        db.close()
        print("Goodbye!")
        print(separator)
        break

    match selection:
        # Add new book
        case "n":
            new_book()
        # Update book details
        case "u":
            update_book(db, cursor)
        # Delete book from system
        case "d":
            delete_book(db, cursor)

        # Search for book
        case "s":
            search(cursor)

        case _:
            print(separator)
            print("Input not recognised, please try again.")
