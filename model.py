from audioop import add
import sqlite3 as sql
try:
    sql.connect("database.db").cursor().execute("CREATE TABLE IF NOT EXISTS vouchers (id INTEGER PRIMARY KEY, discount INTEGER, expiration DATE, benefit INTEGER)")
    sql.connect("database.db").cursor().execute("CREATE TABLE IF NOT EXISTS usersWVouchers (id INTEGER PRIMARY KEY, idVoucher INTEGER, addressUser TEXT)")
    sql.connect("database.db").cursor().execute("CREATE TABLE IF NOT EXISTS transactions (hash TEXT PRIMARY KEY, relativeTo INTEGER,userAddress TEXT , smartContractAddress TEXT, amount INTEGER,date TEXT)")
except:
    None    

def addVoucher():
    try:
        id=input("id:")
        discount=input("discount:")
        expiration=input("expiration:")
        benefit=input("benefit:")
        with sql.connect("database.db") as con:
            cur = con.cursor()
                    
            cur.execute("INSERT INTO vouchers (id,discount,expiration,benefit) VALUES (?,?,?,?)",(id,discount,expiration,benefit) )
                    
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print(msg)

def addVoucherUser():  
    try:
        id=input("id:")
        idVoucher=input("idVoucher:")
        address=input("address:")
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO usersWVouchers (id,idVoucher,addressUser) VALUES (?,?,?)",(id,idVoucher,address) )
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print(msg)
def eligible():
    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("select addressUser,idVoucher from usersWVouchers where idVoucher in ( select id from vouchers where date(expiration) >= date('now')) ")

        rows = cur.fetchall()
        #print(rows)
        result={}
        for row in rows:
            #print(row[0])
            result[row[0]]=row[1]
        return result
def addTx(hash,relativeTo,userAddress,smartContractAddress,amount,date):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO transactions (hash,relativeTo,userAddress,smartContractAddress,amount,date) VALUES (?,?,?,?,?,?)",(hash,relativeTo,userAddress,smartContractAddress,amount,date) )
            con.commit()
            msg = "tx successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print(msg)

def cli():
    print("start")
    toDo=input("cmd : ")
    if(toDo=="av"):
        addVoucher()
    if(toDo=="avu"):
        addVoucherUser()
    if(toDo=="e"):
        print(eligible())
