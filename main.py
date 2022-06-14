from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify, request, Response,session
from flask_qrcode import QRcode
from datetime import timedelta
import didkit
import redis
import socket
import uuid
import json
import sys
import sqlite3 as sql
import asyncio
from pprint import pprint
import model

app = Flask(__name__)
app.config.from_object(__name__)
app.permanent_session_lifetime = timedelta(minutes=15)
qrcode = QRcode(app)
PORT = 3000
app.secret_key = "1269a3845acac85161e11e51e098ac6be52926635348e1c1c2ca23c141e3179b"


async def verifyPresentation(vc):
    verif = await didkit.verify_presentation(vc, '{}')
    return verif

@app.route('/analytics/')
def home():
    if (session.get('logged')=="True"):
        addressSelector=''
        if(session.get('user')=="admin"):
            addressSelector='''<div><input class="button" type="button" onclick="location.href='/payements?address='+addressToSee.value" value="Select address" /><input  type="text" id="addressToSee" ></div>'''
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()

            try:  
                address=request.args.get('address')
                cur.execute("select * from payements where address='"+address+"'") 
                rows = cur.fetchall()
                return render_template("home.html",rows = rows,addressSelector=addressSelector,addressTezos="admin") 
            except TypeError:
                pass
            
            cur.execute("select * from payements")  
            rows = cur.fetchall()
            return render_template("home.html",rows = rows)
        else:
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from payements where address='"+session.get('user')+"'") 
            rows = cur.fetchall() 
            cur.execute("select * from transactions where userAddress='"+session.get('user')+"'")
            rows2 = cur.fetchall()
            """for row in rows:
                if(row[3]==1):
                    row[3]="done"
                else:
                    row[3]="pending"""
            return render_template("home.html",rows = rows,rows2=rows2,addressSelector=addressSelector,usersWVouchers="hidden",addressTezos=session.get("user")) 
            
    else:
        return redirect(url_for('login'))


@app.route('/analytics/usersvouchers')
def usersWvouchers():
    try:
        if (session.get('logged')=="True"):
            if(session.get('user')=="admin"):
                con = sql.connect("database.db")
                con.row_factory = sql.Row
            
                cur = con.cursor()
                cur.execute("select * from usersWVouchers")
                
                rows = cur.fetchall()
                return render_template("usersWVouchers.html",rows = rows)
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    except KeyError:
        return redirect(url_for('login'))
    except TypeError:
        return redirect(url_for('login'))

@app.route('/analytics/logout', methods=['GET', 'POST'])
def logout():
    session['logged']=False
    session['user']=None
    return redirect(url_for('login'))

