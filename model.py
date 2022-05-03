from audioop import add
import sqlite3 as sql
try:
    sql.connect("database.db").cursor().execute("CREATE TABLE IF NOT EXISTS usersWVouchers (id INTEGER PRIMARY KEY, idVoucher INTEGER, addressUser TEXT, expiration DATE, discount INTEGER, benefitInfluencer INTEGER)")
    sql.connect("database.db").cursor().execute("CREATE TABLE IF NOT EXISTS transactions (hash TEXT PRIMARY KEY, relativeTo INTEGER,userAddress TEXT , smartContractAddress TEXT, amount INTEGER,date TEXT)")
except:
    None    


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
        cur.execute("select addressUser,discount,id from usersWVouchers where date(expiration) > date('now')")

        rows = cur.fetchall()
        #print(rows)
        return rows
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
    if(toDo=="avu"):
        addVoucherUser()
    if(toDo=="e"):
        print(eligible())
