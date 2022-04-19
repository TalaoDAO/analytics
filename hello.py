from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template("home.html")


@app.route('/vouchers')
def vouchers():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from vouchers")
   
   rows = cur.fetchall()
   return render_template("vouchers.html",rows = rows)

@app.route('/usersvouchers')
def usersWvouchers():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from usersWVouchers")
   
   rows = cur.fetchall()
   return render_template("usersWVouchers.html",rows = rows)
if __name__ == '__main__':
   app.run(debug = True)