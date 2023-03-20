"""

The index corresponding to each already entered date has to be saved for each account. How can we do this?
When the user signs in to his account, the data from the file of his account is grabbed.
The first line in his file is his indexes corresponding to each already entered dates.
The rest of the file is the transactions.

To do:
> Add comments.
> Make the program more user-friendly.
> Make the transaction method functional (therefore the user can add or take money from his balance)
> Make it so the dates entered are saved, and that the transactions are saved.
> Then start working on categories
> Then start working on statistics.
"""
from tkinter import *
import json
from tkcalendar import Calendar
from datetime import *
#CURRENTLY WORKING ON SUBMIT TRANSACTION FUNCTIONALITY
# Loads all accounts (their usernames and passwords)
try:
    with open("accounts", "r") as file:
        data = file.readlines()
except Exception:
    print("Something went wrong!")

# The program tries to get each account's username and password from the accounts text file, to a dictionary variable.
try:
    account_details_json = json.loads(data[0])
    account_details = dict(account_details_json)
except IndexError:
    # If the text file is empty, an empty dictionary is created.
    account_details = dict()

# The program tries to get each account's balance from the accounts text file, to a dictionary variable.
try:
    balances_json = json.loads(data[1])
    balances = dict(balances_json)
except IndexError:
    # If the text file is empty, an empty dictionary is created.
    balances = dict()

user_data = [{500: "Food", 400: "Accessories"}]

main_menu_window = Tk()

# The current account whose data is being used, and manipulated.
current_account = StringVar()

# The line in the text file which is currently selected and will be manipulated.
selected_line = IntVar()

# The account which is currently signed in to.
selected_account = StringVar()


def check_date(date):
    # A list of all the dates which have already been entered / created before is created.
    dates_entered = [i for i in date_lines.values()]

    # The program checks if the date which has been chosen in the calendar has already been entered before
    if not dates_entered.__contains__(date):
        # If false, the new date is inserted into the lines variable.
        date_lines.update({len(date_lines): date})
        selected_line.set(len(date_lines) - 1)

        # Puts all the data in date_lines in the variable new_date_lines_json, in JSON format, as a string variable.
        new_date_lines_json = json.dumps(date_lines)

        # Saves the file (adds the corresponding dates and line numbers to the account's database file).
        with open(f"{selected_account.get()}.txt", "w") as file:
            file.truncate(0)
            file.write(new_date_lines_json)
    else:
        # If true, the program gets the index of the selected date in the lines variable,
        # and sets it to the selected line
        for index in date_lines:
            if date_lines.get(index) == date:
                selected_line.set(index)


# The selected date in the calendar is submitted.
def submit_date(calendar, date_label):
    check_date(calendar.get_date())

    # The label in the account menu is updated to the newly selected date.
    date_label.config(text=f"Selected date: {calendar.get_date()}")
    print(selected_line.get())




# The calendar is opened
def open_calendar(date_label):

    calendar_menu = Toplevel()
    calendar_menu.title("Choose Date")
    calendar_menu.geometry("300x300")

    calendar = Calendar(calendar_menu, date_pattern="dd/mm/yy")
    calendar.pack()
    submit_button = Button(calendar_menu, text="Submit Date", font=("Arial", 25),
                           command=lambda date=calendar, label=date_label: submit_date(calendar, label))
    submit_button.pack()

# The program grabs the date from the account's file.
def grab_user_data(username):

    global date_lines
    try:
        with open(f"{username}.txt", "r") as file:
            # Grabs all the data from the account's file.
            user_data = file.readlines()
            try:
                # The first line in the file is the corresponding line numbers and dates.
                date_lines_json = json.loads(user_data[0])
                date_lines = dict(date_lines_json)
            except IndexError:
                # If the text file is empty, an empty dictionary is created.
                date_lines = dict()

    except Exception:
        print("Something went wrong!")

    # The currently signed in account is set so the program knows which text file to be using.
    selected_account.set(username)


