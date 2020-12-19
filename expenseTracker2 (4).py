from tkinter import *
from PIL import Image, ImageTk
import pymysql
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

expenditure = []
debit_amount = []
mnth1 = []
amnt1 = []
amnt2 = []
cnt: int = 0

home = 'urHomeDomain'
newlogin = 'urnewlogin'
edit = 'ureditWindow'

# connection = pymysql.connect(host="localhost", user="root", db="database1", password="Anu@0405")
# cur = connection.cursor()


def login():
    global userID
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    if User.get() == "" or Pass.get() == "":
        messagebox.showerror("Incomplete Data", "All fields are required")

    else:
        try:
            messagebox.showinfo("Connected", "Connected successfully to database")
            Email = User.get()
            Password = Pass.get()
            cur = connection.cursor()
            query = "SELECT emailid , password FROM login"
            cur.execute(query)
            for (email, pas) in cur:
                if Email == email and Password == pas:
                    login = True
                    break
                else:
                    login = False
            userID = (Email.split('@')[0])
            if login == True:
                newWindow()
                messagebox.showinfo("Logged in", "Logged in successfully")
            elif login == False:
                messagebox.showerror("Something went wrong", "Enter valid Username of Password")
        except:
            messagebox.showwarning("Not Connected", "Start MySQL Server First")

        connection.close()

