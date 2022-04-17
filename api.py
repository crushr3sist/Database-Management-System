import sqlite3
from sqlite3 import Error
import os

# NOTE this function creates a admin account straight off the bat since it is required by the application to have a default admin account to gain functionality


def admin_register():
    con = connect()
    try:
        # NOTE enters default credentials
        con.execute(
            "INSERT INTO Admin (email,userName,password) VALUES (?,?,?)",
            ("Wizock.Admin@mail.com", "admin", "admin"),
        )
        # NOTE the default username and password is admin admin
        con.commit()
        con.close()
        print("your Admin account has been created :)")
    except Error as e:
        print(e)


def createTableFormat():
    conn1 = connect()
    try:
        conn1.execute(
            """
            CREATE TABLE Admin (
                UserId INTEGER PRIMARY KEY NOT NULL,
                email varchar(255),
                userName varchar(255),
                password varchar(255)
                )
                """
        )
        conn1.execute(
            """
            CREATE TABLE employee_personal (
                UserId INTEGER PRIMARY KEY NOT NULL,
                firstName varchar(255),
                lastName varchar(255),
                email varchar(255),
                userName varchar(255),
                position varchar(255) ,
                gender varchar(255),
                age varchar(255),
                adress varchar(255),
                phonenumber int,
                FOREIGN KEY (Email) REFERENCES employee_personal(normal_contact)
                FOREIGN KEY (phonenumber) REFERENCES emergency_contact(phoneNo)
                )
            """
        )

        conn1.execute(
            """
            CREATE TABLE application_infomation(
                UserId int,
                Username varchar(255) PRIMARY KEY NOT NULL,
                password varchar(255) UNIQUE,
                email varchar(255),
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId),
                FOREIGN KEY (Email) REFERENCES employee_personal(normal_contact)
                )
            """
        )

        conn1.execute(
            """
            CREATE TABLE employee_pay(
                UserId int,
                Username varchar(255),
                weeklyPay money PRIMARY KEY NOT NULL,
                wage int UNIQUE,
                age varchar(255),
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId),
                FOREIGN KEY (Username) REFERENCES application_infomation(employee_shifts)
            )
            """
        )
        conn1.execute(
            """
            CREATE TABLE employee_shifts(
                UserId int,
                Positions string PRIMARY KEY NOT NULL,
                startingTime time,
                endingTime time,
                shiftsPerWeek int,
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId)
                )
            """
        )

        conn1.execute(
            """
            CREATE TABLE late_arrivals(
                UserId int,
                employeeName varchar(255),
                startingTime time,
                arrivalTime time,
                lateBy time,
                lateAmt int PRIMARY KEY NOT NULL ,
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId),
                FOREIGN KEY (employeeName) REFERENCES employee_personal(firstName)
            )"""
        )

        conn1.execute(
            """
            CREATE TABLE emergency_contact(
                UserId int,
                phoneNo int PRIMARY KEY NOT NULL,
                Email string,
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId),
                FOREIGN KEY (Email) REFERENCES employee_personal(normal_contact)
				)
            """
        )

        conn1.execute(
            """
            CREATE TABLE normal_contact(
                UserId int,
                Email string PRIMARY KEY NOT NULL,
                adress string ,
                FOREIGN KEY (UserId) REFERENCES employee_personal(UserId)
            )
            """
        )
        # this is a query which creates a table, this specific query sets up the table's format
        check_Admin = conn1.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Admin'"
        )
        check_Workers = conn1.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='workers'"
        )

        if check_Admin != None:
            conn1.execute("DROP TABLE Admin")
        if check_Workers != None:
            conn1.execute("DROP TABLE workers")
    except Error as e:
        print(e)


# NOTE this function connects to the database file
def connect():
    Path = os.getcwd() + "\main_DataBase.db"
    if Path != os.path.islink(Path):
        con = sqlite3.connect(Path)
    # NOTE this function returns the connection variable so that it can be used anywhere with any variable name.
    return con


# NOTE this function checks if the database file exists or not since it causes errors if the application is asked to create a database that allready exists.
def checkIfEmpty():
    Path = os.getcwd() + "\main_DataBase.db"
    if os.path.exists(Path) == True:
        return False
    else:
        return True
