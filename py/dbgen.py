#!/usr/bin/env python3

import sqlite3
import os


def create_db(caches, file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    db = sqlite3.connect(file_name)

    cur = db.cursor()
    cur.execute("CREATE TABLE caches (code TEXT PRIMARY KEY, name TEXT, coords TEXT, url TEXT, timestamp TIMESTAMP, owner TEXT, finds INTEGER, short_desc TEXT);")
    cur.execute("CREATE TABLE logs (uuid TEXT PRIMARY KEY, cache_code TEXT, user TEXT, type TEXT, comment TEXT, coords TEXT, timestamp TIMESTAMP, FOREIGN KEY(cache_code) REFERENCES caches(code));")
    cur.execute("CREATE TABLE logimages (log_uuid TEXT, url TEXT, thumb_url TEXT, caption TEXT, FOREIGN KEY(log_uuid) REFERENCES logs(uuid));")
    db.commit()

    cur = db.cursor()
    for cache in caches:
        cur.execute(
            "INSERT INTO caches (code, name, coords, url, timestamp, owner, finds, short_desc) VALUES (?,?,?,?,?,?,?,?);",
            (cache._code, cache._name, cache._coordinates, cache._url, cache._date, cache._owner, cache._founds, cache._short_description))
        for log in cache._logs:
            cur.execute(
                "INSERT INTO logs (uuid, cache_code, user, type, comment, coords, timestamp) VALUES (?,?,?,?,?,?,?);",
                (log._uuid, cache._code, log._user, log._type, log._comment, log._coordinates, log._date))
            for image in log._images:
                cur.execute(
                    "INSERT INTO logimages (log_uuid, url, thumb_url, caption) VALUES (?,?,?,?);",
                    (log._uuid, image["url"], image["thumb_url"], image["caption"]))
                
    db.commit()