#FIX ERROR ON LINE 136
#Then I need to make it so that the total money transacted in the selected date is calculated (grabbing all the keys from
#the user_data dictionary and adding them to each other). Then I need to modify the balance label accordingly to the
#new balance.
#Then I need to make the user_data variable savable, and loadable in/from the account text file
def submit_transaction(transaction_entry, category_entry, transaction_label, balance_label):

    balances[selected_account.get()] += transaction_entry.get()
    #When this line is executed an error happens (IndexError: list index out of range)
    #This happens since if the selected line is 3, user_data might still have only 1, or 2 indexes.
    #What I am thinking is that every time a date is submitted, "None" is appended to the user_data variable.
    user_data[selected_line.get()].update({transaction_entry.get() : category_entry.get()})
    money_transacted = 0
    transaction_label.config(text=f"Money spent on {date_lines.get(selected_line)}: ")


# The user can either take money from his balance or put money in his balance
def open_transaction_menu(transaction_label, balance_label):

    transaction_window = Toplevel()
    transaction_window.geometry("300x300")

    transaction_frame = Frame(transaction_window)
    transaction_frame.pack()
    Label(transaction_frame, text="Money spent: ", font=("Arial", 20)).grid(row=0, column=0)
    money_entry = Entry(transaction_frame, font=("Arial", 20))
    money_entry.grid(row=0, column=1)
    Label(transaction_frame, text="Category of transaction: ", font=("Arial", 20)).grid(row=1, column=0)
    category_entry = Entry(transaction_frame, font=("Arial", 20))
    category_entry.grid(row=1, column=1)
    submit_entry_button = Button(transaction_window, text="Submit transaction",
                                 command=lambda transact_entry=money_entry, category_entry=category_entry:
                                 submit_transaction(transact_entry, category_entry, transaction_label, balance_label))
    submit_entry_button.pack()
# The menu where the user enters money and sees statistics is opened.
def open_account_menu(username):
    # The program grams the account's data from its text file.
    grab_user_data(username)

    # The program gets the present date.
    today = date.today()
    present_date = today.strftime("%d/%m/%y")
    check_date(present_date)

    # The main menu is destroyed and the account window is opened
    main_menu_window.destroy()
    account_window = Tk()
    account_window.title("My Financial Pal - " + username)
    account_window.geometry("420x420")

    # Displays the currently selected date
    selected_date_label = Label(account_window, text=f"Selected date: {present_date}", font=("Arial", 20))
    selected_date_label.pack()
    # Displays the current balance of the user.
    current_balance_label = Label(account_window, text=f"Current balance: {balances.get(selected_account.get())}",
                                  font=("Arial", 20))
    current_balance_label.pack()
    money_transacted_label = Label(account_window, text=(f"Money spent on {present_date}: " + ""), font=("Arial", 20))
    money_transacted_label.pack()
    # The user can transact money with this button.
    transaction_button = Button(account_window, text="Transact money", font=("Arial", 25),
                                command= lambda transact_label=money_transacted_label,
                                                balance_label=current_balance_label :
                                open_transaction_menu(transact_label, balance_label))
    transaction_button.pack()
    # The user can choose the date which he wants to log entries in with the calendar.
    calendar_button = Button(account_window, text="Select Day", font=("Arial", 25),
                             command=lambda label=selected_date_label: open_calendar(label))
    calendar_button.pack()

    account_window.mainloop()


# The user confirms his sign (if his entered account is valid).
def confirm_sign_in(username_entry, password_entry):
    if len(account_details) == 0:
        Label(sign_in_menu, text="There arent any existing accounts yet!", font=("Arial", 15)).pack()
    # The program goes through each account, and checks if the entered username and password match with any account.
    for key in account_details:
        # If they match, the current account is set accordingly.

        if username_entry.get() == key and password_entry.get() == account_details.get(key):
            current_account.set(username_entry.get())
            open_account_menu(username_entry.get())
        else:
            Label(sign_in_menu, text="Incorrect username or password!", font=("Arial", 15)).pack()


