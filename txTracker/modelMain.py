import sqlite3 as sql
from datetime import datetime
from environment import DBPATH
import logging
logging.basicConfig(level=logging.INFO)

try:
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS usersWVouchers (id INTEGER PRIMARY KEY, addressUser TEXT, expiration DATE, discount INTEGER, benefitAffiliate INTEGER, benefitAffiliateType TEXT, affiliate TEXT)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS transactions (hash TEXT PRIMARY KEY, relativeTo INTEGER,userAddress TEXT , smartContractAddress TEXT, amount INTEGER,date TEXT, refunded NUMBER, forAffiliate NUMBER,currency TEXT)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS payements (prio NUMBER PRIMARY KEY,hash TEXT, address TEXT, applied TEXT, forWho TEXT, amount INTEGER,date TEXT,hashPayement TEXT,currency TEXT)")
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS FeeTracker (hash TEXT PRIMARY KEY, addressUser TEXT, date DATE,amount INTEGER,currency TEXT)")
    sql.connect(DBPATH).cursor().execute("drop table didToAddresses")

    
    sql.connect(DBPATH).cursor().execute("CREATE TABLE IF NOT EXISTS didToAddresses (did TEXT, addresses TEXT)")
    max =sql.connect(DBPATH).cursor().execute("select max(prio) from payements ").fetchone()
    if not max[0] :
        logging.info("no payements")
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
            logging.info("msg db %s",msg)
except:
    logging.warning("error DB")
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
        logging.info("msg db %s", msg)


def eligible():
    with sql.connect(DBPATH) as conn:
        cur = conn.cursor()
        cur.execute("select addressUser,(max(cast(substr(discount,1,length(discount)-1) as INTEGER))) as discount,id,benefitAffiliate,benefitAffiliateType,affiliate from usersWVouchers where date(expiration) > date('now') group by addressUser;")
        rows = cur.fetchall()
        return rows


def isEligible(address):
    with sql.connect(DBPATH) as conn:
        cur = conn.cursor()
        cur.execute("""select addressUser,(max(cast(substr(discount,1,length(discount)-1) as INTEGER))) as discount,id,benefitAffiliate,benefitAffiliateType,affiliate from usersWVouchers where date(expiration) > date('now') and (( SELECT count(*) from (select seq from (WITH RECURSIVE split(seq, word, str) AS (SELECT 0, ',', substr(addressUser,2,length(addressUser)-2)||','UNION ALL SELECT seq+1,substr(str, 0, instr(str, ',')),substr(str, instr(str, ',')+1)FROM split WHERE str != '') SELECT * FROM split ORDER BY split.seq ASC) where word=" '"""+address+"""'" or word="'"""+address+"""'")) or addressUser='"""+address+"""'  or addressUser="['"""+address+"""']");""")
        rows = cur.fetchall()
        return rows


def addTx(hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate,currency):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO transactions (hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate,currency) VALUES (?,?,?,?,?,?,?,?,?)",(hash,relativeTo,userAddress,smartContractAddress,amount,date,refunded,forAffiliate,currency) )
            con.commit()
            msg = "tx successfully added"
    except:
        con.rollback()
        msg = "error in insert operation" 
    finally:
        con.close()
        logging.info("msg db %s", msg)


def addPayement(hash,address,forWho,amount,currency):
    text = "trying to add payement with "+str(hash)+" "+str(address)+" "+str(forWho)+" "+str(amount)+" "+str(currency)
    logging.info(text)
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select max(prio) from payements ")
            max = cur.fetchone()
            cur = con.cursor()
            cur.execute("INSERT INTO payements (hash,prio,address,applied,forWho,amount,currency) VALUES (?,?,?,?,?,?,?)",(hash,max[0]+1,address,False,forWho,amount,currency) )
            con.commit()
            msg = "payement successfully added"
    except sql.Error as er:
        logging.error('SQLite error: %s', ' '.join(er.args))
    finally:
        logging.info(msg)
        con.close()

