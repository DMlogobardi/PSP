from pydantic import BaseModel
from datetime import datetime

class People(BaseModel):
    idPeople : int
    name : str
    surname : str
    classm : str
    cf : str
    gender : str
    email : str 
    birthday : str
    sub : str

    def __init__(self, idPeople, name, surname, classm, cf, gender, email, birthday, sub):
        self.idPeople = idPeople
        self.name = name
        self.surname = surname
        self.classm = classm
        self.cf = cf
        self.gender = gender
        self.email = email
        self.birthday = birthday
        self.sub = sub

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
        if birthday.strip().lower() != "" or birthday.strip().lower() != None and datetime.strptime( birthday.strip().lower()):
            self.birthday =  birthday.strip().lower()

    def getBirthday(self):
        return self.birthday

    #sub get and set
    def setSub(self, sub):
        self.sub = sub.strip().lower()

    def getSub(self):
        return self.sub

    #tostring
    def tostring(self):
        return f"""id:{self.idPeople}, name:{self.name}, surname:{self.surname}, classm:{self.classm}, cf:{self.cf}, gender:{self.gender}, email:{self.email}, birthday:{self.birthday}, sub:{self.sub}"""