def create():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    if (newLogin.first_name.get() == "" or newLogin.last_name.get() == "" or newLogin.EmailID.get() == "" or
            newLogin.Occupation.get() == "" or newLogin.mobnum.get() == "" or newLogin.set_password.get() == "" or newLogin.cnf_password.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    elif newLogin.set_password.get() != newLogin.cnf_password.get():
        messagebox.showerror("Error", "Password and Confirm password should be same...")
    else:
        try:
            cur = connection.cursor()
            cur.execute("SELECT * FROM login WHERE emailid=%s", User.get())
            row = cur.fetchone()
            if row != NONE:
                messagebox.showerror("User already exist", "User already exist please try another Email-ID")
            else:
                sqlinsert = "INSERT INTO login(first_name,Last_name,emailid,occupation,mobile_number,password)VALUES(%s,%s,%s,%s,%s,%s)"
                cur.execute(sqlinsert,
                            (newLogin.first_name.get(), newLogin.last_name.get(), newLogin.EmailID.get(),
                             newLogin.Occupation.get(),
                             newLogin.mobnum.get(), newLogin.set_password.get()))
                connection.commit()
                connection.close()
                messagebox.showinfo("Data Inserted", "User Data Inserted Successfully...")
                clearNewlogin()
        except Exception as es:
            messagebox.showerror("Error", "Unable to Login")


def back():
    global newlogin
    newlogin.withdraw()
    root.deiconify()


def clearNewlogin():
    newLogin.first_name.delete(0, END)
    newLogin.last_name.delete(0, END)
    newLogin.EmailID.delete(0, END)
    newLogin.Occupation.delete(0, END)
    newLogin.mobnum.delete(0, END)
    newLogin.set_password.delete(0, END)
    newLogin.cnf_password.delete(0, END)


def addCredit():
    credit = newWindow.credit_entry.get()
    date = newWindow.date_entry.get()
    credit_mode = newWindow.mode_of_credit.get()

    if (newWindow.date_entry.get() == "" or newWindow.credit_entry.get() == "" or newWindow.mode_of_credit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        newWindow.txt_box1.insert(END,
                                  "       " + date + "\t\t       " + credit + "\t\t                 " + credit_mode + "\n")

        credit_table()
        clearCredit()


def addDebit():
    date = newWindow.date_entry.get()
    expenditure = newWindow.item.get()
    deposit = newWindow.deposit_entry.get()
    deposit_mode = newWindow.mode_of_deposit.get()

    if (newWindow.date_entry.get() == "" or newWindow.item.get() == "" or newWindow.deposit_entry.get() == "" or
            newWindow.mode_of_deposit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")

    else:
        newWindow.txt_box2.insert(END, " " + date + "\t   " + expenditure + "\t\t       " + deposit +
                                  "\t\t" + deposit_mode + "\n")

        debit_table()
        clearDebit()


def credit_table():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    if (newWindow.date_entry.get() == "" or newWindow.credit_entry.get() == "" or newWindow.mode_of_credit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        cur = connection.cursor()
        insert_credit = "INSERT INTO credit(Date_of_Credit,Amount_Credited,Mode_of_Credit,emailid)VALUES(%s,%s,%s,%s)"
        cur.execute(insert_credit,
                    (newWindow.date_entry.get(), newWindow.credit_entry.get(), newWindow.mode_of_credit.get(),
                     User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Data Inserted", "Credit data inserted to table successfully")


def debit_table():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    if (newWindow.date_entry.get() == "" or newWindow.item.get() == "" or newWindow.deposit_entry.get() == "" or
            newWindow.mode_of_deposit.get() == ""):
        messagebox.showerror("Incomplete Data", "All fields are required")
    else:
        cur = connection.cursor()
        insert_debit = "INSERT INTO debit(Date_of_Debit,Expenditure,Amount_Debited,Mode_of_Debit,emailid)VALUES(%s,%s,%s,%s,%s)"
        cur.execute(insert_debit,
                    (newWindow.date_entry.get(), newWindow.item.get(), newWindow.deposit_entry.get(),
                     newWindow.mode_of_deposit.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Data Inserted", "Debit data inserted to table successfully")


def printTotal():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query1 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s"
    cur.execute(query1, (User.get()))
    result1 = cur.fetchall()

    query2 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s"
    cur.execute(query2, (User.get()))
    result2 = cur.fetchall()

    result = result1[0][0] - result2[0][0]
    newWindow.balance_entry.insert(0, result)


def clearCredit():
    newWindow.date_entry.delete(0, END)
    newWindow.credit_entry.delete(0, END)
    newWindow.mode_of_credit.delete(0, END)


def clearDebit():
    newWindow.date_entry.delete(0, END)
    newWindow.item.delete(0, END)
    newWindow.deposit_entry.delete(0, END)
    newWindow.mode_of_deposit.delete(0, END)


def clearShow():
    newWindow.balance_entry.delete(0, END)

def My_data():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "Select first_name from login where emailid = %s"
    cur.execute(query, User.get())
    res1 = cur.fetchone()
    Profile.first_name.insert(0, res1)

    cur = connection.cursor()
    query = "Select last_name from login where emailid = %s"
    cur.execute(query, User.get())
    res2 = cur.fetchone()
    Profile.last_name.insert(0, res2)

    cur = connection.cursor()
    query = "Select occupation from login where emailid = %s"
    cur.execute(query, User.get())
    res3 = cur.fetchone()
    Profile.Occupation.insert(0, res3)

    cur = connection.cursor()
    query = "Select mobile_number from login where emailid = %s"
    cur.execute(query, User.get())
    res4 = cur.fetchone()
    Profile.mob_no.insert(0, res4)

    cur = connection.cursor()
    query = "Select emailid from login where emailid = %s"
    cur.execute(query, User.get())
    res5 = cur.fetchone()
    Profile.EmailID.insert(0, res5)


def clear_update_field():
    Profile.first_name.delete(0, END)
    Profile.last_name.delete(0, END)
    Profile.Occupation.delete(0, END)
    Profile.mob_no.delete(0, END)
    Profile.EmailID.delete(0, END)


def update():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    if Edit.ref1.get() == 'first_name':
        cur = connection.cursor()
        query = "UPDATE login set first_name = %s where emailid =%s"
        cur.execute(query, (Edit.ref2.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Updated", "Data Updated successfully")

    elif Edit.ref1.get() == 'last_name':
        cur = connection.cursor()
        query = "UPDATE login set last_name = %s where emailid =%s"
        cur.execute(query, (Edit.ref2.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Updated", "Data Updated successfully")

    elif Edit.ref1.get() == 'occupation':
        cur = connection.cursor()
        query = "UPDATE login set occupation = %s where emailid =%s"
        cur.execute(query, (Edit.ref2.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Updated", "Data Updated successfully")

    elif Edit.ref1.get() == 'mobile_number':
        cur = connection.cursor()
        query = "UPDATE login set mobile_number = %s where emailid =%s"
        cur.execute(query, (Edit.ref2.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Updated", "Data Updated successfully")

    else:
        cur = connection.cursor()
        query = "UPDATE login set password = %s where emailid =%s"
        cur.execute(query, (Edit.ref2.get(), User.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Updated", "Data updated Successfully")

    clear_update_field()
    My_data()


def clearLogin():
    User.delete(0, END)
    Pass.delete(0, END)


def exitWindow():
    global home
    home.withdraw()
    root.deiconify()
    clearLogin()
    messagebox.showinfo("Logged Out", "Logged out Successfully!!!")


def delete_debit():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "DELETE FROM debit WHERE emailid=%s AND Expenditure=%s AND Date_of_Debit=%s AND Amount_Debited=%s"
    cur.execute(query, (User.get(), deleteWindow.entry4.get(), deleteWindow.entry3.get(), deleteWindow.entry5.get()))
    connection.commit()
    messagebox.showinfo("Debit Deleted", "Debit Transaction deleted successfully")
    clear_deleteDebit()
    clear_display_debit()
    display_debit()


def delete_credit():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "DELETE FROM credit WHERE emailid=%s AND Date_of_Credit=%s AND Amount_Credited=%s"
    cur.execute(query, (User.get(), deleteWindow.entry1.get(), deleteWindow.entry2.get()))
    connection.commit()
    messagebox.showinfo("Credit Deleted", "Credit Transaction deleted successfully")
    clear_deleteCredit()
    clear_display_credit()
    display_credit()


def clear_deleteDebit():
    deleteWindow.entry4.delete(0, END)
    deleteWindow.entry3.delete(0, END)
    deleteWindow.entry5.delete(0, END)


def clear_deleteCredit():
    deleteWindow.entry1.delete(0, END)
    deleteWindow.entry2.delete(0, END)


def display_debit():
    clear_display_debit()
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query1 = "SELECT * FROM debit WHERE emailid = %s order by date(Date_of_Debit)"
    cur.execute(query1, (User.get()))
    result1 = cur.fetchall()
    if len(result1) != 0:
        for rows in result1:
            date1 = str(rows[0])
            expenditure1 = rows[1]
            amount1 = str(rows[2])
            mode = rows[3]
            newWindow.txt_box2.insert(END, " " + date1 + "\t   " + expenditure1 + "\t\t       " + amount1 +
                                      "\t\t" + mode + "\n")
        messagebox.showinfo("Debit Records Entered", "Debit Records Entered successfully")
    else:
        messagebox.showerror("No Data", "No data in database")
    connection.commit()
    connection.close()


def display_credit():
    clear_display_credit()
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query2 = "SELECT * FROM credit WHERE emailid = %s order by date(Date_of_Credit)"
    cur.execute(query2, (User.get()))
    result2 = cur.fetchall()
    if len(result2) != 0:
        for rows in result2:
            date2 = str(rows[0])
            amount2 = str(rows[1])
            mode = rows[2]
            newWindow.txt_box1.insert(END,
                                      "       " + date2 + "\t\t       " + amount2 + "\t\t                 " + mode + "\n")
        messagebox.showinfo("Credit Records Entered", "Credit Records Entered successfully")
    else:
        messagebox.showerror("No Data", "No data in database")
    connection.commit()
    connection.close()


def clear_display_credit():
    newWindow.txt_box1.delete("1.0", END)


def clear_display_debit():
    newWindow.txt_box2.delete("1.0", END)


def new_details():
    clear_display_debit()
    clear_display_credit()


def last_update():
    last = Toplevel(root)
    last.title("Last Transaction")
    last.geometry('600x460+450+100')
    last.config(bg="azure")
    last.resizable(False, False)

    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()

    # ********************* FRAME 1 CREDIT TRANSACTION *************************

    frame1 = Frame(last, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(last, text="Credit Transaction")
    frame1.place(x=20, y=20, width=560, height=180)

    lab1 = Label(frame1, text="Date :", font=('arial', 15, 'bold'))
    lab1.place(x=20, y=20)
    entry1 = Entry(frame1, font=('arial', 15), bd=5, relief=SUNKEN)
    entry1.place(x=225, y=20)

    lab2 = Label(frame1, text="Amount Credited :", font=('arial', 15, 'bold'))
    lab2.place(x=20, y=60)
    entry2 = Entry(frame1, font=('arial', 15), bd=5, relief=SUNKEN)
    entry2.place(x=225, y=60)

    lab3 = Label(frame1, text="Mode of Payment : ", font=('arial', 15, 'bold'))
    lab3.place(x=20, y=100)
    entry3 = Entry(frame1, font=('arial', 15), bd=5, relief=SUNKEN)
    entry3.place(x=225, y=100)

    query2 = "SELECT Date_of_Credit, Amount_Credited, Mode_of_Credit FROM credit WHERE emailid=%s"
    cur.execute(query2, User.get())
    result2 = cur.fetchall()
    for i in result2:
        date1 = i[0]
        amt1 = i[1]
        mode1 = i[2]

    entry1.insert(0, date1)
    entry2.insert(0, amt1)
    entry3.insert(0, mode1)

    # ********************* FRAME 2 DEBIT TRANSACTION *************************

    frame2 = Frame(last, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(last, text="Debit Transaction")
    frame2.place(x=20, y=220, width=560, height=220)

    lab4 = Label(frame2, text="Date :", font=('arial', 15, 'bold'))
    lab4.place(x=20, y=20)
    entry4 = Entry(frame2, font=('arial', 15), bd=5, relief=SUNKEN)
    entry4.place(x=225, y=20)

    lab5 = Label(frame2, text="Amount Debited :", font=('arial', 15, 'bold'))
    lab5.place(x=20, y=60)
    entry5 = Entry(frame2, font=('arial', 15), bd=5, relief=SUNKEN)
    entry5.place(x=225, y=60)

    lab6 = Label(frame2, text="Expenditure", font=('arial', 15, 'bold'))
    lab6.place(x=20, y=100)
    entry6 = Entry(frame2, font=('arial', 15), bd=5, relief=SUNKEN)
    entry6.place(x=225, y=100)

    lab7 = Label(frame2, text="Mode of Payment : ", font=('arial', 15, 'bold'))
    lab7.place(x=20, y=140)
    entry7 = Entry(frame2, font=('arial', 15), bd=5, relief=SUNKEN)
    entry7.place(x=225, y=140)

    query1 = "SELECT Date_of_Debit, Expenditure, Amount_Debited, Mode_of_Debit FROM debit WHERE emailid=%s"
    cur.execute(query1, User.get())
    result1 = cur.fetchall()
    for j in result1:
        date2 = j[0]
        exp = j[1]
        amt2 = j[2]
        mode2 = j[3]

    entry4.insert(0, date2)
    entry5.insert(0, amt2)
    entry6.insert(0, exp)
    entry7.insert(0, mode2)


def barChart():
    global expenditure, debit_amount
    expenditure *= 0
    debit_amount *= 0

    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT Expenditure, SUM(Amount_Debited) FROM debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s group by expenditure"
    cur.execute(query1, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    for i in result1:
        expenditure.append(i[0])
        debit_amount.append(i[1])

    plt.style.use('bmh')
    plt.xlabel('Expenditure', fontsize=15)
    plt.ylabel('Amount', fontsize=15)
    plt.bar(expenditure, debit_amount, 0.4)
    plt.title("Debit Amount V/S Expenditure")
    plt.show()
    # expenditure.clear()
    # debit_amount.clear()


def pieChart():
    global expenditure, debit_amount
    expenditure *= 0
    debit_amount *= 0

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT Expenditure, Amount_Debited FROM debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s group by expenditure"
    cur.execute(query1, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    for i in result1:
        expenditure.append(i[0])
        debit_amount.append(i[1])

    plt.style.use('bmh')
    plt.pie(debit_amount, labels=expenditure, radius=1.2, autopct='%0.01f%%', shadow=True)
    plt.title("Debit Amount V/S Expenditure")
    plt.show()

    # expenditure.clear()
    # debit_amount.clear()


def track1():
    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()
    query = "SELECT SUM(Amount_Credited) from credit WHERE emailid=%s AND Date_of_Credit BETWEEN %s AND %s"
    cur.execute(query, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result1 = cur.fetchall()
    trackMoney.ref3.insert(0, result1)

    query = "SELECT SUM(Amount_Debited) from debit WHERE emailid=%s AND Date_of_Debit BETWEEN %s AND %s"
    cur.execute(query, (User.get(), trackMoney.ref1.get(), trackMoney.ref2.get()))
    result2 = cur.fetchall()
    trackMoney.ref4.insert(0, result2)

    result3 = result1[0][0] - result2[0][0]
    trackMoney.ref5.insert(0, result3)


def reset():
    trackMoney.ref3.delete(0, END)
    trackMoney.ref4.delete(0, END)
    trackMoney.ref5.delete(0, END)


def view():
    if trackMoney.ref6.get() == 'Bar Chart':
        barChart()
    elif trackMoney.ref6.get() == 'Pie Chart':
        pieChart()
    else:
        messagebox.showerror("Error", "Please select proper option")


def monthTracker():
    mnth = Toplevel(root)
    mnth.title("Monthly Tracker")
    mnth.geometry("600x580+450+100")
    mnth.config(bg="azure")
    mnth.resizable(0, 0)

    # **************************** FRAME 1 ********************************

    frame1 = Frame(mnth, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(mnth, text="Compare Monthly")
    frame1.place(x=10, y=10, width=580, height=380)

    lab1 = Label(frame1, text="Month 1", font=('arial', 15, 'bold'))
    lab1.place(x=75, y=15)

    monthTracker.ref1 = ttk.Combobox(frame1, font=('arial', 15))
    monthTracker.ref1['values'] = (
        '', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December')
    monthTracker.ref1.place(x=10, y=50)

    lab2 = Label(frame1, text="Month 2", font=('arial', 15, 'bold'))
    lab2.place(x=375, y=15)

    monthTracker.ref2 = ttk.Combobox(frame1, font=('arial', 15))
    monthTracker.ref2['values'] = (
        '', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December')
    monthTracker.ref2.place(x=290, y=50)

    cmpr_btn1 = Button(frame1, text="COMPARE", font=("Times", 15, "bold"), fg="black", bg='#009999',
                       activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                       command=compare, cursor="hand2").place(x=215, y=90)

    lab3 = Label(frame1, text="Month 1", font=('arial', 15, 'bold'))
    lab3.place(x=175, y=150)

    lab4 = Label(frame1, text="Month 2", font=('arial', 15, 'bold'))
    lab4.place(x=375, y=150)

    lab5 = Label(frame1, text="Credited\nAmount", font=('arial', 15, 'bold'))
    lab5.place(x=10, y=190)

    lab6 = Label(frame1, text="Debited\nAmount", font=('arial', 15, 'bold'))
    lab6.place(x=10, y=250)

    monthTracker.entry1 = Entry(frame1, font=('arial', 15), width=13)
    monthTracker.entry1.place(x=150, y=205)

    monthTracker.entry2 = Entry(frame1, font=('arial', 15), width=13)
    monthTracker.entry2.place(x=350, y=205)

    monthTracker.entry3 = Entry(frame1, font=('arial', 15), width=13)
    monthTracker.entry3.place(x=150, y=265)

    monthTracker.entry4 = Entry(frame1, font=('arial', 15), width=13)
    monthTracker.entry4.place(x=350, y=265)

    clr_btn1 = Button(frame1, text="CLEAR", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=7, height=1, relief=RAISED, bd=5,
                      command=clear_monthTracker, cursor="hand2").place(x=275, y=305)

    # btn1 = Button(frame1, text="MONTHLY HISTORY", font=("Times", 15, "bold"), fg="black", bg='#009999',
    #               activebackground='#669999', width=18, height=1, relief=RAISED, bd=5,
    #               command=barChart2, cursor="hand2").place(x=215, y=365)

    # ********************** FRAME 2 *******************************

    frame2 = Frame(mnth, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(mnth, text="Graphical Representation")
    frame2.place(x=10, y=405, width=580, height=165)

    monthTracker.opt_box = ttk.Combobox(frame2, font=('arial', 17))
    monthTracker.opt_box['values'] = ('', 'Bar Graph', 'Line Graph', 'Stacked Bar Graph')
    monthTracker.opt_box.place(x=160, y=10)

    btn1 = Button(frame2, text="MONTHLY HISTORY", font=('Times', 15, 'bold'), fg="black", bg='#009999',
                  activebackground='#669999', width=18, height=1, relief=RAISED, bd=5,
                  command=data_barChart2, cursor="hand2").place(x=170, y=70)


def compare():
    connection = pymysql.connect(host="localhost", user="root",db="manager", password="Shubham@2404")
    cur = connection.cursor()

    query1 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s AND MONTHNAME(Date_of_Credit)=%s"
    cur.execute(query1, (User.get(), monthTracker.ref1.get()))
    result1 = cur.fetchall()
    monthTracker.entry1.insert(0, result1[0][0])

    query2 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid=%s AND MONTHNAME(Date_of_Credit)=%s"
    cur.execute(query2, (User.get(), monthTracker.ref2.get()))
    result2 = cur.fetchall()
    monthTracker.entry2.insert(0, result2[0][0])

    query3 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s AND MONTHNAME(Date_of_Debit)=%s"
    cur.execute(query3, (User.get(), monthTracker.ref1.get()))
    result3 = cur.fetchall()
    monthTracker.entry3.insert(0, result3[0][0])

    query4 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid=%s AND MONTHNAME(Date_of_Debit)=%s"
    cur.execute(query4, (User.get(), monthTracker.ref2.get()))
    result4 = cur.fetchall()
    monthTracker.entry4.insert(0, result4[0][0])


def clear_monthTracker():
    monthTracker.entry1.delete(0, END)
    monthTracker.entry2.delete(0, END)
    monthTracker.entry3.delete(0, END)
    monthTracker.entry4.delete(0, END)
    monthTracker.ref1.delete(0,END)
    monthTracker.ref2.delete(0,END)


def data_barChart2():
    global mnth1, amnt1, amnt2

    mnth1 *= 0  # clearing list
    amnt1 *= 0  # clearing list
    amnt2 *= 0  # clearing list

    connection = pymysql.connect(host="localhost", user="root", db="manager", password="Shubham@2404")
    cur = connection.cursor()

    # ****** QUERY FOR MONTH ************

    query1 = "SELECT MONTHNAME(Date_of_Debit) AS 'Month Name' FROM debit WHERE emailid=%s ORDER BY MONTH(Date_of_Debit)"
    cur.execute(query1, User.get())
    result1 = cur.fetchall()
    for m in result1:
        if m[0] not in mnth1:
            mnth1.append(m[0])

    # ********* QUERY FOR SUM OF AMOUNT DEBITED ***********

    query2 = "SELECT SUM(Amount_Debited) FROM debit WHERE emailid = %s GROUP BY MONTHNAME(Date_of_Debit) ORDER BY MONTH(Date_of_Debit)"
    cur.execute(query2, User.get())
    result2 = cur.fetchall()
    for i in result2:
        amnt1.append(i[0])

    # ************ QUERY FOR SUM OF AMOUNT CREDITED ************

    query3 = "SELECT SUM(Amount_Credited) FROM credit WHERE emailid = %s GROUP BY MONTHNAME(Date_of_Credit) ORDER BY MONTH(Date_of_Credit)"
    cur.execute(query3, User.get())
    result3 = cur.fetchall()
    for j in result3:
        amnt2.append(j[0])

    if monthTracker.opt_box.get() == "Bar Graph":
        bar1 = np.arange(len(mnth1))
        bar2 = [i + 0.4 for i in bar1]
        plt.xticks(bar1 + 0.4 / 2, mnth1)
        plt.bar(bar2, amnt1, 0.4, label="Debit")
        plt.bar(bar1, amnt2, 0.4, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    elif monthTracker.opt_box.get() == "Line Graph":
        plt.plot(mnth1, amnt1, label="Debit")
        plt.plot(mnth1, amnt2, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    elif monthTracker.opt_box.get() == "Stacked Bar Graph":
        plt.bar(mnth1, amnt1, 0.4, label="Debit")
        plt.bar(mnth1, amnt2, 0.4, bottom=amnt1, label="Credit")
        plt.xlabel("Month's")
        plt.ylabel("Amount")
        plt.title("Amount V/S Month")
        plt.legend()
        plt.show()

    else:
        messagebox.showerror("Error", "Select proper option..!!!")


def deleteWindow():
    delWin = Toplevel(root)
    delWin.title("Delete Transaction Window")
    delWin.geometry("600x480+450+100")
    delWin.config(bg='azure')
    delWin.resizable(False, False)

    # --------------- Frame1 ------------------------------------------------------------------
    frame1 = Frame(delWin, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(delWin, text="Credit Details")
    frame1.place(x=20, y=20, width=560, height=200)

    lab1 = Label(frame1, text="Date of Credit :", font=('arial', 15, 'bold'))
    lab1.place(x=10, y=10)
    deleteWindow.entry1 = DateEntry(frame1, font=('arial', 15), date_pattern='yyyy-mm-dd')
    deleteWindow.entry1.place(x=220, y=10)

    lab2 = Label(frame1, text="Amount Credited :", font=('arial', 15, 'bold'))
    lab2.place(x=10, y=50)
    deleteWindow.entry2 = Entry(frame1, font=('arial', 15))
    deleteWindow.entry2.place(x=220, y=50)

    del_btn1 = Button(frame1, text="DELETE CREDIT\nTRANSACTION", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=19, height=2, relief=RAISED, bd=5,
                      command=delete_credit, cursor="hand2").place(x=175, y=90)

    # --------------- Frame2 ------------------------------------------------------------------

    frame2 = Frame(delWin, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(delWin, text="Debit Details")
    frame2.place(x=20, y=230, width=560, height=235)

    lab3 = Label(frame2, text="Date of Debit :", font=('arial', 15, 'bold'))
    lab3.place(x=10, y=10)
    deleteWindow.entry3 = DateEntry(frame2, font=('arial', 15), date_pattern='yyyy-mm-dd')
    deleteWindow.entry3.place(x=220, y=10)

    lab4 = Label(frame2, text="Expenditure :", font=('arial', 15, 'bold'))
    lab4.place(x=10, y=50)
    deleteWindow.entry4 = ttk.Combobox(frame2, font=('arial', 15), justify='left')
    deleteWindow.entry4['values'] = (
        '', 'EMI', 'Maintainence', 'Shopping', 'Food', 'Health', 'Entertainment', 'Travelling', 'Other')
    deleteWindow.entry4.place(x=220, y=50)

    lab5 = Label(frame2, text="Amount Debited :", font=('arial', 15, 'bold'))
    lab5.place(x=10, y=90)
    deleteWindow.entry5 = Entry(frame2, font=('arial', 15))
    deleteWindow.entry5.place(x=220, y=90)

    del_btn2 = Button(frame2, text="DELETE DEBIT\nTRANSACTION", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=19, height=2, relief=RAISED, bd=5,
                      command=delete_debit, cursor="hand2").place(x=175, y=130)


def back2():
    pass
# *********************** EDIT WINDOW **********************

def Edit():
    edit = Toplevel(root)
    edit.title("My Profile")
    edit.geometry('600x200+450+150')
    edit.config(bg='azure')
    edit.resizable(False, False)

    frame1 = Frame(edit, bd=2, relief=SUNKEN)
    frame1.place(x=20, y=20, width=560, height=160)

    Edit.lab1 = Label(frame1, text='Select field to Update :', font=('arial', 15, 'bold'))
    Edit.lab1.place(x=10, y=10)
    Edit.ref1 = ttk.Combobox(frame1, font=("arial", 17))
    Edit.ref1['values'] = ('', 'first_name', 'last_name', 'occupation', 'mobile_number', 'password')
    Edit.ref1.place(x=250, y=10)

    Edit.lab2 = Label(frame1, text='Enter new data   :', font=('arial', 15, 'bold'))
    Edit.lab2.place(x=10, y=50)
    Edit.ref2 = Entry(frame1, font=("arial", 15), bd=5, relief=SUNKEN, width=10)
    Edit.ref2.place(x=250, y=50)

    show_btn = Button(frame1, text="UPDATE", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                      command=update, cursor="hand2").place(x=120, y=100)

    back_btn2 = Button(frame1, text="BACK", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                      command=back2, cursor="hand2").place(x=250, y=100)

# ************************ HISTORY WINDOW *******************

def trackMoney():
    track_money = Toplevel(root)
    track_money.title("Track Money")
    track_money.geometry("600x665+450+70")
    track_money.config(bg="azure")
    track_money.resizable(False, False)

    # ******************* FRAME 1 ******************************

    frame1 = Frame(track_money, bd=2, relief=SUNKEN)
    frame1 = LabelFrame(track_money, text="Date Entry")
    frame1.place(x=20, y=15, width=565, height=180)

    trackMoney.label1 = Label(frame1, text="Starting Date :", font=("arial", 15, "bold"))
    trackMoney.label1.place(x=10, y=10)
    trackMoney.ref1 = DateEntry(frame1, font=("arial", 15), date_pattern="yyyy-mm-dd")
    trackMoney.ref1.place(x=190, y=10)

    trackMoney.label2 = Label(frame1, text="Ending Date :", font=("arial", 15, "bold"))
    trackMoney.label2.place(x=10, y=50)
    trackMoney.ref2 = DateEntry(frame1, font=("arial", 15), date_pattern="yyyy-mm-dd")
    trackMoney.ref2.place(x=190, y=50)

    show_btn = Button(frame1, text="SHOW", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                      command=track1, cursor="hand2").place(x=80, y=100)

    # ************************* FRAME 2 *********************************

    frame2 = Frame(track_money, bd=2, relief=SUNKEN)
    frame2 = LabelFrame(track_money, text="Details")
    frame2.place(x=20, y=205, width=565, height=250)

    trackMoney.lab3 = Label(frame2, text='Total money Earn      :', font=('arial', 15, 'bold'))
    trackMoney.lab3.place(x=10, y=20)
    trackMoney.ref3 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=10)
    trackMoney.ref3.place(x=250, y=20)

    trackMoney.lab4 = Label(frame2, text='Total money spent     :', font=('arial', 15, 'bold'))
    trackMoney.lab4.place(x=10, y=70)
    trackMoney.ref4 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=10)
    trackMoney.ref4.place(x=250, y=70)

    trackMoney.lab5 = Label(frame2, text='Total money available :', font=('arial', 15, 'bold'))
    trackMoney.lab5.place(x=10, y=120)
    trackMoney.ref5 = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=10)
    trackMoney.ref5.place(x=250, y=120)

    reset_btn = Button(frame2, text="RESET", font=("Times", 15, "bold"), fg="black", bg='#009999',
                       activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                       command=reset, cursor="hand2").place(x=80, y=170)

    # ******************** FRAME 3 ********************************

    frame3 = Frame(track_money, bd=2, relief=SUNKEN)
    frame3 = LabelFrame(track_money, text="Graphical Representation")
    frame3.place(x=20, y=465, width=565, height=180)

    trackMoney.lab6 = Label(frame3, text="Plot Graph:", font=('arial', 15, 'bold'))
    trackMoney.lab6.place(x=70, y=25)

    trackMoney.ref6 = ttk.Combobox(frame3, font=('arial', 17))
    trackMoney.ref6['values'] = ('', 'Bar Chart', 'Pie Chart')
    trackMoney.ref6.place(x=220, y=25)

    view_btn = Button(frame3, text="VIEW", font=('Times', 15, 'bold'), fg='black', bg='#009999',
                      activebackground='#669999', width=10, height=1, relief=RAISED, bd=5,
                      command=view, cursor="hand2").place(x=140, y=95)


def back1():
    global Profile, home
    Profile.withdraw()
    home.deiconify()


# ************************ PROFILE WINDOW ********************

def Profile():
    profile = Toplevel(root)
    profile.title("PROFILE PAGE")
    profile.geometry("610x450+450+100")
    profile.config(bg="azure")
    profile.resizable(False, False)

    image3 = Image.open("profile.jpeg")
    image3 = image3.resize((1500, 750), Image.ANTIALIAS)
    test3 = ImageTk.PhotoImage(image3)
    label3 = Label(profile, image=test3)
    label3.image = test3
    label3.place(x=0, y=0)

    image4 = Image.open("newloginface.jpeg")
    image4 = image4.resize((120, 75), Image.ANTIALIAS)
    test4 = ImageTk.PhotoImage(image4)
    label4 = Label(profile, image=test4)
    label4.image = test4
    label4.place(x=30, y=35)

    something_1 = Label(profile, text="PERSONAL DATA", font=('arial', 25, 'bold'), fg='black')
    something_1.place(x=215, y=50)

    first = Label(profile, text="First Name :", font=('arial', 15, 'bold'), fg='black').place(x=30, y=145)
    Profile.first_name = Entry(profile, width=30, font=('caliber', 14), highlightbackground='black',
                               highlightthickness=1)
    Profile.first_name.place(x=230, y=145)

    last = Label(profile, text="Last Name :", font=('arial', 15, 'bold'), fg='black').place(x=30, y=185)
    Profile.last_name = Entry(profile, width=30, font=('caliber', 15), highlightbackground='black',
                              highlightthickness=1)
    Profile.last_name.place(x=230, y=185)

    occ = Label(profile, text="Occupation:", font=('arial', 15, 'bold'), fg='black').place(x=30, y=225)
    Profile.Occupation = Entry(profile, width=30, font=('caliber', 15), highlightbackground='black',
                               highlightthickness=1)
    Profile.Occupation.place(x=230, y=225)

    mob_no = Label(profile, text="Mobile Number:", font=('arial', 15, 'bold'), fg='black').place(x=30, y=265)
    Profile.mob_no = Entry(profile, width=30, font=('caliber', 15), highlightbackground='black', highlightthickness=1)
    Profile.mob_no.place(x=230, y=265)

    Email = Label(profile, text="Email-ID:", font=('arial', 15, 'bold'), fg='black').place(x=30, y=305)
    Profile.EmailID = Entry(profile, width=30, font=('caliber', 15), highlightbackground='black',
                            highlightthickness=1)
    Profile.EmailID.place(x=230, y=305)

    My_data()

    updat_Data = Button(profile, text="Update Data", font=("Times", 15, "bold"), fg="black", bg='#009999',
                        activebackground='#669999', width=12, height=1, relief=RAISED, bd=5,
                        command=Edit, cursor="hand2").place(x=160, y=375)

    back_btn1 = Button(profile, text="BACK", font=("Times", 15, "bold"), fg="black", bg='#009999', cursor="hand2",
                       activebackground='#669999', width=12, height=1, relief=RAISED, bd=5, command=back1)
    back_btn1.place(x=390, y=375)


# ************************ NEW WINDOW *************************

def newWindow():
    global userID, home
    root.withdraw()  # closes the login window
    home = Toplevel(root)
    home.title("Main Window:: Expense Tracker")
    home.geometry("1500x750+15+0")
    home.configure(background="lightblue")
    home.resizable(False, False)

    # **************MENU BAR******************************
    my_menu = Menu(home)
    home.config(menu=my_menu)

    # ******************** EDIT MENU ******************************

    profile = Menu(my_menu, font="Times 15")
    my_menu.add_cascade(label="Profile", menu=profile)
    profile.add_command(label="Edit", command=Profile)
    profile.add_command(label="Logout", command=exitWindow)

    # ************** FILE MENU *******************************

    fileMenu = Menu(my_menu, font="Times 15 ")
    my_menu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Transaction", command=new_details)
    fileMenu.add_command(label="Delete Transaction", command=deleteWindow)
    fileMenu.add_command(label="Display Debit Transaction", command=display_debit)
    fileMenu.add_command(label="Display Credit Transaction", command=display_credit)
    fileMenu.add_command(label="View Last Transaction", command=last_update)

    # ***************** HISTORY ***********************************

    track = Menu(my_menu, font="Times 15")
    my_menu.add_cascade(label="History", menu=track)
    track.add_command(label="Track Transaction", command=trackMoney)
    track.add_command(label="Track Monthly", command=monthTracker)

    # *******************FRAME 1 *********************************

    frame1 = Frame(home, bd=2, relief=SUNKEN)
    frame1.place(x=20, y=20, width=650, height=440)

    title1 = Label(frame1, text="Expenditure Info", font=("times new roman", 24, "underline"), bg="#666699",
                   fg="white", width=10, height=1).place(x=0, y=0, relwidth=1)

    # --------------- date entry ----------------------------------

    date_label = Label(frame1, text="Date : ", font=("times", 18), bg="white", fg="black").place(x=20, y=60)
    newWindow.date_entry = DateEntry(frame1, font=("arial", 18), date_pattern='yyyy-mm-dd')
    newWindow.date_entry.place(x=250, y=60)

    # --------------- Credited Amount --------------------------------------
    credit_label = Label(frame1, text="Amount Credited : ", font=("times", 18), bg="white",
                         fg="black").place(x=20, y=110)
    newWindow.credit_entry = Entry(frame1, font=("arial", 18), relief=SUNKEN)
    newWindow.credit_entry.place(x=250, y=110)

    # ---------------- Mode of Credit ------------------------------

    mode_of_credit = Label(frame1, text="Mode of Credit : ", font=("times", 18), bg="white",
                           fg="black").place(x=20, y=160)
    newWindow.mode_of_credit = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.mode_of_credit['values'] = ('', 'Cash', 'Debit Card', 'Net Banking', 'UPI', 'Other')
    newWindow.mode_of_credit.place(x=250, y=160)

    # -------------- Money Spend on ----------------------------------------
    item_label = Label(frame1, text="Money Spend on : ", font=("times", 18), bg="white",
                       fg="black").place(x=20, y=210)
    newWindow.item = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.item['values'] = (
        '', 'EMI', 'Maintainence', 'Shopping', 'Food', 'Health', 'Entertainment', 'Travelling', 'Other')
    newWindow.item.place(x=250, y=210)

    # -------------- Deposited Amount --------------------------------------------------------
    deposit_label = Label(frame1, text="Amount Debited : ", font=("times", 18), bg="white",
                          fg="black").place(x=20, y=260)
    newWindow.deposit_entry = Entry(frame1, font=("arial", 18), relief=SUNKEN)
    newWindow.deposit_entry.place(x=250, y=260)

    # ------------- Mode of Deposit ---------------------------------------------

    mode_of_deposit = Label(frame1, text="Mode of Debit", font=("arial", 18), bg="white",
                            fg="black").place(x=20, y=310)
    newWindow.mode_of_deposit = ttk.Combobox(frame1, font=("arial", 18), justify="left")
    newWindow.mode_of_deposit['values'] = ('', 'Cash', 'Debit Card', 'Net Banking', 'UPI', 'Other')
    newWindow.mode_of_deposit.place(x=250, y=310)

    # -------------------------- Add Button -------------------------------------

    add_btn1 = Button(frame1, text="ADD DEBIT DETAILS", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=19, height=1, relief=RAISED, bd=5,
                      command=addDebit, cursor="hand2").place(x=350, y=380)

    add_btn2 = Button(frame1, text="ADD CREDIT DETAILS", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=19, height=1, relief=RAISED, bd=5,
                      command=addCredit, cursor="hand2").place(x=50, y=380)

    # ***********************FRAME 2************************************************

    frame2 = Frame(home, bd=2, relief=SUNKEN)
    frame2.place(x=20, y=485, width=650, height=250)

    title2 = Label(frame2, text="Details", font=("times new roman", 24, "underline"), bg="#666699",
                   fg="white", width=10, height=1).place(x=0, y=0, relwidth=1)

    # ----------------------- Balance -----------------------------------------

    balance_label = Label(frame2, text="Total Balance :", font=("times", 20), bg="white",
                          fg="black").place(x=90, y=90)
    newWindow.balance_entry = Entry(frame2, font=("arial", 20), bd=5, relief=SUNKEN, width=15)
    newWindow.balance_entry.place(x=320, y=90)

    # ------------------------ Show Button --------------------------------------

    show_btn = Button(frame2, text="SHOW", font=("Times", 15, "bold"), fg="black", bg='#009999',
                      activebackground='#669999', width=8, height=1, relief=RAISED, bd=5,
                      command=printTotal, cursor="hand2").place(x=140, y=160)

    reset_btn = Button(frame2, text="RESET", font=("Times", 15, "bold"), fg="black", bg='#009999',
                       activebackground='#669999', width=9, height=1, relief=RAISED, bd=5,
                       command=clearShow, cursor="hand2").place(x=320, y=160)

    # **************************FRAME 3 ******************************************

    frame3 = Frame(home, bd=2, relief=SUNKEN)
    frame3.place(x=700, y=20, width=780, height=713)

    title3 = Label(frame3, text="TABLE", font=("times new roman", 24, "underline"), bg="#666699",
                   fg="white", width=10, height=1).place(x=0, y=0, relwidth=1)

    # ---------------------- Headings -------------------------------------------

    heading_label1 = Label(frame3, font=("times", 18),
                           text="          Date                     Amount Credited                        Mode of Credit").place(
        x=20, y=60)

    newWindow.txt_box1 = Text(frame3, width=52, height=8, font=("times", 20))
    newWindow.txt_box1.place(x=20, y=90)

    heading_label2 = Label(frame3, font=("times", 18),
                           text="    Date            Expenditure            Amount Debited        Mode of Payment").place(
        x=20, y=345)

    newWindow.txt_box2 = Text(frame3, width=52, height=10, font=("times", 20))
    newWindow.txt_box2.place(x=20, y=375)

    scrlbar1 = ttk.Scrollbar(frame3, command=newWindow.txt_box2.yview)
    scrlbar1.place(relx=1, rely=0, relheight=1, anchor='ne')
    newWindow.txt_box2.configure(yscrollcommand=scrlbar1.set)

    scrlbar2 = ttk.Scrollbar(frame3, command=newWindow.txt_box1.yview)
    scrlbar2.place(relx=0.98, rely=0.5, relheight=1, anchor='se')
    newWindow.txt_box1.configure(yscrollcommand=scrlbar2.set)


# ************************* NEW LOGIN **************************

def newLogin():
    global userID, home, newlogin
    root.withdraw()  # close login page
    newlogin = Toplevel(root)
    newlogin.title("New Registration")
    newlogin.geometry('1500x750+15+15')
    newlogin.config(bg='azure')
    newlogin.resizable(False, False)

    image2 = Image.open("newlogin.jpeg")
    image2 = image2.resize((1500, 750), Image.ANTIALIAS)
    test2 = ImageTk.PhotoImage(image2)
    label2 = Label(newlogin, image=test2)
    label2.image = test2
    label2.place(x=0, y=0)

    image4 = Image.open("newloginface.jpeg")
    image4 = image4.resize((150, 80), Image.ANTIALIAS)
    test4 = ImageTk.PhotoImage(image4)
    label4 = Label(newlogin, image=test4)
    label4.image = test4
    label4.place(x=470, y=90)

    something_1 = Label(newlogin, text="USER DETAILS", font=('arial', 35, 'bold'), fg='black')
    something_1.place(x=730, y=110)

    first = Label(newlogin, text="First Name :", font=('arial', 18, 'bold'), fg='black').place(x=470, y=220)
    newLogin.first_name = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                                highlightthickness=1)
    newLogin.first_name.place(x=740, y=220)

    last = Label(newlogin, text="Last Name :", font=('arial', 18, 'bold'), fg='black').place(x=470, y=270)
    newLogin.last_name = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                               highlightthickness=1)
    newLogin.last_name.place(x=740, y=270)

    occ = Label(newlogin, text="Occupation:", font=('arial', 18, 'bold'), fg='black').place(x=470, y=320)
    newLogin.Occupation = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                                highlightthickness=1)
    newLogin.Occupation.place(x=740, y=320)

    mobnum = Label(newlogin, text="Mobile Number:", font=('arial', 18, 'bold'), fg='black').place(x=470, y=370)
    newLogin.mobnum = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black', highlightthickness=1)
    newLogin.mobnum.place(x=740, y=370)

    Email = Label(newlogin, text="Email-ID:", font=('arial', 18, 'bold'), fg='black').place(x=470, y=420)
    newLogin.EmailID = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                             highlightthickness=1)
    newLogin.EmailID.place(x=740, y=420)

    set_pass = Label(newlogin, text="Set Password:", font=('arial', 18, 'bold'), fg='black').place(x=470, y=470)
    newLogin.set_password = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                                  highlightthickness=1, show='*')
    newLogin.set_password.place(x=740, y=470)

    cnf_password = Label(newlogin, text="Confirm Password:", font=('arial', 18, 'bold'), fg='black').place(x=470, y=520)
    newLogin.cnf_password = Entry(newlogin, width=30, font=('caliber', 17), highlightbackground='black',
                                  highlightthickness=1, show='*')
    newLogin.cnf_password.place(x=740, y=520)

    save = Button(newlogin, text="SAVE", font=('arial', 18, 'bold'), fg='white', bg='blue', activebackground='gray',
                  width=8, height=1, command=create, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
    save.place(x=620, y=590)

    back_btn = Button(newlogin, text="BACK", font=('arial', 18, 'bold'), fg='white', bg='blue', activebackground='gray',
                      width=8, height=1, command=back, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
    back_btn.place(x=820, y=590)


# ************************** LOGIN PAGE *************************

root = Tk()
root.title("Login Page")
root.geometry("1500x750+15+0")
root.resizable(False, False)

image1 = Image.open("login2.jpeg")
image1 = image1.resize((1500, 750), Image.ANTIALIAS)
test1 = ImageTk.PhotoImage(image1)

label1 = Label(root, image=test1)
label1.image = test1
label1.place(x=0, y=0)

site1 = Label(root, text='WELCOME TO MONEY MANAGER', font=('Times', 35, 'bold'), fg="darkblue")
site1.place(x=0, y=2, relwidth=1)

username = Label(root, text="Username :", font=('arial', 15, 'bold'), fg='black').place(x=880, y=390)
User = Entry(root, width=27, font=('caliber', 15), bd=4, highlightbackground='black', highlightthickness=1)
User.place(x=1030, y=390)

password = Label(root, text="Password :", font=('arial', 15, 'bold'), fg='black').place(x=880, y=440)
Pass = Entry(root, width=27, font=('caliber', 15), bd=4, highlightbackground='black', highlightthickness=1, show="*")
Pass.place(x=1030, y=440)

submit = Button(root, text="LOGIN", font=('arial', 13, 'bold'), fg='white', bg='green', activebackground='lightblue',
                width=10, height=2, command=login, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
submit.place(x=1100, y=530)

label2 = Label(root, text="Don't have an account? ", font=('times', 16), fg='black', bg='lightgray', height=1)
label2.place(x=890, y=615)

newlogin = Button(root, text='SIGN UP', font=('arial', 13, 'bold'), fg='white', bg='green',
                  activebackground='lightblue',
                  width=10, height=2, command=newLogin, compound=LEFT, relief=RAISED, bd=5, cursor="hand2")
newlogin.place(x=1100, y=600)

root.mainloop()
