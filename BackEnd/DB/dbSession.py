from sqlmodel import Field, SQLModel, Session, create_engine, Relationship
from typing import Optional, List
from datetime import date, datetime
import hashlib
import pymysql
pymysql.install_as_MySQLdb()

#DB mapping

class People(SQLModel, table = True):
    idPeople : Optional[int] = Field(default=None, primary_key = True)
    name : str
    surname : str
    cf : str
    gender : Optional[str]
    email : str 
    birthday : date
    sub : Optional[str]
    IdClass : Optional[int] = Field(default=None, foreign_key="classm.IdClass")
    
    classm : Optional["Classm"] = Relationship(back_populates="people")
    account : Optional["Account"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates = "people")
    vehicles: List["Vehicles"] = Relationship(back_populates="people")
    phones: List["Phones"] = Relationship(back_populates="people")

    #name set
    def setName(self, name):
        if name.strip().lower() != "" or name.strip().lower() != None:
            self.name = name.strip().lower()

    #surname set
    def setSurname(self, surname):
        if surname.strip().lower() != "" or surname.strip().lower() != None:
            self.surname = surname.strip().lower()

    #cf set
    def setCf(self, cf):
        if cf.strip().upper() != "" or cf.strip().upper() != None and len(cf.strip().upper()) == 16:
            self.cf = cf.strip().upper()

    #gender set
    def setGender(self, gender):
        if gender.strip().lower() != "" or gender.strip().lower() != None and gender.strip().lower() == 'm' or gender.strip().lower() == 'f':
            self.gender = gender.strip().lower()  

    #email set
    def setEmail(self, email):
        if email.strip().lower() != "" or email.strip().lower() != None:
            self.email = email.strip().lower()

    #birthday set
    def setBirthday(self, birthday):
        if birthday != None and int(date.year(birthday)) - int(date.year(date.today())) > 13 and int(date.year(birthday)) - int(date.year(date.today())) < 90:
            self.birthday = birthday

    #sub set
    def setSub(self, sub):
        self.sub = sub.strip().lower()

    #IdClass set
    def setIdClass(self, idClass):
        if idClass > 0:
            self.IdClass = idClass

class Classm(SQLModel, table = True):
    IdClass : Optional[int] = Field(default=None, primary_key = True)
    Carrel : str
    Year : int
    Articulation : str
    Active : str

    people: List["People"] = Relationship(back_populates = "classm")

    #Carrel set
    def setCarrel(self, carrel):
        if carrel.strip().lower() != "" or carrel.strip().lower() != None and len(carrel.strip().lower())<=2:
            self.Carrel = carrel.strip().lower()

    #Year set
    def setYear(self, year):
        if year > 0 and year <=5:
            self.Year = year

    #Articulation set
    def setArticulation(self, articulation):
        if articulation.strip().lower() != "" or articulation.strip().lower() != None:
            self.Articulation = articulation

    #Active set
    def setActive(self, active):
        if active.strip().lower() != "" or active.strip().lower() != None:
            self.Active = active

class Phones (SQLModel, table = True):
    IdPhones : Optional[int] = Field(default=None, primary_key = True)
    number : str
    prefix : str
    IdPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
    people : Optional[People] = Relationship(back_populates="phones")
    
    #number set
    def setNumber(self, number):
        if number.strip().lower() != "" or number.strip().lower() != None and len(number.strip()) <= 15 and len(number.strip()) > 5:
            self.number = number

    #prefix set   
    def setPrefix(self, prefix):
        if prefix.strip().lower() != "" or prefix.strip().lower() != None and len(prefix.strip()) >= 2:
            self.prefix = prefix

    #IdPeople set
    def setIdPeople(self, idPeople):
        if idPeople > 0:
            self.IdPeople = idPeople

class Vehicles(SQLModel, table = True):
    IdV : Optional[int] = Field(default=None, primary_key = True)
    Type : str
    Plate : str
    Owner : str
    IdPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
    
    people : Optional[People] = Relationship(back_populates="vehicles")
    
    #Type set
    def setType(self, Type):
        if Type.strip().lower() != "" or Type.strip().lower() != None and len(Type.strip()) >= 5:
            self.Type = Type

    #Plate set
    def setPlate(self, Plate ):
        if Plate.strip().lower() != "" or Plate.strip().lower() != None and len(Plate.strip()) <= 8:
            self.Plate = Plate
    
    #Owner set
    def setOwner(self, Owner):
        if Owner.strip().lower() != "" or Owner.strip().lower() != None:
            self.Owner = Owner

    #IdPeople set
    def setIdPeople(self, idPeople):
        if idPeople > 0:
            self.IdPeople = idPeople

class Account(SQLModel, table = True):
    IdAccount : Optional[int] = Field(default=None, primary_key = True)
    Nick : str
    Pass : str
    GK : Optional[str]
    Ruolo : Optional[str]
    DataReg : Optional[date]
    DataExp : Optional[date] 
    idPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")

    people : Optional[People] = Relationship(back_populates="account")
    entriess : List["Entries"] = Relationship(back_populates="account")

    #Nick set
    def setNick(self, Nick):
        if Nick.strip().lower() != "" or Nick.strip().lower() != None:
            self.Nick = Nick

    #Pass only get
    def getPass(self):
        return hashlib.sha256(self.Pass.encode()).hexdigest()

    #GK get and set 
    def getGK(self):
        return hashlib.sha256(self.GK.encode()).hexdigest()
    
    def setGK(self, Gk):
        if Gk.strip().lower() != "" or Gk.strip().lower() != None and len(Gk.strip().lower()) > 0 and len(Gk.strip().lower()) <= 4:
            self.GK = Gk
    
    #Ruolo set
    def setRuolo(self, Ruolo):
        if Ruolo.strip().lower() != "" or Ruolo.strip().lower() != None:
            self.Ruolo = Ruolo

    #DataReg set
    def setDataReg(self, DataReg):
        if DataReg != None and DataReg >= date.today():
            self.DataReg = DataReg

    #DataExp set
    def setDataExp(self, DataExp):
        if DataExp != None and DataExp >= date.today():
            self.DataExp = DataExp

    #IdPeople set
    def setIdPeople(self, idPeople):
        if idPeople > 0:
            self.IdPeople = idPeople

class Entries(SQLModel, table = True):
    IdIng : Optional[int] = Field(default=None, primary_key = True)
    DataIn : datetime
    DataOut :  Optional[datetime]
    IdAccount : int = Field(default=None, foreign_key="account.IdAccount")

    account: Optional[Account] = Relationship(back_populates="entriess")

    #DataIn set
    def setDataIn(self, DataIn):
        if DataIn != None and DataIn >= datetime.now():
            self.DataIn = DataIn 

    #DataOut set
    def setDataOut(self, DataOut):
        if DataOut != None and DataOut >= datetime.now():
            self.DataOut = DataOut

    #IdAccount set
    def setIdAccount(self, idAccount):
        if idAccount > 0:
            self.IdPeople = idAccount

#creazione ed invio sessione

def session():
    try:
        engine = create_engine("mysql://root:@localhost/psp")
        SQLModel.metadata.create_all(engine)
        session = Session(engine)
        return session
    except Exception as e:
       return e
    