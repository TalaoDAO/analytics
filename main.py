from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify, request, Response,session,send_file
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
import traceback
from pprint import pprint
import json
from flask_mobility.decorators import mobilized

with open('keys.json') as mon_fichier:
    data = json.load(mon_fichier)

app = Flask(__name__)
app.config.from_object(__name__)
app.permanent_session_lifetime = timedelta(minutes=15)
qrcode = QRcode(app)
PORT = 3000
app.secret_key = "1269a3845acac85161e11e51e098ac6be52926635348e1c1c2ca23c141e3179b"
DBPATH="/home/achille/analytics/database.db"
#DBPATH="/home/achille1017/prog/tezotopia/database.db"


async def verifyPresentation(vc):
    verif = await didkit.verify_presentation(vc, '{}')
    print(verif)
    return verif

@app.route('/analytics/')
def home():
    if (session.get('logged')=="True"):
        addressSelector=''
        if(session.get('user')=="admin"):
            addressSelector='''<div><input class="button" type="button" onclick="location.href='/payements?address='+addressToSee.value" value="Select address" /><input  type="text" id="addressToSee" ></div>'''
            con = sql.connect(DBPATH)
            con.row_factory = sql.Row
            cur = con.cursor()

            try:  
                address=request.args.get('address')
                cur.execute("select * ,CASE WHEN applied =0 THEN 'pending' ELSE 'done' END AS status from (select a.relativeTo,a.hash,a.amount/1000000 as amount,datetime(a.date) as date,b.applied,b.address,b.amount as 'amountDiscount' ,b.hashPayement,c.discount from transactions a, payements b, (select discount,id from usersWVouchers) c where a.hash=b.hash and c.id=a.relativeTo and b.forWho='player')") 
                rows = cur.fetchall()
                print("rows   --------0")
                sys.stdout.flush()
                print(rows[0])
                sys.stdout.flush()
                return render_template("home.html",rows = rows,addressSelector=addressSelector,addressTezos="admin") 
            except TypeError:
                pass
            
            cur.execute("select * from payements")  
            rows = cur.fetchall()
            print("rows   --------1")
            sys.stdout.flush()
            print(rows)
            sys.stdout.flush()
            return render_template("home.html",rows = rows)
        else:
            con = sql.connect(DBPATH)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * ,CASE WHEN applied =0 THEN 'pending' ELSE 'done' END AS status from (select a.relativeTo,a.hash,a.amount/1000000 as amount,datetime(a.date) as date,b.applied,b.address,b.amount as 'amountDiscount' ,b.hashPayement,c.discount from transactions a, payements b, (select discount,id from usersWVouchers) c where a.hash=b.hash and c.id=a.relativeTo and b.forWho='player' and address='"+session.get('user')+"')") 
            rows = cur.fetchall() 
            print("rows   --------2")
            sys.stdout.flush()
#            print(rows[0])
            sys.stdout.flush()

            return render_template("home.html",rows = rows,addressSelector=addressSelector,usersWVouchers="hidden",addressTezos=session.get("user")) 
            
    else:
        return redirect(url_for('login'))


@app.route('/analytics/usersvouchers')
def usersWvouchers():
    try:
        if (session.get('logged')=="True"):
            if(session.get('user')=="admin"):
                con = sql.connect(DBPATH)
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

@app.route('/analytics/style' , methods=['GET'])
def style():
	return send_file('./static/style.css', attachment_filename='style.css')

@app.route('/analytics/static/logo',methods=['GET'])
def logo():
	return send_file('./static/Logo.png', attachment_filename='Logo.png')

@app.route('/analytics/static/background',methods=['GET'])
def background():
	return send_file('./static/tezotopia-space.png', attachment_filename='tezotopia-space.png')

@app.route('/analytics/static/font',methods=['GET'])
def font():
	return send_file('./static/Rubik-Regular.ttf', attachment_filename='Rubik-Regular.ttf')

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
        <head>       <link rel="stylesheet" href="https://talao.co/analytics/style"><!--https://talao.co/analytics/style {{url_for('static', filename = 'style.css')}}-->
      </head>
        <body>
        <center>
            <div>  

      <img  src="../analytics/static/logo">
                <br>
                
                <div id="access">
                <p >from Desktop</p>
                </div>
                <p id="connect">Connect with your email pass, your Tezotopia voucher or membership card</p>
                <br><br>
                <p id="scan">Scan the QR Code bellow with your smartphone wallet</p5> 
                <br>  
                <div><img id="qrcode" src="{{ qrcode(url) }}" ></div>
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

