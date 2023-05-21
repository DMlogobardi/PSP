import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getClassm(year, carrel):
	try:
		with db.session() as s:
			statment = select(db.Classm).where(db.Classm.year == year).where(db.Classm.carrel == carrel.strip())
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e

def getAllClassm():
	try:
		with db.session() as s:
			statment = select(db.Classm).order_by(db.Classm.carrel)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def getValidClassm():
	try:
		with db.session() as s:
			statment = select(db.Classm).where(db.Classm.active == "YES")
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e

def deletClassm(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Classm).where(db.Classm.idClass == id)
				r = s.exec(statment)
				classm = r.one_or_none()
				if classm != None:
					s.delete(classm)
					s.commit()
					return classm.idClass
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1

def updateClassm(id, clas:db.Classm):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Classm).where(db.Classm.idClass == id)
				r = s.exec(statment)
				classm = r.one_or_none()
				if classm != None:
					clas_data = clas.dict(exclude_unset=True)
					for key, value in clas_data.items():
						setattr(classm, key, value)
					s.add(classm)
					s.commit()
					s.refresh(classm)
					return classm.idClass
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1

def insertClassm(clas:db.Classm):
	try:
		with db.session() as s:
			try:
				s.add(clas)
				s.commit()
				c = getClassm(year = clas.year, carrel= clas.carrel)
				return c.idClass
			except Exception as e:
				print(e)
				return None
	except Exception as e:
		return e
	
def testFilterClassm(data_payload: Any):
	try:
		with db.session() as s:

			data_filter = json.loads(data_payload)

			query = select(db.Classm)

			if data_payload:
				for field, value in data_filter.items():
					query = query.filter(getattr(db.Classm, field) == value)

			r = s.exec(query)

			return r.all()
		
	except Exception as e:
		return e