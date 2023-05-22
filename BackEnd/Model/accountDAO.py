import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

#funzionante
def getLog(nick):
	try:
		with db.session() as s:
			statment = select(db.Account).where(db.Account.nick == nick.strip())
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e
	
def getAccountById(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account).where(db.Account.idAccount == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
	
def getAccountByIdPeople(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account).where(db.Account.idPeople == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
		
def getAccountGK(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account.gK).where(db.Account.idAccount == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1

def getAllAccount():
	try:
		with db.session() as s:
			statment = select(db.Account).order_by(db.Account.idAccount)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def getAllAccountGK():
	try:
		with db.session() as s:
			statment = select(db.Account.gK)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
		
def deletAccount(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account).where(db.Account.idAccount == id)
				r = s.exec(statment)
				account = r.one_or_none()
				if account != None:
					s.delete(account)
					s.commit()
					return account.idAccount
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1

def updateAccount(id, acc:db.Account):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account).where(db.Account.idAccount == id)
				r = s.exec(statment)
				account = r.one_or_none()
				if account != None:
					acc_data = acc.dict(exclude_unset=True)
					for key, value in acc_data.items():
						setattr(account, key, value)
					s.add(account)
					s.commit()
					s.refresh(account)
					return account.idAccount
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1	

#funzionante
def insertAccount(acc:db.Account):
	try:
		with db.session() as s:
			try:
				s.add(acc)
				s.commit()
				a = getLog(acc.nick.strip())
				return a.idAccount
			except:
				return None
	except Exception as e:
		return e
	
def testFilterAccount(data_payload: Any):
	try:
		with db.session() as s:
			
			data_json = json.dumps(data_payload)
			data_filter = json.loads(data_json)

			query = select(db.Account)

			if data_filter:
				for field, value in data_filter.items():
					query = query.filter(getattr(db.Account, field) == value)

			r = s.exec(query)

			return r.fetchall()
		
	except Exception as e:
		return e