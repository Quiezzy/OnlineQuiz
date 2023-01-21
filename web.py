from flask import Flask,render_template, request , redirect , url_for,session

web =Flask(__name__)

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

print("hello")
if __name__=="__main__":
    web.run(debug=True,port=8000)

print("Arnab")
print("Hello")