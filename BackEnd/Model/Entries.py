from pydantic import BaseModel
from datetime import datetime

class Entries(BaseModel):
    IdIng : int
    DataIn : datetime
    DataOut : datetime
    IdAccount : int

    def __init__(self, IdIng, DataIn, DataOut, IdAccount):
        self.IdIng = IdIng
        self.DataIn = DataIn
        self.DataOut = DataOut
        self.IdAccount = IdAccount

    #IdIng only get
    def getIdIng(self):
        return self.IdIng
    
    #DataIn get and set
    def getDataIn(self):
        return self.DataIn
    
    def setDataIn(self, DataIn):
        if DataIn != None and DataIn < datetime.now():
            self.DataIn = DataIn 

    #DataOut get and set
    def getDataOut(self):
        return self.DataOut
    
    def setDataOut(self, DataOut):
        if DataOut != None and DataOut < datetime.now():
            self.DataOut = DataOut

    #IdAccount only get
    def getIdAccount(self):
        return self.IdAccount
    
    #tostring
    def tostring(self):
        return f"""id:{self.IdIng }, DataIn{self.DataIn}, DataOut{self.DataOut}, IdAccount{self.IdAccount}"""       