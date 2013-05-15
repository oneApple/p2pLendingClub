# -*- coding: UTF-8 -*-

import sqlite3
import DbConfig

class DbInterface:
    configPath = DbConfig.DbConfig()
    def __init__(self):
        self.dbPath = DbInterface.configPath.GetConfigMessage()
    
    def Connect(self):
        self.__con = sqlite3.connect(self.dbPath)
         
    def ExcuteCmd(self,sql,value = []):
        cur = self.__con.cursor()
        cur.execute(sql,value)
        self.__con.commit()
        
    def InsertValue(self,dbname,value = []):
        valueNum = len(value)
        cur = self.__con.cursor()
        query = 'INSERT INTO ' + dbname + ' VALUES(' + '?,' * (valueNum - 1) + '?)'
        cur.execute(query,value)
        self.__con.commit()
    
    def Search(self,sql,value = []):
        cur = self.__con.cursor()
        cur.execute(sql,value)
        self.__con.commit()
        return cur.fetchall()
     
    def CloseCon(self):
        self.__con.close()

if __name__=='__main__': 
    a = DbInterface()
    a.Connect()
    #a.ExcuteCmd("CREATE TABLE UserDB (name TEXT PRIMARY KEY,password TEXT,position TEXT,permission INT)" )
    #sql = "UPDATE UserDB SET password=?,permission=? where name=?"
    #a.ExcuteCmd(sql, ["new",2,"ke"])
    #a.InsertValue("UserDB",['ke',"d","POS",1])
    print a.Search("SELECT * FROM UserDB")
    a.CloseCon()

