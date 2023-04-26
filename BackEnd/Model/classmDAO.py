from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getClassm(year, carrel):
	try:
		with db.session() as s:
			statment = select(db.Classm).where(db.Classm.Year == year and db.Classm.Carrel == carrel.strip())
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e

def getAllClassm():
	try:
		with db.session() as s:
			statment = select(db.Classm)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e

def deletClassm(year, carrel):
	try:
		with db.session() as s:
			statment = select(db.Classm).where(db.Classm.Year == year and db.Classm.Carrel == carrel.strip())
			r = s.exec(statment)
			classm = r.one_or_none()
			if classm != None:
				s.delete(classm)
				s.commit()
				return classm.IdClass
			else:
				return None
	except Exception as e:
		return e

def updateClassm(year, carrel, clas:db.Classm):
	try:
		with db.session() as s:
			statment = select(db.Classm).where(db.Classm.Year == year and db.Classm.Carrel == carrel.strip())
			r = s.exec(statment)
			classm = r.one_or_none()
			if classm != None:
				clas_data = clas.dict(exclude_unset=True)
				for key, value in clas_data.items():
					setattr(classm, key, value)
				s.add(classm)
				s.commit()
				s.refresh(classm)
				return classm.IdClass
			else:
				return None	
	except Exception as e:
		return e

def insertClassm(clas:db.Classm):
	try:
		with db.session() as s:
			try:
				s.add(clas)
				s.commit()
				c = getClassm(year = clas.Year, carrel= clas.Carrel)
				return c.IdClass
			except:
				return None
	except Exception as e:
		return e