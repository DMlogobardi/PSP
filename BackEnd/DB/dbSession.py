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
    

    
    #idPeople only get
    def getIdPeople(self):
        return self.idPeople

    #name get and set
    def setName(self, name):
        if name.strip().lower() != "" or name.strip().lower() != None:
            self.name = name.strip().lower()

    def getName(self):
        return self.name

    #surname det and set
    def setSurname(self, surname):
        if surname.strip().lower() != "" or surname.strip().lower() != None:
            self.surname = surname.strip().lower()

    def getSurname(self):
        return self.surname

    #classm get and set
    def setClassm(self, classm):
        if len(classm.strip().lower()) <= 3 and len(classm.strip().lower()) > 0:
            self.classm = classm.strip().lower()

    def getClassm(self):
        return self.classm

    #cf get and set
    def setCf(self, cf):
        if cf.strip().upper() != "" or cf.strip().upper() != None and len(cf.strip().upper()) == 16:
            self.cf = cf.strip().upper()

    def getCf(self):
        return self.cf

    #gender get and set
    def setGender(self, gender):
        if gender.strip().lower() != "" or gender.strip().lower() != None and gender.strip().lower() == 'm' or gender.strip().lower() == 'f':
            self.gender = gender.strip().lower()  

    def getGender(self):
        return self.gender

    #email get and set
    def setEmail(self, email):
        if email.strip().lower() != "" or email.strip().lower() != None:
            self.email = email.strip().lower()

    def getEmail(self):
        return self.email

    #birthday get and set
    def setBirthday(self, birthday):
        if birthday != None and int(date.year(birthday)) - int(date.year(date.today())) > 13 and int(date.year(birthday)) - int(date.year(date.today())) < 90:
            self.birthday = birthday

    def getBirthday(self):
        return self.birthday

    #sub get and set
    def setSub(self, sub):
        self.sub = sub.strip().lower()

    def getSub(self):
        return self.sub

class Classm(SQLModel, table = True):
    IdClass : Optional[int] = Field(default=None, primary_key = True)
    Carrel : str
    Year : int
    Articulation : str
    Active : str

    people: List["People"] = Relationship(back_populates = "classm")

class Phones (SQLModel, table = True):
    IdPhones : Optional[int] = Field(default=None, primary_key = True)
    number : str
    prefix : str
    IdPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
    people : Optional[People] = Relationship(back_populates="phones")


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

class Vehicles(SQLModel, table = True):
    IdV : Optional[int] = Field(default=None, primary_key = True)
    Type : str
    Plate : str
    Owner : str
    IdPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
    
    people : Optional[People] = Relationship(back_populates="vehicles")
    
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
        return hashlib.sha256(self.Pass.encode()).hexdigest()

    #GK only get 
    def getGK(self):
        return hashlib.sha256(self.GK.encode()).hexdigest()
    
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

class Entries(SQLModel, table = True):
    IdIng : Optional[int] = Field(default=None, primary_key = True)
    DataIn : datetime
    DataOut :  Optional[datetime]
    IdAccount : int = Field(default=None, foreign_key="account.IdAccount")

    account: Optional[Account] = Relationship(back_populates="entriess")

    #IdIng only get
    def getIdIng(self):
        return self.IdIng
    
    #DataIn get and set
    def getDataIn(self):
        return self.DataIn
    
    def setDataIn(self, DataIn):
        if DataIn != None and DataIn >= datetime.now():
            self.DataIn = DataIn 

    #DataOut get and set
    def getDataOut(self):
        return self.DataOut
    
    def setDataOut(self, DataOut):
        if DataOut != None and DataOut >= datetime.now():
            self.DataOut = DataOut

    #IdAccount only get
    def getIdAccount(self):
        return self.IdAccount

#creazione ed invio sessione

def session():
    try:
        engine = create_engine("mysql://root:@localhost/psp")
        SQLModel.metadata.create_all(engine)
        session = Session(engine)
        return session
    except Exception as e:
       return e
    