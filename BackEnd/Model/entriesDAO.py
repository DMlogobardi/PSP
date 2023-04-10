from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getEntriesByAccount(nick):
	try:
		with db.session() as s:
			statment = select(db.Entries).join(db.Account).where(db.Account.Nick == nick.strip())
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e

def getEntries():
	try:
		with db.session() as s:
			statment = select(db.Entries)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def deletEntries(id):
	try:
		with db.session() as s:
			statment = select(db.Entries).where(db.Entries.IdIng == id)
			r = s.exec(statment)
			entrie = r.one_or_none()
			if entrie != None:
				s.delete(entrie)
				s.commit()
				return entrie.getIdIng()
			else:
				return None
	except Exception as e:
		return e
	
def updateEntries(id, ing:db.Entries):
	try:
		with db.session() as s:
			statment = select(db.Entries).where(db.Entries.IdIng == id)
			r = s.exec(statment)
			entrie = r.one_or_none()
			if entrie != None:
				s.add(ing)
				s.commit()
				s.refresh(entrie)
				return entrie.getIdIng()
			else:
				return None	
	except Exception as e:
		return e
	
def insertEntries(ing:db.Entries):
	try:
		with db.session() as s:
			s.add(ing)
			s.commit()
	except Exception as e:
		return e