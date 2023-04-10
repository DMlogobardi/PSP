from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getPhonesByPeople(cf):
	if len(cf.strip()) == 16:
		try:
			with db.session() as s:
				statment = select(db.Phones).join(db.People).where(db.People.cf == cf.strip())
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
	
def getAllPhones():
	try:
		with db.session() as s:
			statment = select(db.Phones)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def deletPhones(id):
	try:
		with db.session() as s:
			statment = select(db.Phones).where(db.Phones.IdPhones == id)
			r = s.exec(statment)
			phone = r.one_or_none()
			if phone != None:
				s.delete(phone)
				s.commit()
				return phone.getIdPhones()
			else:
				return None
	except Exception as e:
		return e
	
def updatePhones(id, cell:db.Phones):
	try:
		with db.session() as s:
			statment = select(db.Phones).where(db.Phones.getIdPhones() == id)
			r = s.exec(statment)
			phone = r.one_or_none()
			if phone != None:
				s.add(cell)
				s.commit()
				s.refresh(phone)
				return phone.getIdPhones()
			else:
				return None	
	except Exception as e:
		return e

def insertPhones(cell:db.Phones):
	try:
		with db.session() as s:
			s.add(cell)
			s.commit()
	except Exception as e:
		return e