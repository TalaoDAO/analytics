from audioop import add
import sqlite3 as sql
import traceback
import sys
from datetime import datetime

#DBPATH="/home/achille/analytics/database.db"
DBPATH="/home/achille1017/prog/tezotopia/database.db"


try:
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS usersWVouchers (id INTEGER PRIMARY KEY, addressUser TEXT, expiration DATE, discount INTEGER, benefitAffiliate INTEGER, benefitAffiliateType TEXT, affiliate TEXT)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS transactions (hash TEXT PRIMARY KEY, relativeTo INTEGER,userAddress TEXT , smartContractAddress TEXT, amount INTEGER,date TEXT, refunded NUMBER, forAffiliate NUMBER)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS payements (prio NUMBER PRIMARY KEY,hash TEXT, address TEXT, applied TEXT, forWho TEXT, amount INTEGER,date TEXT,hashPayement TEXT)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS FeeTracker (hash TEXT PRIMARY KEY, addressUser TEXT, date DATE,amount INTEGER)")
    max =sql.connect(DBPATH).cursor().execute("select max(prio) from payements ").fetchone()
    print(max[0])
    if(max[0]==None):
        print("no payements")
        try:
            with sql.connect(DBPATH) as con:
                cur = con.cursor()
                cur.execute("insert into payements values (0,0,0,0,0,0,0,0)" )
                con.commit()
                msg = "new payement added "
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            con.close()
            print("msg db "+str(msg))
except:
    None    


def addVoucherUser():  
    try:
        id=input("id:")
        idVoucher=input("idVoucher:")
        address=input("address:")
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO usersWVouchers (id,idVoucher,addressUser) VALUES (?,?,?)",(id,idVoucher,address) )
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print("msg db "+str(msg))
def eligible():
    with sql.connect(DBPATH) as conn:
        cur = conn.cursor()
        cur.execute("select addressUser,discount,id,benefitAffiliate,benefitAffiliateType,affiliate from usersWVouchers where date(expiration) > date('now')")

        rows = cur.fetchall()
        print("eligibles :")
        print(rows)
        return rows
def addTx(hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate):
    eligible()
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO transactions (hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate) VALUES (?,?,?,?,?,?,?,?)",(hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate) )
            con.commit()
            msg = "tx successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print("msg db "+str(msg))
def addPayement(hash,address,forWho,amount):
    print("trying to add payement with "+str(hash)+" "+str(address)+" "+str(forWho)+" "+str(amount))
    sys.stdout.flush()
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select max(prio) from payements ")
            max = cur.fetchone()
            cur = con.cursor()
            cur.execute("INSERT INTO payements (hash,prio,address,applied,forWho,amount) VALUES (?,?,?,?,?,?)",(hash,max[0]+1,address,False,forWho,amount) )
            con.commit()
            msg = "payement successfully added"
    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        sys.stdout.flush()
        print("Exception class is: ", er.__class__)
        sys.stdout.flush()
        print('SQLite traceback: ')
        sys.stdout.flush()
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        sys.stdout.flush()
    finally:
        print(msg)
        sys.stdout.flush()
        con.close()

def setPayementDone(prio,hash,date):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            print("update payements set applied=1,hashPayement='"+hash+"' where prio="+str(prio))
            now = datetime.now()
            cur.execute("update payements set applied=1,hashPayement='"+hash+"',date='"+now.strftime("%d/%m/%Y %H:%M:%S")+"' where prio="+str(prio))
            con.commit()

    except sql.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        con.close()
def cli():
    print("start")
    toDo=input("cmd : ")
    if(toDo=="avu"):
        addVoucherUser()
    if(toDo=="e"):
        print(eligible())
    if(toDo=="p"):
        print(getPayementPrio())
    if(toDo=="t"):
        print(isUserTracked("tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"))
def getPayementPrio():
    try:
        with sql.connect(DBPATH) as con:
            #print("try")
            cur = con.cursor()
            cur.execute("select address,amount,hash,prio from payements where prio=(select min(prio) from payements where applied=0 and forWho='player') ")
            max = cur.fetchone()
            """if(max==None):
                cur.execute("select address,amount,hash,prio from payements where prio=(select min(prio) from payements where applied=0 and forWho='affiliate') ")
                max = cur.fetchone()"""
            return max
    except:
        con.rollback()        
    finally:
        con.close()
def isUserTracked(address):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select addressUser from usersWVouchers where addressUser='"+address+"'")
            #print("select addressUser from usersWVouchers where addressUser='"+address+"'")
            res = cur.fetchall()
            print("res "+str(res))
            if(len(res)==0):
                return False
            return True
    except sql.Error as er:
                    con.rollback()
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    print('SQLite traceback: ')
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    print(traceback.format_exception(exc_type, exc_value, exc_tb))
                    msg="error"       
    finally:
        con.close()
def getAddressFromMail(mail):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select addressUser from usersWVouchers where email='"+mail+"'")
            res = cur.fetchall()
            if(len(res)==0):
                return None
            return res[0][0]
    except:
        con.rollback()        
    finally:
        con.close()
def addFee(hash,address,date,amount):
    print("trying to add fee with "+str(hash)+" "+str(address)+" "+str(date)+" "+str(amount))
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO feeTracker (hash,addressUser,date,amount) VALUES (?,?,?,?)",(hash,address,date,amount) )
            con.commit()
            msg = "fee successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
        
    finally:
        con.close()
        print("msg db "+str(msg))

eligible()
isUserTracked("tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im")

"""select sum(amount) from (select * from payements where forWho="affiliate" and amount !="2%" and address="tz1P3zm6rgzfYM3xHLv4xm9bQbQ5A74oid39")  union select prio from payements where forWho="affiliate" and amount !="2%" and address="tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg5555";
select * from payements"""
