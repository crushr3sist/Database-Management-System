from api import *
from session import *
import sqlite3

# NOTE this function is a login system for admins. admins and workers need separate login systems since they have different tables.
def login_attemp_admin():
    global username, password

    # NOTE connects to the database
    con = connect()
    # NOTE starts a while loop as to give the user multiple chances to login however, it can be bruteforced.
    while True:
        # NOTE user enters their credentials
        username = input("Enter username:")
        password = input("Enter password:")
        cursor = con.cursor()
        # NOTE runs a query to check if the entered credentials exist in the table or not.
        find_user_fromAdmin = cursor.execute(
            ("SELECT * FROM Admin WHERE userName = ? AND password = ?"),
            (username, password),
        )
        resultsPassword = cursor.fetchall()
        # NOTE if the login in is successful, then it starts the admin function.
        if resultsPassword:
            print("Welcome :" + username)
            beginAdmin()
        else:
            # NOTE else it restarts the loop and prompts the user to enter their credentials correctly
            print("Username or Password not found")
            print("try again")


def login_attemp_workers():
    con = connect()
    while True:
        username = input("Enter username:")
        password = input("Enter password:")
        cursor = con.cursor()
        find_user_fromAdmin = cursor.execute(
            ("SELECT * FROM workers WHERE userName = ? AND password = ?"),
            (username, password),
        )
        firstName = cursor.execute(
            "SELECT firstName FROM workers WHERE userName = ? ", (username,)
        )
        resultsPassword = cursor.fetchall()
        if resultsPassword:
            print("Welcome :", list(firstName))
            break
        print("Username or Password not found")
        print("try again")


# NOTE  this is the main function, its what binds the files together.
def main():
    # NOTE it checks if a database file exists or not
    permission = checkIfEmpty()

    # NOTE if the file exists then it wont create the database file and it would just connect
    if permission == True:
        con = connect()
        createTableFormat()
        admin_register()

    # NOTE if the file doesnt exist then it will create one
    if permission == False:
        con = sqlite3.connect("main_Database.db")
        createTableFormat()
        admin_register()

    # NOTE this assure that the application is giving the correct privileges to the correct person
    adminOrNot = input("are you a worker or a admin?| type 'admin' or 'worker': ")

    if adminOrNot == "admin":
        print("please Login:\n")
        login_attemp_admin()

    if adminOrNot == "worker":
        print("please Login:\n")
        login_attemp_workers()


if __name__ == "__main__":
    main()
