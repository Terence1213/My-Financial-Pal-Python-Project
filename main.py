"""
To do:
> Test the program and go over code and comments.
"""
from tkinter import *
import json
from tkcalendar import Calendar
import datetime
from datetime import *
from datetime import timedelta
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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

        user_data.append(dict())

        save_user_data()



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
    money_spent = 0
    try:
        # Calculates the money spent depending on all the transactions in the date.
        money_spent = calculate_money_spent(user_data[selected_line.get()])
    except IndexError:
        print("Tried calculating the money spent on the selected day, but no transactions have been entered yet!")
    # The label in the account menu is updated to the newly selected date.
    date_label.config(text=f"Selected date: {calendar.get_date()}")

    # The selected_line is typecasted to string because the line numbers in date_lines are saved as strings.
    transaction_label.config(text=f"Money spent on {calendar.get_date()}: {money_spent}")


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

            # The data which is grabbed from the text file is transferred into the public user_data variable.
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

    # Checks if either the transaction entry box or the category entry box are empty.
    if transaction_entry.get() == "" or category_entry.get() == "":
        is_transaction_valid = False
        Label(window, text="You cannot leave the transaction box or the category box empty!").pack()

    # The program tries to convert the transaction into an integer variable. If the entry is either empty or not
    # entirely numeric, error messages are displayed, and the transaction is set as not valid.
    try:
        # The transaction entry is converted into an integer variable.
        transaction = int(transaction_entry.get())
    except ValueError:
        is_transaction_valid = False
        if transaction_entry.get() == "":
            pass
        else:
            Label(window, text="You can only enter numbers in the transaction box!").pack()

    try:
        all_transactions = [key for key in user_data[selected_line.get()]]
    except IndexError:
        all_transactions = list()
    # If the transaction the user enters has already been entered before in the same day, he is prompted with an error
    # message. I left the program like this because it is very complicated for me to find a way to make a dictionary
    # which allows for duplicate keys, while making the program work and save and load the data from / to the text files
    if all_transactions.__contains__(transaction_entry.get()):
        Label(window, text="Sorry, but you can't enter the same transaction amount twice in the same day. \n"
                           "Adding a + at the start of your transaction number allows you to enter 2 of \nthe same"
                           " transaction amount in the same day.",
              font=("Arial", 10)).pack()
    elif is_transaction_valid and (balances[selected_account.get()] + transaction) >= 0:
        # His balance is modified accordingly to his transaction
        balances[selected_account.get()] += transaction

        # The variable which contains all the transactions is updated with the new transaction.
        user_data[selected_line.get()].update({transaction_entry.get(): (category_entry.get()).lower()})

        # The transaction label in the account menu is modified accordingly to the user's transaction
        money_spent = calculate_money_spent(user_data[selected_line.get()])
        print(selected_line.get())
        print(type(selected_line.get()))
        print(date_lines.get("2"))

        transaction_label.config(text=f"Money spent on {date_lines.get(str(selected_line.get()))}: {money_spent}")

        # The balance label is updated.
        balance_label.config(text=f"Current balance: €{balances[selected_account.get()]}")

        save_account_data()
        save_user_data()
    elif is_transaction_valid:
        Label(window, text="You cannot extract more money than you currently have in you").pack()


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


# The program converts an RGB colorcode to a hexadecimal colorcode
def rgb_to_hex(r, g, b):
    rgb = [r, g, b]
    x = ''
    for i in rgb:
        x += format(i, '02x').upper()
    if x[0] == x[1] and x[2] == x[3] and x[4] == x[5]:
        x = x[0] + x[2] + x[4]
    return '#' + x


# Creates and draws a pichart on the specified window and with the specified details.
def create_pichart(categories, window):
    # The variable which contains the amount each category was transacted for.
    sizes = list()
    # The variable which contains labels which are to be shown for each category in the pi-chart.
    labels = list()
    # The variable which contains the randomised colors in a temporary RGB format.
    rgb_colors = list()
    # The variable which contains the required colors translated to hexadecimal format.
    colors = list()

    # For each category in the categories variable, the program appends the amount of the item to sizes variable,
    # and the name of the item to the labels variable.
    for item in categories:
        sizes.append(categories.get(item))
        labels.append(item)

    # For each unique category, the program generates a new random color (a random set of 3 numbers - RGB)
    for index in range(len(categories)):
        rgb_colors.append(np.random.choice(range(255), size=3))

    # The program translates all the generated colours to hexadecimal format.
    for (r, g, b) in rgb_colors:
        colors.append(rgb_to_hex(r, g, b))

    # The program sets the figure of the pi-chart and the canvas bar.
    fig = plt.figure(figsize=(3, 3), dpi=100)
    fig.set_size_inches(5, 4)

    # The pi-chart is plotted.
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
    plt.axis('equal')

    # The canvasbar is shown
    canvasbar = FigureCanvasTkAgg(fig, master=window)
    canvasbar.draw()
    canvasbar.get_tk_widget().pack()
    plt.close('all')


