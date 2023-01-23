from flask import Flask,render_template, request , redirect , url_for,session, flash
import tkinter
from tkinter import *
from tkinter import messagebox
from db import *

web =Flask(__name__)
web.secret_key='secretkey'
@web.route("/")
def login():
    return render_template("login.html")

@web.route("/admin_login/")
def admin_login():
    return render_template("admin_login.html")

@web.route("/user/")
def user_login():
    return render_template("user_login.html")

@web.route("/register/")
def register():
    return render_template("register.html")

@web.route("/reg/",methods=["POST"])
def doReg():
    selectedValue= request.form['size']
    if selectedValue=='1':
     name=request.form["name"]
     email=request.form["email"]
     password=request.form["password"]
     database_connection = sqlite3.connect("quizitDatabase.db")
     database_cursor = database_connection.cursor()
    #  database_cursor.execute("SELECT email FROM register_admin WHERE email=?",(email))
    #  result = database_cursor.fetchall()
    #  if result:
    #   flash('You are already registered, please log in')
    #   return redirect('/admin_login/')
    #  else:
     database_cursor.execute("insert into register_admin (name,email,password) values (?,?,?)",(name,email,password))
     database_connection.commit()
     database_connection.close()
     return redirect(url_for("admin_login"))
    else:
     name=request.form["name"]
     email=request.form["email"]
     password=request.form["password"]
     database_connection = sqlite3.connect("quizitDatabase.db")
     database_cursor = database_connection.cursor()
     database_cursor.execute("insert into register_user (name,email,password) values (?,?,?)",(name,email,password))
     database_connection.commit()
     database_connection.close()
     return redirect(url_for("user_login"))

@web.route("/admin_home/")
def admin_home():
    return render_template("admin_home.html")

@web.route("/user_home/")
def user_home():
    return render_template("user_home.html")

@web.route("/loginadmin/",methods=["POST"])
def adm_log():
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select * from register_admin where email=? and password=? ",(email,password))
    result=database_cursor.fetchone()
    if result:
        flash("login Successful")
        return redirect('/admin_home/')
    else:
        return redirect('/admin_login/')

@web.route("/loginuser/",methods=["POST"])
def us_log():
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select * from register_user where email=? and password=? ",(email,password))
    result=database_cursor.fetchone()
    if result:
        flash("login Successful")
        return redirect('/user_home/')
    else:
        return redirect('/user/')

@web.route("/add_ques/")
def add_ques():
    question=request.form["question"]
    optiona=request.form["optiona"]
    optionb=request.form["optionb"]
    optionc=request.form["optionc"]
    optiond=request.form["optiond"]
    correct_op=request.form["correct_op"]
    print(correct_op)
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("insert into question (question) values (?)",(question))
    database_cursor.execute("select * from ans where op1=? and op2=? and op3=? and op4=? and "(optiona,optionb,optionc,optiond))
    result=database_cursor.fetchone()


@web.route("/create_quiz/")   
def create_quiz():
    quiz_id=request.form["quiz_id"]
    quiz_name=request.form["quiz_name"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("insert into Quiz (quizId,quizName) values (?)",(quiz_id,quiz_name))
    result = database_cursor.fetchone()

if __name__=="__main__":
    web.run(debug=True,port=8000)


    