def setPayementDone(prio,hash,date):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            now = datetime.now()
            cur.execute("update payements set applied=1,hashPayement='"+hash+"',date='"+now.strftime("%d/%m/%Y %H:%M:%S")+"' where prio="+str(prio))
            con.commit()
    except sql.Error as er:
        logging.error('SQLite error: %s', ' '.join(er.args))
    finally:
        con.close()


def cli():
    logging.info("start")
    toDo=input("cmd : ")
    if toDo=="avu":
        addVoucherUser()
    elif toDo=="e":
        logging.info(eligible())
    elif toDo=="p" :
        logging.info(getPayementPrio())
    elif toDo=="t":
        logging.info(isUserTracked("tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"))


def getPayementPrio():
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select address,amount,hash,prio,currency from payements where prio=(select min(prio) from payements where applied=0 and forWho='player' and length(address)=36) ")
            max = cur.fetchone()
            #if(max==None):
                #cur.execute("select address,amount,hash,prio from payements where prio=(select min(prio) from payements where applied=0 and forWho='affiliate' and length(address)=36) ")
                #max = cur.fetchone()
            return max
    except:
        try:
            con.rollback()
        except:
            pass        
    finally:
        try:
            con.close()
        except:
            pass


def isUserTracked(address):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select addressUser from usersWVouchers where addressUser='"+address+"'")
            res = cur.fetchall()
            logging.info("res %s",str(res))
            if not len(res):
                return False
            return True
    except sql.Error as er:
                    con.rollback()
                    logging.error('SQLite error: %s',' '.join(er.args))
    finally:
        con.close()


def isPayementAdded(hash):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select prio from payements where hash='"+hash+"'")
            res = cur.fetchall()
            logging.info("res %s", str(res))
            if not len(res):
                return False
            return True
    except sql.Error as er:
                    con.rollback()
                    logging.error('SQLite error: %s', ' '.join(er.args))
    finally:
        con.close()


def isFeeAdded(hash):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select date from FeeTracker where hash='"+hash+"'")
            res = cur.fetchall()
            logging.info("res %s", str(res))
            if not len(res):
                return False
            return True
    except sql.Error as er:
                    con.rollback()
                    logging.error('SQLite error: %s', ' '.join(er.args))    
    finally:
        con.close()


def getAddressFromMail(mail):
    try:
        with sql.connect(DBPATH) as con:
            cur = con.cursor()
            cur.execute("select addressUser from usersWVouchers where email='"+mail+"'")
            res = cur.fetchall()
            if not len(res) :
                return None
            return res[0][0]
    except:
        con.rollback()        
    finally:
        try:
            con.close()
        except:
            pass


def addFee(hash,address,date,amount):
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
        logging.info("msg db %s", str(msg))



"""select sum(amount) from (select * from payements where forWho="affiliate" and amount !="2%" and address="tz1P3zm6rgzfYM3xHLv4xm9bQbQ5A74oid39")  union select prio from payements where forWho="affiliate" and amount !="2%" and address="tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg5555";
select * from payements"""
isEligible("tz1LK2aE2zmvqqsVYGAaCTauz7peWQ3gAuqK")

"""select addressUser,(max(cast(substr(discount,1,length(discount)-1) as INTEGER))) as discount,id,benefitAffiliate,benefitAffiliateType,affiliate from usersWVouchers where date(expiration) > date('now') and (( SELECT count(*) from (select seq from (WITH RECURSIVE split(seq, word, str) AS (
    SELECT 0, ',', substr(addressUser,2,length(addressUser)-2)||','
    UNION ALL SELECT
        seq+1,
        substr(str, 0, instr(str, ',')),
        substr(str, instr(str, ',')+1)
    FROM split WHERE str != ''
) SELECT * FROM split ORDER BY split.seq ASC) where word=" 'tz1Z3kDJEQJbd91eoJUWRtV83bjFYUX7Lbwf'")) or addressUser='tz1Z3kDJEQJbd91eoJUWRtV83bjFYUX7Lbwf');"""