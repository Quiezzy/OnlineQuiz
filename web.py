from flask import Flask,render_template, request , redirect , url_for,session, flash
import tkinter
from tkinter import *
from tkinter import messagebox
import sqlite3
web =Flask(__name__)
web.secret_key='secretkey'
newQID=int(0)
userId=None
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
adminId=None
@web.route("/reg/",methods=["POST"])
def doReg():
    selectedValue= request.form['size']
    if selectedValue=='1':
     name=request.form["name"]
     email=request.form["email"]
     password=request.form["password"]
     database_connection = sqlite3.connect("quizitDatabase.db")
     database_cursor = database_connection.cursor()
     database_cursor.execute("select (email) from register_admin where email=?",(email,))
     result=database_cursor.fetchone()
     if result:
        flash("Email Already Exist !",category='error')
        return redirect('/register/')
     elif len(password)<6:
        flash("Password must be atleast 6 character long",category='error')
        return redirect('/register/')
     database_cursor.execute("insert into register_admin (name,email,password) values (?,?,?)",(name,email,password))
     database_connection.commit()
     database_connection.close()
     flash("Registration Successful!",category='success')
     return redirect(url_for("admin_login"))
    else:
     name=request.form["name"]
     email=request.form["email"]
     password=request.form["password"]
     database_connection = sqlite3.connect("quizitDatabase.db")
     database_cursor = database_connection.cursor()
     database_cursor.execute("select (email) from register_user where email=?",(email,))
     result=database_cursor.fetchone()
     if result:
        flash("Email Already Exist !",category='error')
        return redirect("/register/")
     elif len(password)<6:
        flash("Password must be atleast 6 character long",category='error')
        return redirect("/register/")
     database_cursor.execute("insert into register_user (name,email,password) values (?,?,?)",(name,email,password))
     database_connection.commit()
     database_connection.close()
     flash("Registration Successful!",category='success')
     return redirect(url_for("user_login"))

admindata=None
@web.route("/admin_home/")
def admin_home():
    global admindata
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    admindata=database_cursor.execute("select name,email,password from register_admin where adminId=?",(adminId,))
    admindata=admindata.fetchall()
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    print(admindata)
    return render_template("admin_home.html",admindata=admindata)
userdata=None
@web.route("/user_home/")
def user_home():
    global userdata
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    userdata=database_cursor.execute("select name,email,password from register_user where userId=?",(userId,))
    userdata=userdata.fetchall()
    return render_template("user_home.html",userdata=userdata)


@web.route("/loginadmin/",methods=["POST"])
def adm_log():
    global adminId
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select * from register_admin where email=? and password=? ",(email,password))
    result=database_cursor.fetchone()
    if result:
        adminId=database_cursor.execute("select (adminId) from register_admin where email=? and password=?",(email,password))
        adminId=adminId.fetchone()[0]
        flash("Login Successful!",category='success')
        return redirect('/admin_home/')
    else:
        database_cursor.execute("select (email) from register_admin where email=?",(email,))
        email=database_cursor.fetchone()
        database_connection.commit()
        database_connection.close()
        if email:
         flash("Invalid Email or Password!",category='error')
         return redirect('/admin_login/')
        else:
            flash("User not Registered with us, kindly Register!",category='error')
            return redirect('/register/')
@web.route("/demo/")
def demo():
    return render_template("demo.html")

@web.route("/loginuser/",methods=["POST"])
def us_log():
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select * from register_user where email=? and password=? ",(email,password))
    result=database_cursor.fetchone()
    if result:
        global userId
        userId=database_cursor.execute("select userId from register_user where email=?",(email,))
        userId=userId.fetchone()[0]
        flash("Login Successful!",category='success')
        return redirect('/user_home/')
    else:
        database_cursor.execute("select (email) from register_user where email=?",(email,))
        email=database_cursor.fetchone()
        database_connection.commit()
        database_connection.close()
        if email:
         flash("Invalid Email or Password!",category='error')
         return redirect('/user/')
        else:
            flash("User not Registered with us, kindly Register!",category='error')
            return redirect('/register/')

