"""
To do:
> Add comments.
> work on statistics
"""
from tkinter import *
import json
from tkcalendar import Calendar
from datetime import *
#Currently working on the statistics. (line 283)
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

date_lines = dict()

user_data = []

main_menu_window = Tk()

# The current account whose data is being used, and manipulated.
current_account = StringVar()

# The line in the text file which is currently selected and will be manipulated.
selected_line = IntVar()

# The account which is currently signed in to.
selected_account = StringVar()


# Saves the account details and balances to the accounts file
def save_account_data():
    # Puts all the data in account_details in the variable new_account_json, in JSON format, as a string variable.
    new_account_json = json.dumps(account_details)
    # Puts all the data in balances in the variable new_balance_json, in JSON format, as a string variable.
    new_balance_json = json.dumps(balances)

    # Saves the file (adds the account and balances to the accounts database file).
    with open("accounts", "w") as file:
        file.truncate(0)
        file.write(new_account_json + "\n" + new_balance_json)


def save_user_data():
    print("user data saved!")
    # Puts all the data in date_lines in the variable new_date_lines_json, in JSON format, as a string variable.
    new_date_lines_json = json.dumps(date_lines)

    # Saves the selected account's data into a text file.
    with open(f"{selected_account.get()}.txt", "w") as file:
        # Saves the file (adds the corresponding dates and line numbers to the account's text file).
        file.truncate(0)
        file.write(new_date_lines_json + "\n")

        # Saves the transactions in each day to the account's text file.
        for line in user_data:
            user_data_json = json.dumps(line)
            file.write(user_data_json + "\n")


def check_date(date):
    # A list of all the dates which have already been entered / created before is created.
    dates_entered = [i for i in date_lines.values()]

    # The program checks if the date which has been chosen in the calendar has already been entered before
    if not dates_entered.__contains__(date):
        # If false, the new date is inserted into the lines variable.
        date_lines.update({len(date_lines): date})
        selected_line.set(len(date_lines) - 1)

        save_user_data()

        user_data.append(dict())

    else:
        # If true, the program gets the index of the selected date in the lines variable,
        # and sets it to the selected line
        for index in date_lines:
            if date_lines.get(index) == date:
                selected_line.set(int(index))


# Calculates the amount of money spent in a day.
def calculate_money_spent(day):
    money_spent = 0

    for key in day:
        money_spent += int(key)

    return money_spent


# The selected date in the calendar is submitted.
def submit_date(calendar, date_label, transaction_label):
    # Checks whether the selected date has already been entered or not, and executes instructions accordingly.
    check_date(calendar.get_date())

    # Calculates the money spent depending on all the transactions in the date.
    money_spent = calculate_money_spent(user_data[selected_line.get()])

    # The label in the account menu is updated to the newly selected date.
    date_label.config(text=f"Selected date: {calendar.get_date()}")

    # The selected_line is typecasted to string because the line numbers in date_lines are saved as strings.
    transaction_label.config(text=f"Money spent on {date_lines.get(str(selected_line.get()))}: {money_spent}")


# The calendar is opened
def open_calendar(date_label, transaction_label):
    calendar_menu = Toplevel()
    calendar_menu.title("Choose Date")
    calendar_menu.geometry("300x300")

    calendar = Calendar(calendar_menu, date_pattern="dd/mm/yy")
    calendar.pack()
    submit_button = Button(calendar_menu, text="Submit Date", font=("Arial", 25),
                           command=lambda date=calendar, label=date_label, transaction=transaction_label:
                           submit_date(calendar, label, transaction))
    submit_button.pack()


# The program grabs the date from the account's file.
def grab_user_data(username):
    global date_lines
    global user_data

    with open(f"{username}.txt", "r") as file:
        # Grabs all the data from the account's file.
        data = file.readlines()
        try:
            # The first line in the file is the corresponding line numbers and dates.
            date_lines_json = json.loads(data[0])
            date_lines = dict(date_lines_json)

            user_data_json = list()

            # The program grabs all the transactions for each entered date from the account's text file.
            for index, line in enumerate(data):
                # The program ignores the first line in the text file (since it is the line numbers and dates)
                if index != 0:
                    user_data_json.append(json.loads(line))

            #The data which is grabbed from the text file is transferred into the public user_data variable.
            user_data = [line for line in user_data_json]


        except IndexError:
            # If the text file is empty, an empty dictionary is created.
            date_lines = dict()

    for line in user_data:
        print(line)
    # The currently signed in account is set so the program knows which text file to be using.
    selected_account.set(username)