@app.route('/analytics/transactions')
def transactions():
    if (session.get('logged')=="True"):
        if(session.get('user')=="admin"):
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
        else:
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
                print('select * from transactions where datetime(date) < date("'+year+'-'+month+'-'+day+'") and datetime(date) > date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+request.args.get('day')+'") and userAddress='+session.get('user'))
                cur.execute('select * from transactions where datetime(date) < date("'+year+'-'+month+'-'+day+'") and datetime(date) > date("'+request.args.get('year')+'-'+request.args.get('month')+'-'+request.args.get('day')+'") and userAddress="'+session.get('user')+'"')
                rows = cur.fetchall()
                return render_template("transactions.html",rows = rows,year=request.args.get('year'),month=request.args.get('month'),day=request.args.get('day'))
            except TypeError:
                pass
            
            cur.execute("select * from transactions where userAddress='"+session.get('user')+"'")
            
            rows = cur.fetchall()
            return render_template("transactions.html",rows = rows)
    else:
        return redirect(url_for('login'))

@app.route('/analytics/payements')
def payements():
    if (session.get('logged')=="True"):
        addressSelector=''
        if(session.get('user')=="admin"):
            addressSelector='''<div><input class="button" type="button" onclick="location.href='/payements?address='+addressToSee.value" value="Select address" /><input  type="text" id="addressToSee" ></div>'''
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()

            try:  
                address=request.args.get('address')
                cur.execute("select * from payements where address='"+address+"'") 
                rows = cur.fetchall()
                return render_template("payements.html",rows = rows,addressSelector=addressSelector) 
            except TypeError:
                pass
            
            cur.execute("select * from payements")  
            rows = cur.fetchall()
            return render_template("payements.html",rows = rows)
        else:
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from payements where address='"+session.get('user')+"'") 
            rows = cur.fetchall()
            return render_template("payements.html",rows = rows,addressSelector=addressSelector) 
            
    else:
        return redirect(url_for('login'))

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

red= redis.Redis(host='127.0.0.1', port=6379, db=0)
OFFER_DELAY = timedelta(seconds= 10*60)
did_verifier = 'did:tz:tz2NQkPq3FFA3zGAyG8kLcWatGbeXpHMu7yk'
# pattern pour https://w3c-ccg.github.io/vp-request-spec/#query-by-example
pattern = {"type": "VerifiablePresentationRequest",
            "query": [
                {
                    "type": "QueryByExample",
                    "credentialQuery": []
                }]
            }

@app.route('/analytics/login' , methods=['GET'], defaults={'red' : red}) 
def login(red):
    id = str(uuid.uuid1())
    pattern['challenge'] = str(uuid.uuid1()) # nonce
    IP=extract_ip()
    pattern['domain'] = 'http://' + IP
    # l'idee ici est de créer un endpoint dynamique
    red.set(id,  json.dumps(pattern))
    #url = 'http://' + IP + ':' + str(PORT) +  '/analytics/endpoint/' + id +'?issuer=' + did_verifier
    url = 'https://talao.co/analytics/endpoint/' + id +'?issuer=' + did_verifier
    html_string = """  <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <center>
            <div>  
                <h2>Scan the QR Code bellow with your smartphone wallet</h2> 
                <br>  
                <div><img src="{{ qrcode(url) }}" ></div>
            </div>
        </center>
        <script>
            var source = new EventSource('/analytics/verifier_stream');
            source.onmessage = function (event) {
                const result = JSON.parse(event.data);
                console.log(result.message);
                if (result.check == 'ok' & result.id == '{{id}}'){
                    window.location.href="/analytics/followup?id={{id}}";
                }
                else { 
                    window.alert(result.message);
                    window.location.href="/analytics/";
                }
            };
        </script>
        </body>
        </html>"""
    return render_template_string(html_string, url=url, id=id)

@app.route('/analytics/endpoint/<id>', methods = ['GET', 'POST'],  defaults={'red' : red})
def presentation_endpoint(id, red):
    try :
        my_pattern = json.loads(red.get(id).decode())
    except :
        event_data = json.dumps({"id" : id,
                                 "message" : "redis decode failed",
                                 "check" : "ko"})
        red.publish('verifier', event_data)
        return jsonify("server error"), 500
    
    if request.method == 'GET':
        return jsonify(my_pattern)
    
    if request.method == 'POST' :
        #red.delete(id)
        try : 
            result = json.loads(asyncio.run(verifyPresentation(request.form['presentation'])))['errors']
        except:
            print("except")
            event_data = json.dumps({"id" : id,
                                    "check" : "ko",
                                    "message" : "presentation is not correct"})
            red.publish('verifier', event_data)
            return jsonify("presentation is not correct"), 403
        if result :
            print("result")
            event_data = json.dumps({"id" : id,
                                    "check" : "ko",
                                    "message" : result})
            red.publish('verifier', event_data)
            return jsonify(result), 403
        # mettre les tests pour verifier la cohérence entre issuer, holder et credentialSubject.id 
        # 
        red.set(id,  request.form['presentation'])
        event_data = json.dumps({"id" : id,
                                "message" : "presentation is verified",
                                "check" : "ok"})           
        red.publish('verifier', event_data)
        
        #return redirect("/")
        return jsonify("ok"), 200

# server event push, peut etre remplacé par websocket
@app.route('/analytics/verifier_stream', methods = ['GET'],  defaults={'red' : red})
def presentation_stream(red):
    def event_stream(red):
        pubsub = red.pubsub()
        pubsub.subscribe('verifier')
        for message in pubsub.listen():
            if message['type']=='message':
                yield 'data: %s\n\n' % message['data'].decode()
    headers = { "Content-Type" : "text/event-stream",
                "Cache-Control" : "no-cache",
                "X-Accel-Buffering" : "no"}
    return Response(event_stream(red), headers=headers)


# uniquement pour l affichage du VP/VC, inutile sinon
@app.route('/analytics/followup', methods = ['GET', 'POST'],  defaults={'red' : red})
def followup(red):  
    print("accessing followup")
    try :  
        presentation = json.loads(red.get(request.args['id']).decode())
    except :
        print('redis problem')
        sys.exit()
    red.delete(request.args['id'])
    holder = presentation['holder']
    # pour prendre en compte une selection multiple ou unique
    if isinstance(presentation['verifiableCredential'], dict) :
        nb_credentials = "1"
        issuers = presentation['verifiableCredential']['issuer']
        types = presentation['verifiableCredential']['type'][1]
        credential = json.dumps(presentation['verifiableCredential'], indent=4, ensure_ascii=False)
    else :
        nb_credentials = str(len(presentation['verifiableCredential']))
        issuer_list = type_list = list()
        for credential in presentation['verifiableCredential'] :
            if credential['issuer'] not in issuer_list :
                issuer_list.append(credential['issuer'])
            if credential['type'][1] not in type_list :
                type_list.append(credential['type'][1])
        issuers = ", ".join(issuer_list)
        types = ", ".join(type_list)
        # on ne presente que le premier
        credential = json.dumps(presentation['verifiableCredential'][0], indent=4, ensure_ascii=False)
    presentation = json.dumps(presentation, indent=4, ensure_ascii=False)
    dictionnaire=json.loads(credential)
    pprint(presentation)
    session["logged"]= "True"
    typeCredential=dictionnaire["type"][1]
    if(typeCredential=="EmailPass"):
        email=dictionnaire["credentialSubject"]["email"]
        if (email=="nicolas.muller@talao.io" or email=="thierry.thevenet@talao.io"):
            session["user"]="admin"
            return redirect("/analytics")
        address=model.getAddressFromMail(email)
        session["user"]=address
        print(address)
        print(session.get("user"))
        if(address=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            session["user"]="admin"
    if(typeCredential=="TalaoCommunity"):
        print(dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"])
        
        session["user"]=dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"]
        if (dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"]=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            #session["user"]="admin"
            session["user"]="admin"
    if(typeCredential=="TezosAssociatedWallet"):      
        session["user"]=dictionnaire["credentialSubject"]["correlation"][0]
        print(session.get("user"))
    #print("logged in "+session.get("user"))
    print(session.get("user"))
    return redirect("/analytics")

@app.route('/analytics/api/newvoucher', methods = ['POST'])
def newvoucher():
    try:
        vc=json.loads(request.get_data())
        key = request.headers.get('key')
        if (key=="SECRET_KEY"):
            adressUser=vc["credentialSubject"]["associatedAddress"]["blockchainTezos"]
            expiration=vc["credentialSubject"]["offers"][0]["endDate"]
            discount=vc["credentialSubject"]["offers"][0]["benefit"]["discount"]
            benefitAffiliate=vc["credentialSubject"]["affiliate"]["benefit"]["incentiveCompensation"]
            benefitAffiliateType=vc["credentialSubject"]["affiliate"]["benefit"]["category"]
            affiliate=vc["credentialSubject"]["affiliate"]["paymentAccepted"]["blockchainAccount"]
            try:
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO usersWVouchers (addressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) VALUES (?,?,?,?,?,?)",(adressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) )
                    con.commit()
                    msg = "usersWVoucher successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"
                
            finally:
                con.close()
                print(msg)
                return jsonify("ok"), 200
        else:
            return jsonify("Forbidden"), 403
    except KeyError:
        return jsonify("error"),404

if __name__ == '__main__':
    # to get the local server IP 
    IP = extract_ip()
    # server start
    app.run(host = IP, port= 3000, debug=True)