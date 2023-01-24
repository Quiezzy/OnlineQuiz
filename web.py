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

adminId=None

@web.route("/loginadmin/",methods=["POST"])
def adm_log():
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select adminId from register_admin where email=? and password=?",(email,password))
    global adminId
    adminId=database_cursor.fetchone()[0]
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
    return render_template("add_question.html")
    
quiz_id=int(0)
@web.route("/create_quiz/",methods=["POST"])   
def create_quiz():
    global quiz_id
    quiz_id=request.form["quiz_id"]
    quiz_name=request.form["quiz_name"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("insert into Quiz (quizId,quizName,adminId) values (?,?,?)",(quiz_id,quiz_name,adminId))
    database_connection.commit()
    database_connection.close()
    return redirect("/add_ques/")


@web.route("/add_question",methods=["POST"])
def add_question():
    question=request.form["question"]
    optiona=request.form["optiona"]
    optionb=request.form["optionb"]
    optionc=request.form["optionc"]
    optiond=request.form["optiond"]
    correct_op=request.form["correct_op"]
    if(correct_op=="Option A"):
     global co_ans
     co_ans=optiona
    elif(correct_op=="Option B"):
        co_ans=optionb
    elif(correct_op=="Option C"):
        co_ans=optionc
    elif(correct_op=="Option D"):
        co_ans=optiond
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    print("Quiz_id",quiz_id)
    database_cursor.execute("insert into question (quizId,qName) values(?,?)",(quiz_id,question))
    database_cursor.execute("select qId from question where quizId=(?) and qName=(?)",(quiz_id,question))
    q_id=database_cursor.fetchone()[0]
    database_cursor.execute("insert into ans (qId,op1,op2,op3,op4,co) values(?,?,?,?,?,?)",(q_id,optiona,optionb,optionc,optiond,co_ans))
    database_connection.commit()
    database_connection.close()
    return redirect("/add_ques/")


@web.route("/quiz/")   
def quiz():
    return render_template("create_quiz.html")

if __name__=="__main__":
    web.run(debug=True,port=8000)


    
