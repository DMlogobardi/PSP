from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from codicefiscale import codicefiscale as Cf
from datetime import date

#funzionante
def getPeopleByCf(cf):
	if Cf.is_valid(cf.strip()):
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.cf == cf.strip())
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1

#funzionante	
def getAllPeople():
	try:
		with db.session() as s:
			statment = select(db.People)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e

#funzionante
def deletPeople(cf):
	if Cf.is_valid(cf.strip()):
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.cf == cf.strip())
				r = s.exec(statment)
				people = r.one_or_none()
				if people != None:
					s.delete(people)
					s.commit()
					return people.idPeople
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1
	
def updatePeople(cf, person:db.People):
	if Cf.is_valid(cf.strip()):
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.cf == cf.strip())
				r = s.exec(statment)
				people = r.one_or_none()
				if people != None:
					person_data = person.dict(exclude_unset=True)
					for key, value in person_data.items():
						setattr(people, key, value)
					s.add(people)
					s.commit()
					s.refresh(people)
					return people.idPeople
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1

#funzionante
def insertPeople(person:db.People):
	if Cf.is_valid(person.cf.strip()):
		try:
			with db.session() as s:
				try:
					s.add(person)
					s.commit()
					p = getPeopleByCf(person.cf.strip())
					return p.idPeople
				except:
					return None
		except Exception as e:
			return e
	else:
		return -1
people1=db.People(name="andrea",surname="cecco",cf="STFNDR80A01L845S",gender="m",email="and.stef@hot.com",birthday=date(2023,4,23),idclass=1)
#people2=db.people(email="peppe.s@itielia.com")

print(updatePeople("STFNDR80A01L845S",people1))
cf="STFNDR80A01L845S"
cf2="DNLPNI89M17L845W"
