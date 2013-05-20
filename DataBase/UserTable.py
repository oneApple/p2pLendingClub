import sqlite3

from GlobalData import MagicNum
from DataBase import DbInterface

class UserTable(DbInterface.DbInterface,object):
    def __init__(self):
        super(UserTable,self).__init__()
    
    def CreateTable(self):
        self.ExcuteCmd("CREATE TABLE UserDB (name TEXT PRIMARY KEY,password TEXT,position TEXT,permission INT)")
        self.AddNewUser(['root','root','root'])
        self.AlterUser("permission",MagicNum.UserDB.PERMISSION_ROOT , 'root')
    
    def AddNewUser(self,value):
        value.append(MagicNum.UserDB.PERMISSION_NOTHING)
        try:
            self.InsertValue("UserDB", value)
        except sqlite3.IntegrityError,e:
            return False
        return True
    
    def AlterUser(self,attri,value,name):
        _sql = "UPDATE UserDB SET " + attri + "=? where name=?"
        self.ExcuteCmd(_sql,[value,name])
    
    def SearchUser(self,name):
        _sql = "SELECT * FROM UserDB where name=?"
        return self.Search(_sql, [name])
    
    def DeleteUser(self,name):
        _sql = "DELETE FROM UserDB WHERE name=?"
        self.ExcuteCmd(_sql, [name,])    
    
    def DeleteTable(self):
        self.ExcuteCmd("DROP TABLE UserDB")   
        
if __name__=='__main__': 
    a = UserTable()
    a.Connect()
    a.CreateTable()
    #a.DeleteUser("any")
    print a.Search("select * from UserDB")
    a.CloseCon()
        