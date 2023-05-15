import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from codicefiscale import codicefiscale as Cf

def getPeopleById(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.idPeople == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
	
def getPeopleByAccount(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.People).join(db.Account).where(db.Account.idAccount == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
	
def getPeopleByClassm(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.People).join(db.Classm).where(db.Classm.idClass == id)
				r = s.exec(statment)
				return r.all()
		except Exception as e:
			return e
	else:
		return -1

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
def deletPeople(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.idPeople == id)
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
	
def updatePeople(id, person:db.People):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.People).where(db.People.idPeople == id)
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
	
def testFilterPeople(data_payload: Any):
	try:
		with db.session() as s:
			
			data_filter = json.loads(data_payload)

			query = select(db.People)

			if data_filter:
				for field, value in data_filter.items():
					query = query.filter(getattr(db.People, field) == value)

			r = s.exec(query)

			return r.fetchall()
		
	except Exception as e:
		return e