@web.route("/add_ques/")
def add_ques():
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    return render_template("add_question.html")
    
quiz_id=int(0)
@web.route("/create_quiz/",methods=["POST"])   
def create_quiz():
    global quiz_id
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    quiz_id=request.form["quiz_id"]
    quiz_name=request.form["quiz_name"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    database_cursor.execute("select (quizId) from Quiz where quizId=?",(quiz_id,))
    result=database_cursor.fetchone()
    if result:
        flash("Quiz Id alreay exist!",category='error')
        return redirect("/quiz/")
    database_cursor.execute("insert into Quiz (quizId,quizName,adminId) values (?,?,?)",(quiz_id,quiz_name,adminId))
    database_connection.commit()
    database_connection.close()
    return redirect("/add_ques/")


@web.route("/add_question",methods=["POST"])
def add_question():
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
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
    database_cursor.execute("insert into ans (qId,op1,op2,op3,op4,co,quizId) values(?,?,?,?,?,?,?)",(q_id,optiona,optionb,optionc,optiond,co_ans,quiz_id))
    database_connection.commit()
    database_connection.close()
    flash("Question added successfully",category='success')
    return redirect("/add_ques/")


@web.route("/quiz/")   
def quiz():
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    return render_template("create_quiz.html")

@web.route("/takeQI/")   
def qi():
    return render_template("take_test.html")

questions=None
options=None
correct=None
trcount=None
i=int(-1)
count=int(0)
trace=int(1)
@web.route("/atQuiz/",methods=["POST","GET"])
def atQuiz():
    global count,i
    i=int(i)+int(1)
    if i==0 :
     database_connection=sqlite3.connect("quizitDatabase.db")
     database_cursor=database_connection.cursor()
     global questions
     questions=database_cursor.execute("select (qName) from question where quizId=?",(newQID,))
     questions=questions.fetchall()
     global options
     options=database_cursor.execute("select op1,op2,op3,op4 from ans where quizId=?",(newQID,))
     options=options.fetchall()
     global correct
     correct=database_cursor.execute("select (co) from ans where quizId=?",(newQID,))
     correct=correct.fetchall()
     database_connection.commit()
     database_connection.close()
     print("Questions are:",questions)
     print("options are:",options)
     print("Correct answers are:",correct)
     return render_template("user_quiz.html",questions=questions,options=options,correct=correct,i=i)
    elif i<len(questions):
        try:
            choseans=request.form['option']
        except:
            i=int(i)-int(1)
            flash("Sorry you can't go to previous question",category='error')
            return render_template("user_quiz.html",questions=questions,options=options,correct=correct,i=i)
        print(choseans)
        if choseans=='optionA':
            if options[i-1][0]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionB':
            if options[i-1][1]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionC':
            if options[i-1][2]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionD':
            if options[i-1][3]==correct[i-1][0]:
                count=int(count)+int(1)
        return render_template("user_quiz.html",questions=questions,options=options,correct=correct,i=i)
    else:
        try:
            choseans=request.form['option']
        except:
            i=int(i)-int(1)
            flash("Sorry you can't go to previous question",category='error')
            return render_template("user_quiz.html",questions=questions,options=options,correct=correct,i=i)
        if choseans=="optionA":
            if options[i-1][0]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionB':
            if options[i-1][1]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionC':
            if options[i-1][2]==correct[i-1][0]:
                count=int(count)+int(1)
        elif choseans=='optionD':
            if options[i-1][3]==correct[i-1][0]:
                count=int(count)+int(1)
        print("Your Score is :",count)
        database_connection=sqlite3.connect("quizitDatabase.db")
        database_cursor=database_connection.cursor()
        database_cursor.execute("insert into ansUser (userId,quizId,result,total) values (?,?,?,?)",(userId,newQID,count,len(questions)))
        database_connection.commit()
        database_connection.close()
        global trcount
        trcount=int(count)
        count=0
        i=int(-1)
        return redirect("/userScore/")

@web.route("/takeQIdata/",methods=["POST","GET"])   
def qidata():
    global i,count,trace
    i=int(-1)
    count=int(0)
    trace=int(1)
    global newQID
    newQID=request.form["quiz_id"]
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    global userId
    if userId==None:
        flash("Sorry! Your session has been expired",category='error')
        return redirect('/user/')
    database_cursor.execute("select (quizId) from ansUser where quizId=? and userId=?",(newQID,userId))
    check=database_cursor.fetchone()
    if check:
        flash("You have already attempted this quiz!",category='success')
        return redirect('/takeQI/')
    database_cursor.execute("select (quizId) from Quiz where quizId=?",(newQID,))
    result=database_cursor.fetchone()
    database_connection.commit()
    database_connection.close()
    if result:
        print(userId,newQID)
        return redirect("/atQuiz/")
    else:
        flash("Invalid QuizId!",category='error')
        return redirect("/takeQI/")
    
@web.route("/userScore/")
def userscore():
    global trcount
    global questions
    return render_template("score.html",count=trcount,total=len(questions))

@web.route("/userResult/")
def userResult():
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    quizName=database_cursor.execute("select (quizName) from Quiz where quizId IN (select (quizId) from ansUser where userId=?)",(userId,))
    quizName=quizName.fetchall()
    score=database_cursor.execute("select (result) from ansUser where userId=?",(userId,))
    score=score.fetchall()
    total=database_cursor.execute("select (total) from ansUser where userId=?",(userId,))
    total=total.fetchall()
    database_connection.commit()
    database_connection.close()
    print("quizName",quizName)
    return render_template("userResult.html",quizName=quizName,score=score,total=total)

@web.route("/adminViewQuiz/")
def adminViewQuiz():
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    viewQuiz=database_cursor.execute("select quizId,quizName from Quiz where adminId=?",(adminId,))
    viewQuiz=viewQuiz.fetchall()
    database_connection.commit()
    database_connection.close()
    print(viewQuiz)
    return render_template("adminViewQuiz.html",viewQuiz=viewQuiz)

@web.route("/adminResult/")
def adminResult():
    global admindata
    if not(admindata):
        flash("Your Session has been expired!",category='error')
        return redirect("/admin_login/")
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    name=database_cursor.execute("select (name) from register_user inner join ansUser on ansUser.userId=register_user.userId where ansUser.userId IN (select (userId) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?))",(adminId,))
    name=name.fetchall()
    quizName=database_cursor.execute("select (quizId) from ansUser where userId IN (select (userId) from ansUser where quizId IN(select (quizId) from Quiz where adminId=?))",(adminId,))
    quizName=quizName.fetchall()
    Name=None
    newName=[]
    for i in quizName:
        Name=database_cursor.execute("select (quizName) from Quiz where quizId=?",(i[0],))
        Name=Name.fetchone()
        newName.append(Name)
    score=database_cursor.execute("select (result) from ansUser where userId IN (select (userId) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?))",(adminId,))
    score=score.fetchall()
    total=database_cursor.execute("select (total) from ansUser where userId IN (select (userId) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?))",(adminId,))
    total=total.fetchall()
    database_connection.commit()
    database_connection.close()
    print("name:",name)
    print("quizname:",newName)
    print("score:",score)
    print("total:",total)
    return render_template("adminResult.html",name=name,quizName=newName,score=score,total=total)
# @web.route("/userResultData/",methods=["POST","GET"])
# def userResultData():
#     global userId
#     database_connection=sqlite3.connect("quizitDatabase.db")
#     database_cursor=database_connection.cursor()
#     quizName=database_cursor.execute("select (quizName) from Quiz where quizId=(select (quizId) from ansUser where userId=?)",(userId,))
#     quizName=quizName.fetchall
#     score=database_cursor.execute("select (result) from ansUser where userId=?",(userId,))
#     score=score.fetchall()
#     total=database_cursor.execute("select (total) from ansUser where userId=?",(userId,))
#     total=total.fetchall()
#     print("quizName",quizName)
#     return render_template("userResult.html",quizName=quizName,score=score,total=total)

# @web.route("/userResultData",methods=["GET"])
# def userResultData():


if __name__=="__main__":
    web.run(debug=True,port=8000)


    