# A window is opened displaying the statistics of the selected day.
# I have to make it so there are separate pi-charts for money-in and money-out.
def submit_day(calendar, window):
    is_date_logged = False
    # The program goes through each existing date in the date_lines variable. If the selected date is not found, the
    # user is displayed with the message that his selected date has not been logged on before.
    for index in date_lines:
        if calendar.get_date() == date_lines.get(index):
            is_date_logged = True

    if not is_date_logged:
        Label(window, text="The date you have selected has not been logged on before!").pack()
    else:
        stats = Toplevel()
        stats.title(f"Statistics on {calendar.get_date()}")
        stats.geometry("700x800")

        current_line = None

        # The current line is set to the corresponding line of the selected date.
        for key in date_lines:
            if date_lines.get(key) == calendar.get_date():
                print("current_line set to " + str(key))
                current_line = key

        total_transactions = 0

        # Goes through each category for each transaction for the selected date.
        for key in user_data[int(current_line)]:
            total_transactions += int(key)

        total_transactions_label = Label(stats, text=f"Total transaction amount made on "
                                                     f"{calendar.get_date()}: {total_transactions}", font=("Arial", 25))
        total_transactions_label.pack()

        # Grabs all the transactions in and out, in the selected day, gets their categories and puts them in a list.
        spend_categories = list()
        deposit_categories = list()

        # Grabs all the transactions in and out in the selected day and puts them in a list.
        spend_transactions = list()
        deposit_transactions = list()

        for key in user_data[int(current_line)]:
            # If the key (the transaction amount) is negative, then the spend_categories is appended with the category.
            if int(key) < 0:
                spend_categories.append(user_data[int(current_line)].get(key))
                spend_transactions.append(int(key))
            # If the key (the transaction amount) is positive, then the deposit_categories is appended with the category.
            else:
                deposit_categories.append(user_data[int(current_line)].get(key))
                deposit_transactions.append(int(key))

        # Grabs the amount of times each category was transacted for, and puts it into a dictionary. ("Food : 1", etc.
        spend_categories = Counter(spend_categories)
        deposit_categories = Counter(deposit_categories)

        # Each item and its amount is multiplied with the corresponding transaction amount, so that if 100 was spent on
        # food once and 1000 was spent on clothes once, in the pi-chart they are not displayed as 50/50
        for index, item in enumerate(spend_categories):
            spend_categories[item] *= -spend_transactions[index]
        for index, item in enumerate(deposit_categories):
            deposit_categories[item] *= deposit_transactions[index]

        Label(stats, text="Pi-chart of transactions in:", font=("Arial", 20)).pack()
        create_pichart(deposit_categories, stats)
        Label(stats, text="Pi-chart of transactions out:", font=("Arial", 20)).pack()
        create_pichart(spend_categories, stats)


# A window is opened displaying the statistics of the days selected combined.
def submit_range_of_days(date1, date2):

    ranged_stats_window = Toplevel()
    ranged_stats_window.title("Ranged statistics window")
    # Date format: %d/%m/%y
    total_transactions = 0

    current_line = None

    print(date1.get(), date2.get())

    # Grabs all the transactions in and out, in the selected day, gets their categories and puts them in a list.
    spend_categories = list()
    deposit_categories = list()

    # Grabs all the transactions in and out in the selected day and puts them in a list.
    spend_transactions = list()
    deposit_transactions = list()

    if date1.get() != None and date2.get() != None and date2.get() > date1.get():
        current_date = date1.get()

        while True:
            #This variable is used to check whether the date selected has been logged on before.
            date_found = False

            # The current line is set to the corresponding line of the selected date.
            for date_index in date_lines:
                if date_lines.get(date_index) == current_date:
                    current_line = date_index
                    date_found = True
                    #The break is so that if the corresponding line index is found, the program doesn't keep looping.
                    break

            if date_found == True:
                # Goes through each category for each transaction for the selected date, if the date selected has been
                # logged on before.
                for key in user_data[int(current_line)]:
                    total_transactions += int(key)

                    # If the key (the transaction amount) is negative, then the spend_categories is appended with the
                    # category.
                    if int(key) < 0:
                        spend_categories.append(user_data[int(current_line)].get(key))
                        spend_transactions.append(int(key))
                    # If the key (the transaction amount) is positive, then the deposit_categories is appended with the
                    # category.
                    else:
                        deposit_categories.append(user_data[int(current_line)].get(key))
                        deposit_transactions.append(int(key))

            # Add the current day's transactions to the total transactions and their categories.
            # Now move to the next day.
            if current_date == date2.get():
                break

            # The current date is converted to a datetime object, so it can be incremented by one day. Then it is
            # converted back to a string variable.
            format = "%d/%m/%y"
            present_date = datetime.strptime(current_date, format)
            present_date += timedelta(days=1)
            current_date = present_date.strftime(format)
            print("new date is:", current_date)

        # Grabs the amount of times each category was transacted for, and puts it into a dictionary. ("Food : 1", etc.
        spend_categories = Counter(spend_categories)
        deposit_categories = Counter(deposit_categories)

        # Each item and its amount is multiplied with the corresponding transaction amount, so that if 100 was spent on
        # food once and 1000 was spent on clothes once, in the pi-chart they are not displayed as 50/50
        for index, item in enumerate(spend_categories):
            spend_categories[item] *= -spend_transactions[index]
        for index, item in enumerate(deposit_categories):
            deposit_categories[item] *= deposit_transactions[index]


        #The total transactions throughout the range of days and the pi-charts are displayed.
        Label(ranged_stats_window,
              text=f"Total transactions in range of dates {date1.get()} - {date2.get()}: {total_transactions}",
              font=("Arial", 25)).pack()

        Label(ranged_stats_window, text="Pi-chart of transactions in:", font=("Arial", 20)).pack()
        create_pichart(deposit_categories, ranged_stats_window)
        Label(ranged_stats_window, text="Pi-chart of transactions out:", font=("Arial", 20)).pack()
        create_pichart(spend_categories, ranged_stats_window)


