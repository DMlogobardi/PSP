from pydantic import BaseModel
from datetime import date
import hashlib

class Account(BaseModel):
    IdAccount  : int
    Nick : str
    Pass : str
    GK : str
    Ruolo : str
    DataReg : date
    DataExp : date
    IdPeople : int

    def __init__(self,  IdAccount, Nick, Pass, GK, Ruolo, DataReg, DataExp, IdPeople):
        self.IdAccount = IdAccount
        self.Nick = Nick
        self.Pass = Pass
        self.GK = GK
        self.Ruolo = Ruolo
        self.DataReg = DataReg
        self.DataExp = DataExp
        self.IdPeople = IdPeople

    #IdAccount  only get
    def getIdAccount(self):
        return self.IdAccount
    
    #Nick get and set
    def getNick(self):
        return self.Nick
    
    def setNick(self, Nick):
        if Nick.strip().lower() != "" or Nick.strip().lower() != None:
            self.Nick = Nick

    #Pass only get
    def getPass(self):
        return hashlib.sha224(self.Pass.encode()).hexdigest()

    #GK only get 
    def getGK(self):
        return hashlib.sha224(self.GK.encode()).hexdigest()
    
    #Ruolo get and set
    def getRuolo(self):
        return self.Ruolo
    
    def setRuolo(self, Ruolo):
        if Ruolo.strip().lower() != "" or Ruolo.strip().lower() != None:
            self.Ruolo = Ruolo

    #DataReg get and set
    def getyDataReg(self):
        return self.DataReg
    
    def setDataReg(self, DataReg):
        if DataReg != None and DataReg >= date.today():
            self.DataReg = DataReg

    #DataExp get and set
    def getDataExp(self):
        return self.DataExp
    
    def setDataExp(self, DataExp):
        if DataExp != None and DataExp >= date.today():
            self.DataExp = DataExp

    #IdPeople only get
    def getIdPeople(self):
        return self.IdPeople
    
    #tostring
    def tostring(self):
        return f"""id:{self.IdAccount}, Nick:{self.Nick}, Ruolo:{self.Ruolo}, DataReg:{self.DataReg}, DataExp:{self.DataExp}, IdPeople:{self.IdPeople}"""