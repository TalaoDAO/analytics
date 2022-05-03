from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template("home.html")



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
      year=request.args.get('year')
      month=request.args.get('month')
      day=request.args.get('day')
      if(int(day)<10):
         day="0"+str(int(request.args.get('day'))+1)
      else:
         day=str(int(request.args.get('day'))+1)
      cur.execute('select * from transactions where datetime(date) < date("'+year+'-'+month+'-'+day+'") and datetime(date) > date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+request.args.get('day')+'")')
      print('select * from transactions where datetime(date) < date("'+year+'-'+month+'-'+day+'") and datetime(date) > date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+request.args.get('day')+'")')
      rows = cur.fetchall()
      return render_template("transactions.html",rows = rows,year=request.args.get('year'),month=request.args.get('month'),day=request.args.get('day'))
   except TypeError:
      pass
   
   cur.execute("select * from transactions")
   
   rows = cur.fetchall()
   return render_template("transactions.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)