from pydantic import BaseModel

class Phones(BaseModel):
    IdPhones : int
    number : str
    prefix : str
    IdPeople : int

    def __init__(self, IdPhones, number, prefix, IdPeople):
        self.IdPhones = IdPhones
        self.number = number
        self.prefix = prefix
        self.IdPeople = IdPeople

    #IdPhones only get
    def getIdPhones(self):
        return self.IdPhones
    
    #number get and set
    def getNumber(self):
        return self.number
    
    def setNumber(self, number):
        if number.strip().lower() != "" or number.strip().lower() != None and len(number.strip()) <= 15 and len(number.strip()) > 5:
            self.number = number

    #prefix get and set
    def getPrefix(self):
        return self.prefix
    
    def setPrefix(self, prefix):
        if prefix.strip().lower() != "" or prefix.strip().lower() != None and len(prefix.strip()) >= 2:
            self.prefix = prefix

    #IdPeople only get
    def getIdPeople(self):
        return self.IdPeople
    
    #tostring
    def tostring(self):
        return f"""id:{self.IdPhones}, number:{self.number}, prefix:{self.prefix}, IdPeople:{self.IdPeople}"""