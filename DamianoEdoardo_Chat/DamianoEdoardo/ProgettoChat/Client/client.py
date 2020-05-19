

import requests
import threading
import os.path
import sqlite3
from os import path
import time

from config import host, myID, dbName, schema  
import base64

class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        db = sqlite3.connect(dbName)
        cur = database.cursor()
        while True:
            time.sleep(1)  
            res = requests.get(f"{host}/api/v1/receive?id={myID}").json()
            for r in res:
                ris = cur.execute(f"SELECT * FROM Contatti WHERE id = {r[0]} AND bloccato = 'False'").fetchone()
                if ris is not None:
                    cur.execute(f"INSERT INTO messaggi_ricevuti (id_mitt, text) VALUES ({r[0]}, '{r[1]}')")
                    database.commit()

def send(dest, text):
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    ris = cur.execute(f"SELECT * FROM Contatti WHERE id = {dest} AND bloccato = 'False'").fetchone()
    if ris is not None:
        res = requests.get(f"{host}/api/v1/send?ID_DEST={dest}&ID_MITT={myID}&TEXT={text}")
        if res: 
            cur.execute(f"INSERT INTO messaggi_inviati (dest, text) VALUES ({dest}, '{text}')")
            db.commit()
            print("Messaggio inviato")
        else:
            print("Errore! Impossibile inviare il messaggio")
    else:
        print("Contatto bloccato")

def receive():
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    res = cur.execute("SELECT * FROM messaggi_ricevuti").fetchall()
    db.commit()
    if len(res) != 0:
        for r in res:
            mitt = cur.execute(f"SELECT * FROM Contatti WHERE id = {r[1]}").fetchone()
            db.commit()
            print("Messaggio: ", r[2], "Mittente: ", mitt[1], mitt[2])
    else:
        print("No messaggi")

def createDatabase():
    f= open(dbName,"w+")
    f.close()
    fd = open(schema, 'r')
    sql = fd.read()
    fd.close()
    db = sqlite3.connect(dbName)
    cur = database.cursor()
    Comandi = sql.split(';')    
    for com in Comandi:    
        try:
            if com.strip() != '':
                cur.execute(com)
        except IOError:
            print ("Errore")
    db.commit()      

def menu():
    print("\n\n1. Contatti")
    print("2. Aggiorna Contatti")
    print("3. Blocca")
    print("4. Sblocca")
    print("5. Invia")
    print("6. Messaggi ricevuti")
    print("7. Invia un'immagine")
    print("0. Esci\n")

def getContatti(id):
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    contatti = cur.execute("SELECT * FROM Contatti").fetchall()
    for k in contatti:
        print(k[0],k[1],k[2], "Bloccato?: ",k[3])

def update():
    URL = f"{host}/api/v1/users"     
    contacts = requests.get(URL).json()
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    c  = 0
    for k in contacts:
        res = cur.execute(f"SELECT * FROM Contatti WHERE id ='{k[0]}'").fetchall()
        if len(result) == 0:
            c += 1   
            cur.execute(f"INSERT INTO Contatti (id, Nome, Cognome, Bloccato) VALUES ({k[0]}, '{k[1]}', '{k[2]}', 'False')")
            database.commit()

def blocca(id):
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    cur.execute(f"UPDATE Contatti SET Bloccato = 'True' WHERE id = {id}")
    db.commit()

def sblocca(id):
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    cur.execute(f"UPDATE Contatti SET Bloccato = 'False' WHERE id = {id}")
    db.commit()

def main(thread):
    update()
    while True:
        menu()
        while True:
            try:
                option = int(input("Scegli un opzione >>> "))
                break
            except:
                print("Inserisci un opzione valida (1-6)")
            if option == 1:
                getContatti(id)
            elif option == 2:
                update()
            elif option == 3:
                lock = input("Inserisci l'id dell'utente che vuoi bloccare: ")
                blocca(lock)
            elif option == 4:
                unlock = input("Inserisci l'id dell'utente che vuoi sbloccare: ")
                sblocca(unlock)
            elif option == 5:
                dest = input("Inserisci l'Id del destinatario: ")
                text = input("Inserisci il testo : ")
                send(dest, text)
            elif option == 6:
                receive()
            elif option == 7:
            elif option == 0:
                break
    thread.join()

if __name__ == "__main__":
    if not path.exists(dbName):
        createDatabase()

    newthread = ClientThread()
    newthread.start()
    main(newthread)

    