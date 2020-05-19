from flask import Flask, request, jsonify
import datetime
import sqlite3
import base64

dbPath = "data/db.db"   

app = Flask(__name__)

@app.route('/api/v1/send', methods=['GET', 'POST'])
def send():
        if "ID_DEST" and "ID_MITT" and "TEXT" in request.args:
            ID_DEST = request.args['ID_DEST']
            ID_MITT = request.args['ID_MITT']
            TEXT = request.args['TEXT']
            if ID_DEST and ID_MITT and TEXT != "":
                db = sqlite3.connect(dbPath)
                c = db.cursor()
                c.execute(f"INSERT INTO MESSAGGI (dest, mitt, text, inviato) VALUES ({ID_DEST}, {ID_MITT}, '{TEXT}', 'False'")
                db.commit()
                db.close()
                return 'True'
            else:
                return 'False'
        return 'False'

@app.route('/api/v1/receive', methods=['GET'])
def receive():
    messaggi = {}
    if "id" in request.args:
        if len(request.args['id']) != 0:
            id = request.args['id']
            db = sqlite3.connect(dbPath)
            c = db.cursor()
            c.execute(
                f"SELECT mitt, text FROM MESSAGGI WHERE dest = {id} AND inviato = 'False'")
            messeggi = c.fetchall()
            c.execute(f"UPDATE MESSAGGI SET inviato = 'True' WHERE dest={id} AND inviato = 'False'")
            db.commit()
            print(messaggi)
            db.close()
    return jsonify(messages)

@app.route('/api/v1/users', methods=['GET'])
def users():
    database = sqlite3.connect(dbPath)
    c = database.cursor()
    c.execute(
        f"SELECT * FROM UTENTI ORDER BY id_utente")
    utenti = c.fetchall()
    database.close()
    return jsonify(utenti)

if __name__ == '__main__':
    app.run()
