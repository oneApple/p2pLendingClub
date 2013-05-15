import sqlite3

from GlobalData import MagicNum
from DataBase import DbInterface

class CommentTable(DbInterface.DbInterface,object):
    def __init__(self):
        super(CommentTable,self).__init__()
    
    def CreateTable(self):
        self.ExcuteCmd("CREATE TABLE CommentTable(quotaname TEXT,username INT,comment TEXT,score INT)")
    
    def AddNewComment(self,value):
        try:
            self.InsertValue("CommentTable", value)
        except sqlite3.IntegrityError,e:
            return False
        return True
    
    def SearchAllComment(self):
        return self.Search("select * from CommentTable")
    
    def SearchComment(self,name):
        _sql = "SELECT * FROM CommentTable where username=?"
        return self.Search(_sql, [name])
    
    def DeleteComment(self,name):
        _sql = "DELETE FROM CommentTable WHERE username=?"
        self.ExcuteCmd(_sql, [name,]) 
    
    def DeleteTable(self):
        self.ExcuteCmd("DROP TABLE CommentTable")   
        
if __name__=='__main__': 
    a = CommentTable()
    a.Connect()
    #a.DeleteTable()
    a.CreateTable()
#    print a.AddNewComment(["t1","keyaming","sb",1])
##   a.DeleteQuota("t1")
#    print a.SearchComment("keyaming")
    print a.SearchAllComment()
    a.CloseCon()
        