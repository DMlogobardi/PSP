import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getEntriescheck(nick):
	try:
		with db.session() as s:
			statment = select(db.Entries).join(db.Account).where(db.Account.nick == nick.strip()).where(db.Entries.dataIn != None).where(db.Entries.dataOut == None)
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e

def getEntriesByIdAccount(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Entries).where(db.Entries.idAccount == id)
				r = s.exec(statment)
				return r.all()
		except Exception as e:
			return e
	else:
		return -1

def getAllEntries():
	try:
		with db.session() as s:
			statment = select(db.Entries)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def deletEntries(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Entries).where(db.Entries.idIng == id)
				r = s.exec(statment)
				entrie = r.one_or_none()
				if entrie != None:
					s.delete(entrie)
					s.commit()
					return entrie.idIng
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1
	
def updateEntries(id, ing:db.Entries):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Entries).where(db.Entries.idIng == id)
				r = s.exec(statment)
				entrie = r.one_or_none()
				if entrie != None:
					ing_data = ing.dict(exclude_unset=True)
					for key, value in ing_data.items():
						setattr(entrie, key, value)
					s.add(entrie)
					s.commit()
					s.refresh(entrie)
					return entrie.idIng
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1
	
def insertEntries(ing:db.Entries):
	try:
		with db.session() as s:
			try:
				s.add(ing)
				s.commit()
				return ing.idAccount
			except:
				return None
	except Exception as e:
		return e

def testFilterEntries(data_payload: Any):
	try:
		with db.session() as s:

			data_filter = json.loads(data_payload)

			query = select(db.Entries)

			if data_filter:
				for field, value in data_filter.items():
					query = query.filter(getattr(db.Entries, field) == value)

			r = s.exec(query)

			return r.fetchall()
		
	except Exception as e:
		return e