# The user submits his transaction
def submit_transaction(transaction_entry, category_entry, transaction_label, balance_label, window):

    transaction = None

    is_transaction_valid = True

    #Checks if either the transaction entry box or the category entry box are empty.
    if transaction_entry.get() == "" or category_entry.get() == "":
        is_transaction_valid = False
        Label(window, text="You cannot leave the transaction box or the category box empty!").pack()

    # The program tries to convert the transaction into an integer variable. If the entry is either empty or not
    # entirely numeric, error messages are displayed, and the transaction is set as not valid.
    try:
        #The transaction entry is converted into an integer variable.
        transaction = int(transaction_entry.get())
    except ValueError:
        is_transaction_valid = False
        if transaction_entry.get() == "":
            pass
        else:
            Label(window, text="You can only enter numbers in the transaction box!").pack()

    all_transactions = [key for key in user_data[selected_line.get()]]

    #If the transaction the user enters has already been entered before in the same day, he is prompted with an error
    #message. I left the program like this because it is very complicated for me to find a way to make a dictionary
    #which allows for duplicate keys, while making the program work and save and load the data from / to the text files.
    if all_transactions.__contains__(transaction_entry.get()):
        Label(window, text="Sorry, but you can't enter the same transaction amount twice in the same day. \n"
                           "Adding a + at the start of your transaction number allows you to enter 2 of \nthe same"
                           " transaction amount in the same day.",
              font=("Arial", 10)).pack()
    elif is_transaction_valid:
        # His balance is modified accordingly to his transaction
        balances[selected_account.get()] += transaction

        # The variable which contains all the transactions is updated with the new transaction.
        user_data[selected_line.get()].update({transaction_entry.get(): (category_entry.get()).lower()})

        # The transaction label in the account menu is modified accordingly to the user's transaction
        money_spent = calculate_money_spent(user_data[selected_line.get()])

        transaction_label.config(text=f"Money spent on {date_lines.get(str(selected_line.get()))}: {money_spent}")

        # The balance label is updated.
        balance_label.config(text=f"Current balance: €{balances[selected_account.get()]}")

        save_account_data()
        save_user_data()


# The user can either take money from his balance or put money in his balance
def open_transaction_menu(transaction_label, balance_label):
    # The transaction window is opened
    transaction_window = Toplevel()

    transaction_frame = Frame(transaction_window)
    transaction_frame.pack()
    Label(transaction_frame, text="Transaction: ", font=("Arial", 20)).grid(row=0, column=0)
    money_entry = Entry(transaction_frame, font=("Arial", 20))
    money_entry.grid(row=0, column=1)
    Label(transaction_frame, text="Category of transaction: ", font=("Arial", 20)).grid(row=1, column=0)
    category_entry = Entry(transaction_frame, font=("Arial", 20))
    category_entry.grid(row=1, column=1)
    submit_entry_button = Button(transaction_window, text="Submit transaction",
                                 command=lambda transact_entry=money_entry, category_entry=category_entry:
                                 submit_transaction(transact_entry, category_entry,
                                                    transaction_label, balance_label, transaction_window))
    submit_entry_button.pack()


#A window is opened displaying the statistics of the selected day
def submit_day(calendar, window):


    is_date_logged = False
    # The program goes through each existing date in the date_lines variable. If the selected date is not found, the
    # user is displayed with the message that his selected date has not been logged on before.
    for index in date_lines:
        if calendar.get_date() == date_lines.get(index):
            is_date_logged = True

    if not is_date_logged:
        Label(window, text="The date you have selected has not been logged on before!")
    else:
        stats = Toplevel()

        current_line = None

        #The current line is set to the corresponding line of the selected date.
        for key in date_lines:
            if date_lines.get(key) == calendar.get_date():
                print("current_line set to " + key)
                current_line = key

        total_transactions = 0

        #Goes through each category for each transaction for the selected date.
        for key in user_data[int(current_line)]:
            total_transactions += int(key)

        total_transactions_label = \
            Label(stats, text=f"Total transaction amount made on {calendar.get_date()}: {total_transactions}")
        total_transactions_label.pack()

        # We need to get each unique category in the user_data variable, and the amount it was purchased for.
        # For the pi-chart, the total amount of transactions is the denominator in the calculation.
        categories = list()
        for line in user_data:
            pass
        canvas = Canvas(window, width=500, height=500)
        canvas.create_arc(100, 100, 350, 350, extent=359, style=ARC, width=5)
        canvas.create_arc(100, 100, 350, 350, extent=30, fill="red", width=5)
        canvas.create_arc(100, 100, 350, 350, start=30, extent=70, fill="green", width=5)
        canvas.create_arc(100, 100, 350, 350, start=100, extent=150, fill="blue", width=5)
        canvas.create_arc(100, 100, 350, 350, start=250, extent=110, fill="yellow", width=5)
        canvas.pack()
        #The program displays the total transactions made that day.
        #The program draws a pi chart according to the categories of the user's transactions.

