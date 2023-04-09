import sqlite3
import time

from Classes.FileMetadata import FileMetadata

def create_table():
    try: 
        conn = sqlite3.connect('metabase.db')
        c = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS metadata
            ([name] TEXT PRIMARY KEY, [file_type] TEXT, [size] INTEGER, [fingerprint] TEXT, [modified] TEXT, [updated] TEXT);"""
        c.execute(query)
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def bulk_insert(metabase):
    try:
        conn = sqlite3.connect('metabase.db')
        c = conn.cursor()
        data = []
        for key, meta in metabase.metadata_by_name_and_type.items():
            data.append((meta.name, meta.file_type, meta.size, meta.fingerprint, str(meta.modified), str(meta.updated)))
        query = """INSERT INTO metadata (name, file_type, size, fingerprint, modified, updated) VALUES (?,?,?,?,?,?);"""
        c.executemany(query, data)
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def bulk_read(metabase):
    try:
        conn = sqlite3.connect('metabase.db')
        c = conn.cursor()
        query = """SELECT * FROM metadata;"""
        c.execute(query)
        records = c.fetchall()
        for row in records:
            key = (row[0], row[1])
            metadata = FileMetadata(row[1], row[0], row[2], row[3], row[4], row[5])
            metabase.metadata_in_db[key] = metadata
            if metadata.file_type not in metabase.metadata_by_type:
                metabase.metadata_by_type[metadata.file_type] = []
            metabase.metadata_by_type[metadata.file_type].append(metadata)
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()


def update_one(metadata):
    try:
        conn = sqlite3.connect('metabase.db')
        c = conn.cursor()
        query = """UPDATE metadata SET
            fingerprint = '""" + metadata.fingerprint + """', size = '""" + metadata.size + """' WHERE name = '""" + metadata.name + """';"""
        c.execute(query)
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def delete_one(metadata):
    try:
        conn = sqlite3.connect('metabase.db')
        c = conn.cursor()
        query = """DELETE from metadata WHERE name = '""" + metadata.name + """';"""
        c.execute(query)
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()