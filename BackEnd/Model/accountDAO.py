from sqlmodel import select
import hashlib
from datetime import date
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getLog(nick):
	try:
		with db.session() as s:
			#statment = select(db.Account).where(db.Account.Nick == nick.strip())
			r = s.query(db.Account).where(db.Account.Nick == nick.strip())
			return r.all()	
	except Exception as e:
		print(e)