#A window is opened displaying the statistics of the days selected combined.
def submit_range_of_days():
    pass


#A calendar is opened, and the user selects which day he wants to see statistics for.
def day_statistics():

    day_statistics_window = Toplevel()
    calendar = Calendar(day_statistics_window, date_pattern="dd/mm/yy")
    calendar.pack()
    submit_button = Button(day_statistics_window, text="Submit Date", font=("Arial", 25),
                           command=lambda date=calendar, window=day_statistics_window: submit_day(date, window))
    submit_button.pack()



#A calendar is opened, and the user selects which range of days he wants to see statistics for.
def ranged_statistics():
    pass


#The user chooses if he wants to see the statistics of a single day, or of a range of days.
def open_statistics_window():

    statistics_window = Toplevel()
    statistics_window.title("Statistics window")

    daily_button = Button(statistics_window, text="One day", font=("Arial", 25), command=day_statistics)
    daily_button.pack()

    ranged_day_button = Button(statistics_window, text="Range of days", font=("Arial",25), command=ranged_statistics)
    ranged_day_button.pack()

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
    money_spent = calculate_money_spent(user_data[selected_line.get()])
    current_balance_label.pack()
    money_transacted_label = Label(account_window, text=f"Money transacted on {present_date}: {money_spent}", font=("Arial", 20))
    money_transacted_label.pack()
    # The user can transact money with this button.
    transaction_button = Button(account_window, text="Transact money", font=("Arial", 25),
                                command=lambda transact_label=money_transacted_label,
                                               balance_label=current_balance_label:
                                open_transaction_menu(transact_label, balance_label))
    transaction_button.pack()
    # The user can choose the date which he wants to log entries in with the calendar.
    calendar_button = Button(account_window, text="Select Day", font=("Arial", 25),
                             command=lambda label=selected_date_label, money_label=money_transacted_label:
                             open_calendar(label, money_label))
    calendar_button.pack()
    #The user opens the statistics window.
    statistics_button = Button(account_window, text="See statistics", font=("Arial", 25),
                               command=open_statistics_window)
    statistics_button.pack()

    account_window.mainloop()


# The user confirms his sign (if his entered account is valid).
def confirm_sign_in(username_entry, password_entry):

    correct_password = True
    if len(account_details) == 0:
        Label(sign_in_menu, text="There arent any existing accounts yet!", font=("Arial", 15)).pack()
    # The program goes through each account, and checks if the entered username and password match with any account.
    for key in account_details:
        # If they match, the current account is set accordingly.

        if username_entry.get() == key and password_entry.get() == account_details.get(key):
            current_account.set(username_entry.get())
            open_account_menu(username_entry.get())
        else:
            correct_password = False

    if not correct_password:
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
                    command=lambda username=username_entry, password=password_entry: confirm_sign_in(username,
                                                                                                     password))
    button.pack()


#The user submits the balance which he enters in the balance entry box.
def submit_balance(balance_entry, name_entry):

    #The program tries, since if text is entered a run-time error would occur.
    try:
        #The balances dictionary is updated with the new account's starting balance.
        balances.update({name_entry.get(): int(balance_entry.get())})

        #The account text file is loaded and saved with this new data.
        save_account_data()

        #The balance and new account window are destroyed, leaving only the main menu open.
        balance_window.destroy()
        new_account_menu.destroy()
    except ValueError:
        error = Label(balance_window,
                      text="You can`t enter text in the balance entry box (only numbers can be entered.)!")
        error.pack()

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

    # The program checks if either the username or the password are left blank. If true, an error message is displayed
    # to the user.
    if username_entry.get() == "" or password_entry.get() == "":
        account_valid = False
        error = Label(menu, text="You cannot leave the username or password blank!")
        error.pack()

    # If the account is valid (username is unique),
    # a new file which will contain all the data of the new account is created.
    try:
        if account_valid:
            open(f"{username_entry.get()}.txt", "x")
    except FileExistsError:
        error = Label(menu, text="There is already an existing account with the same username!")
        error.pack()
        account_valid = False



    # If the account the user entered isn't already taken, the user is sent back to the main menu,
    # and the new account is saved
    if account_valid:
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