@app.route('/analytics/login' , methods=['GET'], defaults={'red' : red}) 
@mobilized(login(red))
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
        <head>       <link rel="stylesheet" href="https://talao.co/analytics/style"><!--https://talao.co/analytics/style {{url_for('static', filename = 'style.css')}}-->
      </head>
        <body>
        <center>
            <div>  

      <img  src="../analytics/static/logo">
                <br>
                
                <div id="access">
                <p >from Mobile</p>
                </div>
                <p id="connect">Connect with your email pass, your Tezotopia voucher or membership card</p>
                <br><br>
                <p id="scan">Scan the QR Code bellow with your smartphone wallet</p5> 
                <br>  
                <div><img id="qrcode" src="{{ qrcode(url) }}" ></div>
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
        #pprint("my_pattern "+str(my_pattern))
    except :
        event_data = json.dumps({"id" : id,
                                 "message" : "redis decode failed",
                                 "check" : "ko"})
        red.publish('verifier', event_data)
        #pprint("event data "+str(event_data))
        return jsonify("server error"), 500
    
    if request.method == 'GET':
        #pprint("my_pattern "+str(my_pattern))

        return jsonify(my_pattern)
    
    if request.method == 'POST' :
        #red.delete(id)
        try : 
            pprint(request.form['presentation'])
            #result = json.loads(asyncio.run(verifyPresentation(request.form['presentation'])))
            result=False
            print("result "+str(result))
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
    #print(presentation)
    
    typeCredential=dictionnaire["type"][1]
    print("type credential : "+typeCredential)

    if(typeCredential=="EmailPass"):
        #print("presentation " +str(presentation))
        email=dictionnaire["credentialSubject"]["email"]
        print("email "+str(email))
        if (email=="nicolas.muller@talao.io" or email=="thierry.thevenet@talao.io" or email=="achillerondo@gmail.com" or email=="denis@altme.io" or email=="hugo@altme.io" or email=="achillemarseille@gmail.com"):
            session["logged"]= "True"
            session["user"]="admin"
            return redirect("/analytics")
        else:
            return redirect(url_for('login'))

    if(typeCredential=="TalaoCommunity"):
        #print(dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"])
        session["user"]=dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"]
        if (dictionnaire["credentialSubject"]["associatedAddress"][0]["blockchainAccount"]=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            #session["user"]="admin"
            session["logged"]= "True"
            session["user"]="admin"

    if(typeCredential=="TezVoucher_1"):
        session["user"]=dictionnaire["credentialSubject"]["associatedAddress"]["blockchainTezos"]
        session["logged"]= "True"
        if (session.get("user")=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            session["user"]="admin"

    if(typeCredential=="MembershipCard_1"):
        session["user"]=dictionnaire["credentialSubject"]["associatedAddress"]["blockchainTezos"]
        session["logged"]= "True"
        if (session.get("user")=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            session["user"]="admin"
            
    """if(typeCredential=="TezosAssociatedWallet"):   
        print("presentation " +str(presentation))   
        session["logged"]= "True"
        session["user"]=dictionnaire["credentialSubject"]["correlation"][0]
        if(dictionnaire["credentialSubject"]["correlation"][0]=="tz1ReP6Pfzgmcwm9rTzivdJwnmQm4KzKS3im"):
            session["user"]="admin"
        print("user "+session.get("user"))"""
    #print("logged in "+session.get("user"))
    #print(session.get("user"))
    return redirect("/analytics")

@app.route('/analytics/api/newvoucher', methods = ['POST'])
def newvoucher():
    try:
        vc=json.loads(request.get_data())
        key = request.headers.get('key')
        if (key=="SECRET_KEY" or key==data.get('apiKey')):
            print(vc)
            if(vc["credentialSubject"]["type"]=="MembershipCard_1"):
                print("MembershipCard_1")
                adressUser=vc["credentialSubject"]["associatedAddress"]["blockchainTezos"]
                expiration=vc["expirationDate"]
                try:
                    discount=vc["credentialSubject"]["offers"][0]["benefit"]["discount"]
                except:
                    discount=vc["credentialSubject"]["offers"]["benefit"]["discount"]
                benefitAffiliate=None
                benefitAffiliateType=None
                affiliate=None
                try:
                    with sql.connect(DBPATH) as con:
                        cur = con.cursor()
                        print("INSERT INTO usersWVouchers (addressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) VALUES (?,?,?,?,?,?)",(adressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate))
                        cur.execute("INSERT INTO usersWVouchers (addressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) VALUES (?,?,?,?,?,?)",(adressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) )
                        con.commit()
                        msg = "usersWVoucher successfully added"
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
                    print("msg db addVoucher "+str(msg))
                    return jsonify("ok"), 200
            if(vc["credentialSubject"]["type"]=="TezVoucher_1"):
                print("TezVoucher_1")
                adressUser=vc["credentialSubject"]["associatedAddress"]["blockchainTezos"]
                expiration=vc["expirationDate"]
                try:
                    discount=vc["credentialSubject"]["offers"][0]["benefit"]["discount"]
                except:
                    discount=vc["credentialSubject"]["offers"]["benefit"]["discount"]
                benefitAffiliate=vc["credentialSubject"]["affiliate"]["benefit"]["incentiveCompensation"]
                benefitAffiliateType=vc["credentialSubject"]["affiliate"]["benefit"]["category"]
                affiliate=vc["credentialSubject"]["affiliate"]["paymentAccepted"]["blockchainAccount"]
                print(str(adressUser)," ",str(expiration)," ",str(discount), " ",str(benefitAffiliate)," ",str(benefitAffiliateType)," ",str(affiliate))
                try:
                    with sql.connect(DBPATH) as con:
                        cur = con.cursor()
                        print("INSERT INTO usersWVouchers (addressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) VALUES (?,?,?,?,?,?)",(adressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate))
                        cur.execute("INSERT INTO usersWVouchers (addressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) VALUES (?,?,?,?,?,?)",(adressUser,expiration,discount,benefitAffiliate,benefitAffiliateType,affiliate) )
                        con.commit()
                        msg = "usersWVoucher successfully added"
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
                    print("msg db addVoucher "+str(msg))
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
