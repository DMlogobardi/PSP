import json
import select
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship
from typing import Any, Dict, Optional, List
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
    idClass : Optional[int] = Field(default=None, foreign_key="classm.idClass")
    
    classm : Optional["Classm"] = Relationship(back_populates="people")
    account : Optional["Account"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates = "people")
    vehicles: List["Vehicles"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="people")
    phones: List["Phones"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="people")

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
            self.idClass = idClass

def createPeople(people_payload: Any) -> People:
    people_json = json.dumps(people_payload)
    people_data = json.loads( people_json)
    people = People(
        name=people_data.get("name"),
        surname=people_data.get("surname"),
        cf=people_data.get("cf"),
        gender=people_data.get("gender"),
        email=people_data.get("email"),
        birthday=people_data.get("birthday"),
        sub=people_data.get("sub"),
        idClass=people_data.get("idClass")
    )
    return people


class Classm(SQLModel, table = True):
    idClass : Optional[int] = Field(default=None, primary_key = True)
    carrel : str
    year : int
    articulation : Optional[str]
    active : Optional[str]

    people: List["People"] = Relationship(back_populates = "classm")

    #Carrel set
    def setCarrel(self, carrel):
        if carrel.strip().lower() != "" or carrel.strip().lower() != None and len(carrel.strip().lower())<=2:
            self.carrel = carrel.strip().lower()

    #Year set
    def setYear(self, year):
        if year > 0 and year <=5:
            self.year = year

    #Articulation set
    def setArticulation(self, articulation):
        if articulation.strip().lower() != "" or articulation.strip().lower() != None:
            self.articulation = articulation

    #Active set
    def setActive(self, active):
        if active.strip().lower() != "" or active.strip().lower() != None:
            self.active = active

def createClassm(classm_payload: Any) -> Classm:
    classm_json = json.dumps(classm_payload)
    classm_data = json.loads(classm_json)
    classm = Classm(
        year= classm_data.get("year"),
        carrel= classm_data.get("carrel"),
        articulation= classm_data.get("articulation") if "articulation" in classm_data else None,
        active= classm_data.get("active") if "active" in classm_data else None
    )
    return classm

class Phones (SQLModel, table = True):
    idPhones : Optional[int] = Field(default=None, primary_key = True)
    number : str
    prefix : str
    idPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
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
            self.idPeople = idPeople

def createPhones(phones_payload: Any) -> Phones:
    phones_json = json.dumps(phones_payload)
    phones_data = json.loads(phones_json)
    phone = Phones(
        number= phones_data.get("number"),
        prefix= phones_data.get("prefix"),
        idPeople= phones_data.get("idPeople") if "idPeople" in phones_data else None
    )
    return phone

class Vehicles(SQLModel, table = True):
    idV : Optional[int] = Field(default=None, primary_key = True)
    type : str
    plate : str
    owner : str
    idPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")
    
    people : Optional[People] = Relationship(back_populates="vehicles")
    
    #Type set
    def setType(self, type):
        if type.strip().lower() != "" or type.strip().lower() != None and len(type.strip()) >= 5:
            self.type = type

    #Plate set
    def setPlate(self, plate ):
        if plate.strip().lower() != "" or plate.strip().lower() != None and len(plate.strip()) <= 8:
            self.plate = plate
    
    #Owner set
    def setOwner(self, owner):
        if owner.strip().lower() != "" or owner.strip().lower() != None:
            self.owner = owner

    #IdPeople set
    def setIdPeople(self, idPeople):
        if idPeople > 0:
            self.idPeople = idPeople

def createVehicles(vehicles_payload: Any) -> Vehicles:
    vehicles_json = json.dumps(vehicles_payload)
    vehicles_data = json.loads(vehicles_json)
    vehicle = Vehicles(
        type= vehicles_data.get("type"),
        plate= vehicles_data.get("plate"),
        owner= vehicles_data.get("owner"),
        idPeople= vehicles_data.get("idPeople") if "idPeople" in vehicles_data else None
    )
    return vehicle

