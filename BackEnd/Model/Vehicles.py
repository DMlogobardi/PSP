from pydantic import BaseModel

class Vehicles(BaseModel):
    IdV : int
    Type : str
    Plate : str
    Owner : str
    IdPeople : int

    def __init__(self, IdV, Type, Plate, Owner, IdPeople):
        self.IdV = IdV
        self.Type = Type
        self.Plate= Plate
        self.Owner = Owner
        self.IdPeople = IdPeople

    #IdV only get
    def getIdV(self):
        return self.IdV
    
    #Type get and set
    def getType(self):
        return self.Type
    
    def setType(self, Type):
        if Type.strip().lower() != "" or Type.strip().lower() != None and len(Type.strip()) >= 5:
            self.Type = Type

    #Plate get and set
    def getPlate(self):
        return self.Plate 
    
    def setPlate(self, Plate ):
        if Plate.strip().lower() != "" or Plate.strip().lower() != None and len(Plate.strip()) <= 8:
            self.Plate = Plate
    
    #Owner get and set
    def getOwner(self):
        return self.Owner
    
    def setOwner(self, Owner):
        if Owner.strip().lower() != "" or Owner.strip().lower() != None:
            self.Owner = Owner

    #IdPeople only get
    def getIdPeople(self):
        return self.IdPeople
    
    #tostring
    def tostring(self):
        return f"""id:{self.IdV}, Type:{self.Type}, Plate:{self.Plate}, Owner:{self.Owner}, IdPeople:{self.IdPeople}"""