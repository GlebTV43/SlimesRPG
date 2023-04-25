from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    con_user = sqlite3.connect("users.db")
    cur_user = con_user.cursor()
    all_rating = cur_user.execute(f"SELECT User_Name, Rating, Experience FROM Users").fetchall()
    all_rating.sort(key=lambda x: x[1], reverse=True)
    if len(all_rating) >= 3:
        for i in range(3):
            print(all_rating[i])
    else:
        for i in all_rating:
            print(i)
    return render_template("index1.html", data=all_rating)


if __name__ == '__main__':
    app.run(port=8080, host='185.185.71.200')
