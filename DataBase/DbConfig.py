from ConfigParser import ConfigParser
_metaclass_ = type
class DbConfig:
    databasepath = ""
    def __init__(self):
        CONFIGFILE = "./config.dat"
        config = ConfigParser()
        config.read(CONFIGFILE)
        DbConfig.databasepath = config.get('database', 'path')
    def GetConfigMessage(self):
        return DbConfig.databasepath
    
if __name__=='__main__':
    c = DbConfig()
    print c.GetConfigMessage()