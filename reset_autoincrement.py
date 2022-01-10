#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

database = sys.argv[1].lower()
table = sys.argv[2].lower()


# Leer campos y datos

with sqlite3.connect(database) as conn:
    conn.row_factory = sqlite3.Row
    
    cursor = conn.execute(
        f"""SELECT * FROM {table};"""
    )
    row = cursor.fetchone()
    names = row.keys()
    
with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT * FROM {table};"""
    )
    table_copy = cursor.fetchall()



if table_copy:
    # Borrar viejos datos
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""DELETE FROM {table};"""
        )
        
    # Resetear AUTOINCREMENT
       
        cursor.execute(
            f"""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table}';"""
        )
                
    # Insertar nuevos datos

        for i, x in enumerate(table_copy, 1):
            for a in x:
                values = [str(y) if not isinstance(y, str) else f'"{y}"' for y in x[1:]]
                s = f'INSERT INTO {table} VALUES ({i}, ' + ', '.join(values) + ')'
            print(s)
            cursor.execute(s)
            
        conn.commit()