#!/usr/bin/env python
# Copyright (C) Serg, creator of https://rnma.xyz/boinc
import mysql.connector
from lxml import etree
import os

def jobs_avail():
 db_host, db_name, db_user, db_passwd=db_creds()
 connection = mysql.connector.connect(host=db_host,
  database=db_name,
  user=db_user,
  password=db_passwd)
 sql_select_Query = "select count(*) from boinc.result where server_state=2"
 cursor = connection.cursor()
 cursor.execute(sql_select_Query)
 record = cursor.fetchone()[0] >> 1
 return(record)

def read_file(name):
 f=open(name,mode='r') 
 s=f.read()
 f.close()
 return s

def write_file(name, content):
 with open(name, 'w') as f:
  f.write(str(content))

def db_creds():
 root = etree.fromstring(read_file('config.xml'))
 conftag=root.find('config')
 return conftag.find('db_host').text.strip(), conftag.find('db_name').text, conftag.find('db_user').text, conftag.find('db_passwd').text
def dirmap():
 return(map(lambda f: f, os.scandir()))

def filteredmap(dm):
 return(filter(lambda f: f is not None and not f.is_dir() and f.is_file, dm))

def fmap():
 return(filteredmap(dirmap()))


if __name__ == "__main__":
 print(jobs_avail())