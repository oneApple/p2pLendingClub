import sqlite3

from GlobalData import MagicNum
from DataBase import DbInterface

class QuotaTable(DbInterface.DbInterface,object):
    def __init__(self):
        super(QuotaTable,self).__init__()
    
    def CreateTable(self):
        self.ExcuteCmd("CREATE TABLE QuotaTable (name TEXT PRIMARY KEY,highertype INT,relation INT,description TEXT,formula TEXT)")
    
    def AddNewQuota(self,value):
        try:
            self.InsertValue("QuotaTable", value)
        except sqlite3.IntegrityError,e:
            return False
        return True
    
    def AlterQuota(self,attri,value,name):
        _sql = "UPDATE QuotaTable SET " + attri + "=? where name=?"
        self.ExcuteCmd(_sql,[value,name])
    
    def SearchAllQuota(self):
        return self.Search("select * from QuotaTable")
    
    def SearchQuota(self,name):
        _sql = "SELECT * FROM QuotaTable where name=?"
        return self.Search(_sql, [name])
    
    def DeleteQuota(self,name):
        _sql = "DELETE FROM QuotaTable WHERE name=?"
        self.ExcuteCmd(_sql, [name,]) 
    
    def DeleteTable(self):
        self.ExcuteCmd("DROP TABLE QuotaTable")   
        
if __name__=='__main__': 
    a = QuotaTable()
    a.Connect()
    #a.DeleteTable()
    a.CreateTable()
    #print a.AddNewQuota(["t1",MagicNum.QuotaTable.CURRENT_VALUE,"des","formula"])
#    a.DeleteQuota("t1")
    #print a.SearchQuota("t1")
    #print a.SearchAllQuota()
    a.CloseCon()
        