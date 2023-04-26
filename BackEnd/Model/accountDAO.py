from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
import hashlib

#funzionante
def getLog(nick):
	try:
		with db.session() as s:
			statment = select(db.Account).where(db.Account.Nick == nick.strip())
			r = s.exec(statment)
			return r.one_or_none()
	except Exception as e:
		return e
	
def getAccountById(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Account).where(db.Account.IdAccount == id)
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e

	
def getAllAccount():
	try:
		with db.session() as s:
			statment = select(db.Account)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def getAllAccountGK():
	try:
		with db.session() as s:
			statment = select(db.Account.GK)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
		
def deletAccount(nick):
	try:
		with db.session() as s:
			statment = select(db.Account).where(db.Account.Nick == nick.strip())
			r = s.exec(statment)
			account = r.one_or_none()
			if account != None:
				s.delete(account)
				s.commit()
				return account.IdAccount
			else:
				return None
	except Exception as e:
		return e

def updateAccount(nick, acc:db.Account):
	try:
		with db.session() as s:
			statment = select(db.Account).where(db.Account.Nick == nick.strip())
			r = s.exec(statment)
			account = r.one_or_none()
			if account != None:
				acc_data = acc.dict(exclude_unset=True)
				for key, value in acc_data.items():
					setattr(account, key, value)
				s.add(account)
				s.commit()
				s.refresh(account)
				return account.IdAccount
			else:
				return None	
	except Exception as e:
		return e	

#funzionante
def insertAccount(acc:db.Account):
	try:
		with db.session() as s:
			try:
				s.add(acc)
				s.commit()
				a = getLog(acc.Nick.strip())
				return a.IdAccount
			except:
				return None
	except Exception as e:
		return e