def open_sign_in_menu():
    global sign_in_menu
    sign_in_menu = Toplevel()
    sign_in_menu.title("Sign In")
    # The user can enter his username and password
    details_frame = Frame(sign_in_menu)
    details_frame.pack()
    username_label = Label(details_frame, text="Username: ", font=("Arial", 25))
    username_label.grid(row=0, column=0)
    username_entry = Entry(details_frame, font=("Arial", 25))
    username_entry.grid(row=0, column=1)
    password_label = Label(details_frame, text="Password: ", font=("Arial", 25))
    password_label.grid(row=1, column=0)
    password_entry = Entry(details_frame, font=("Arial", 25))
    password_entry.grid(row=1, column=1)

    # This button calls the confirm sign in method
    button = Button(sign_in_menu, text="Sign in", font=("Arial", 25),
                    command=lambda username=username_entry, password=password_entry: confirm_sign_in(username, password))
    button.pack()


def submit_balance(balance_entry, name_entry):
    balances.update({name_entry.get(): balance_entry.get()})

    # Puts all the data in account_details in the variable new_account_json, in JSON format, as a string variable.
    new_account_json = json.dumps(account_details)
    # Puts all the data in balances in the variable new_balance_json, in JSON format, as a string variable.
    new_balance_json = json.dumps(balances)

    # Saves the file (adds the account and balances to the accounts database file).
    with open("accounts", "w") as file:
        file.truncate(0)
        file.write(new_account_json + "\n" + new_balance_json)

    balance_window.destroy()
    new_account_menu.destroy()


# When creating his account, the user enters his starting balance
def open_set_balance_menu(name_entry):
    # The balance window is opened.
    global balance_window
    balance_window = Toplevel()
    balance_window.title("Set Balance")

    # The user is prompted to enter his balance
    Label(balance_window, text="Enter your account's starting balance in €\n(Can only be done once)",
          font=("Arial", 15)).pack()
    balance_entry = Entry(balance_window, font=("Arial", 15))
    balance_entry.pack()
    submit_balance_button = Button(balance_window, text="Submit balance", font=("Arial", 20),
                                   command=
                                   lambda entry=balance_entry, username=name_entry: submit_balance(entry, username))
    submit_balance_button.pack()


# The user tries to submit his account
def submit_account(username_entry, password_entry, menu):
    # If the user enters a username which is already taken, this is set to false, and the account won't be created.
    account_valid = True

    # If the account is valid (username is unique),
    # a new file which will contain all the data of the new account is created.
    try:
        open(f"{username_entry.get()}.txt", "x")
    except FileExistsError:
        error = Label(menu, text="There is already an existing account with the same username!")
        error.pack()
        account_valid = False

    # If the account the user entered isn't already taken, the user is sent back to the main menu,
    # and the new account is saved
    if account_valid == True:
        # The account details variable which contains all the account usernames and passwords is updated.
        account_details.update({username_entry.get(): password_entry.get()})

        open_set_balance_menu(username_entry)


# The create account menu is shown
def open_account_creation_menu():
    # this variable is global since another function needs to access it
    global new_account_menu

    new_account_menu = Toplevel()
    new_account_menu.title("Create Account")
    # The user can enter his username and password
    details_frame = Frame(new_account_menu)
    details_frame.pack()
    username_label = Label(details_frame, text="Username: ", font=("Arial", 25))
    username_label.grid(row=0, column=0)
    username_entry = Entry(details_frame, font=("Arial", 25))
    username_entry.grid(row=0, column=1)
    password_label = Label(details_frame, text="Password: ", font=("Arial", 25))
    password_label.grid(row=1, column=0)
    password_entry = Entry(details_frame, font=("Arial", 25))
    password_entry.grid(row=1, column=1)

    # With this button, the user tries to submit his account.
    button = Button(new_account_menu, text="Create Account", font=("Arial", 25),
                    command=lambda username=username_entry, password=password_entry:
                    submit_account(username, password, new_account_menu))
    button.pack()


# The menu at the start of running the program is displayed.
main_menu_window.title("Main Menu")
Button(main_menu_window, text="Sign in", font=("Arial", 25), command=open_sign_in_menu).pack()
Button(main_menu_window, text="Create account", font=("Arial", 25), command=open_account_creation_menu).pack()
main_menu_window.mainloop()
