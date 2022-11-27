import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="573169",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            if username == "":
                return "Введите логин!"
            password = request.form.get('password')
            if password == "":
                return "Введите пароль!"
            try:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            except Exception as E:
                print(E)
                return "Не удалось войти в аккаунт, проверьте логин и пароль, если забыли пароль воспользуйтесь запасным!"

        elif request.form.get("backup"):
            return redirect("/backup/")
    return render_template('login.html')


@app.route('/backup/', methods=['POST', 'GET'])
def backup():
    if request.method == 'POST':
        username = request.form.get('username')
        if username == "":
            return "Введите логин!"

        password2 = request.form.get('password2')
        if password2 == "":
            return "Введите пароль!"

        try:
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password2=%s",
                           (str(username), str(password2)))
            records = list(cursor.fetchall())
            return render_template('backuppassword.html', full_name=records[0][1], login=records[0][2], password2=records[0][4])
        except Exception as E:
            print(E)
            return "Вас нет в базе данных!"
    return render_template('backup.html')


if __name__ == '__main__':
    app.run(debug=True)