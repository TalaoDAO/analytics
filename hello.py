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

@app.route('/transactions')
def transactions():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()

   try:

      cur.execute('select * from transactions where datetime(date) < date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+str(int(request.args.get('day'))+1)+'") and datetime(date) > date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+request.args.get('day')+'")')
      rows = cur.fetchall()
      return render_template("transactions.html",rows = rows,year=request.args.get('year'),month=request.args.get('month'),day=request.args.get('day'))
   except TypeError:
      pass
   
   cur.execute("select * from transactions")
   
   rows = cur.fetchall()
   return render_template("transactions.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)