class Account(SQLModel, table = True):
    idAccount : Optional[int] = Field(default=None, primary_key = True)
    nick : str
    p_ass : str
    gK : Optional[str]
    ruolo : Optional[str]
    dataReg : Optional[date]
    dataExp : Optional[date]
    valid : Optional[str]
    idPeople : Optional[int] = Field(default=None, foreign_key="people.idPeople")

    people : Optional[People] = Relationship(back_populates="account")
    entriess : List["Entries"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="account")

    #Nick set
    def setNick(self, nick):
        if nick.strip().lower() != "" or nick.strip().lower() != None:
            self.nick = nick

    #Pass only get
    def getP_ass(self):
        return hashlib.sha256(self.p_ass.encode()).hexdigest()

    #GK get and set 
    def getGK(self):
        return hashlib.sha256(self.gK.encode()).hexdigest()
    
    def setGK(self, gK):
        if gK.strip().lower() != "" or gK.strip().lower() != None and len(gK.strip().lower()) > 0 and len(gK.strip().lower()) <= 4:
            self.gK = gK
    
    #Ruolo set
    def setRuolo(self, ruolo):
        if ruolo.strip().lower() != "" or ruolo.strip().lower() != None:
            self.ruolo = ruolo

    #DataReg set
    def setDataReg(self, dataReg):
        if dataReg != None and dataReg >= date.today():
            self.dataReg = dataReg

    #DataExp set
    def setDataExp(self, dataExp):
        if dataExp != None and dataExp >= date.today():
            self.dataExp = dataExp

    #IdPeople set
    def setIdPeople(self, idPeople):
        if idPeople > 0 and idPeople != None:
            self.idPeople = idPeople

def createAccount(account_payload: Any) -> Account:
    account_json = json.dumps(account_payload)
    account_data = json.loads(account_json)
    account = Account(
        nick= account_data.get("nick"),
        p_ass= account_data.get("p_ass"),
        gK= account_data.get("gK") if "gK" in account_data else None,
        ruolo= account_data.get("ruolo") if "ruolo" in account_data else None,
        dataReg= account_data.get("dataReg") if "dataReg" in account_data else None,
        dataExp= account_data.get("dataExp") if "dataExp" in account_data else None,
        valid= account_data.get("valid") if "valid" in account_data else None,
        idPeople= account_data.get("idPeople") if "idPeople" in account_data else None
    )
    return account

class Entries(SQLModel, table = True):
    idIng : Optional[int] = Field(default=None, primary_key = True)
    dataIn : datetime
    dataOut :  Optional[datetime]
    idAccount : int = Field(default=None, foreign_key="account.idAccount")

    account: Optional[Account] = Relationship(back_populates="entriess")

    #DataIn set
    def setDataIn(self, dataIn):
        if dataIn != None and dataIn >= datetime.now():
            self.dataIn = dataIn 

    #DataOut set
    def setDataOut(self, dataOut):
        if dataOut != None and dataOut >= datetime.now():
            self.dataOut = dataOut

    #IdAccount set
    def setIdAccount(self, idAccount):
        if idAccount > 0:
            self.idAccount = idAccount

def createEntries(entries_payload: Any) -> Entries:
    entrie_json = json.dumps(entries_payload)
    entrie_data = json.loads(entrie_json)
    entrie = Entries(
        dataIn= entrie_data.get("dataIn"),
        dataOut= entrie_data.get("dataOut") if "dataOut" in entrie_data else None,
        idAccount= entrie_data.get("idAccount") if "idAccount" in entrie_data else None
    )
    return entrie

#creazione ed invio sessione

def session():
    try:
        engine = create_engine("mysql://root:@localhost/psp")
        SQLModel.metadata.create_all(engine)
        session = Session(engine)
        return session
    except Exception as e:
       return e