# A calendar is opened, and the user selects which day he wants to see statistics for.
def day_statistics():

    global day_statistics_window
    day_statistics_window = Toplevel()
    calendar = Calendar(day_statistics_window, date_pattern="dd/mm/yy")
    calendar.pack()
    submit_button = Button(day_statistics_window, text="Submit Date", font=("Arial", 25),
                           command=lambda date=calendar, window=day_statistics_window: submit_day(date, window))
    submit_button.pack()


# The first date of the range of dates is selected by the user
def set_date_two(calendar):
    print(calendar.get_date())
    global date_two
    date_two.set(calendar.get_date())

# the second date of the range of dates is selected by the user
def set_date_one(calendar):
    print(calendar.get_date())
    global date_one
    date_one.set(calendar.get_date())


# A calendar is opened, and the user selects which range of days he wants to see statistics for.
def ranged_statistics():

    global date_one
    global date_two

    date_one = StringVar()
    date_two = StringVar()

    ranged_statistics_window = Toplevel()
    calendar = Calendar(ranged_statistics_window, date_pattern="dd/mm/yy")
    calendar.pack()

    # This is the frame which contains the date_one select and date_two select button
    frame = Frame(ranged_statistics_window)

    # The user selectes the starting and ending dates with these buttons
    date_one_button = Button(frame, text="Choose date1", command=lambda calendar=calendar:
    set_date_one(calendar))
    date_two_button = Button(frame, text="Choose date2", command=lambda calendar=calendar:
    set_date_two(calendar))

    # The buttons are displayed
    date_one_button.grid(row=0, column=0)
    date_two_button.grid(row=0, column=1)

    # The frame is displayed
    frame.pack()

    # If the starting and ending dates were selected, and date1 is smaller than date2, the user clicks the submit button
    # to submit the dates.
    submit_button = Button(ranged_statistics_window, text="Submit Date", font=("Arial", 25),
                           command=lambda date1=date_one, date2=date_two:
                           submit_range_of_days(date1, date2))
    submit_button.pack()


# The user chooses if he wants to see the statistics of a single day, or of a range of days.
def open_statistics_window():
    if len(user_data) > 0:
        statistics_window = Toplevel()
        statistics_window.title("Statistics window")

        daily_button = Button(statistics_window, text="One day", font=("Arial", 25), command=day_statistics)
        daily_button.pack()

        ranged_day_button = Button(statistics_window, text="Range of days", font=("Arial", 25),
                                   command=ranged_statistics)
        ranged_day_button.pack()
    else:
        print("No transactions were ever made on this account!")


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
    account_window.geometry("600x600")

    # Displays the currently selected date
    selected_date_label = Label(account_window, text=f"Selected date: {present_date}", font=("Arial", 20))
    selected_date_label.pack()
    # Displays the current balance of the user.
    current_balance_label = Label(account_window, text=f"Current balance: {balances.get(selected_account.get())}",
                                  font=("Arial", 20))

    money_spent = 0

    try:
        money_spent = calculate_money_spent(user_data[selected_line.get()])
    except IndexError:
        print("Tried calculating the money spent on the selected day, but no transactions have been entered yet!")
    current_balance_label.pack()
    money_transacted_label = Label(account_window, text=f"Money transacted on {present_date}: {money_spent}",
                                   font=('Arial', 20))
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
    # The user opens the statistics window.
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


# The user submits the balance which he enters in the balance entry box.
def submit_balance(balance_entry, name_entry):
    # The program tries, since if text is entered a run-time error would occur.
    try:
        # The balances dictionary is updated with the new account's starting balance.
        balances.update({name_entry.get(): int(balance_entry.get())})

        # The account text file is loaded and saved with this new data.
        save_account_data()

        # The balance and new account window are destroyed, leaving only the main menu open.
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
