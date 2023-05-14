from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from codicefiscale import codicefiscale as Cf

def getPhonesByPeople(cf):
	if Cf.is_valid(cf.strip()):
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
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Phones).where(db.Phones.idPhones == id)
				r = s.exec(statment)
				phone = r.one_or_none()
				if phone != None:
					s.delete(phone)
					s.commit()
					return phone.idPhones
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1
	
def updatePhones(id, cell:db.Phones):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Phones).where(db.Phones.idPhones == id)
				r = s.exec(statment)
				phone = r.one_or_none()
				if phone != None:
					cell_data = cell.dict(exclude_unset=True)
					for key, value in cell_data.items():
						setattr(phone, key, value)
					s.add(phone)
					s.commit()
					s.refresh(phone)
					return phone.idPhones
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1

def insertPhones(cell:db.Phones):
	try:
		with db.session() as s:
			try:
				s.add(cell)
				s.commit()
				return cell.idPhones
			except:
				return None
	except Exception as e:
		return e