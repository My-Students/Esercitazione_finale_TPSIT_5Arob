"""
Uso questo file per aprire e chiudere il database
"""
import sqlite3

def open_db():
    conn = sqlite3.connect('database.db')   # creo l'oggetto conn
    return conn     # ritorno la conn

def close_db(conn):    # passo l'oggetto conn da chiudere
    conn.close()