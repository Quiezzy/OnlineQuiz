import sqlite3
def adminResult():
    database_connection=sqlite3.connect("quizitDatabase.db")
    database_cursor=database_connection.cursor()
    adminId=int(1)
    name=database_cursor.execute("select (name) from register_user where userId IN (select (userId) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?))",(adminId,))
    name=name.fetchall()
    quizName=database_cursor.execute("select (quizId) from ansUser where userId IN (select (userId) from ansUser where quizId IN(select (quizId) from Quiz where adminId=?))",(adminId,))
    quizName=quizName.fetchall()
    Name=None
    newName=[]
    for i in quizName:
        Name=database_cursor.execute("select (quizName) from Quiz where quizId=?",(i[0],))
        Name=Name.fetchone()
        newName.append(Name)
    score=database_cursor.execute("select (result) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?)",(adminId,))
    score=score.fetchall()
    total=database_cursor.execute("select (total) from ansUser where quizId IN (select (quizId) from Quiz where adminId=?)",(adminId,))
    total=total.fetchall()
    print("name:",name)
    print("quizname:",newName)
    print("score:",score)
    print("total:",total)
adminResult()