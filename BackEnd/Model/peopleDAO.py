from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from codicefiscale import codicefiscale as Cf

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
	
def getAllPeople():
	try:
		with db.session() as s:
			statment = select(db.People)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
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
					s.add(person)
					s.commit()
					s.refresh(people)
					return people.idPeople
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1
	
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