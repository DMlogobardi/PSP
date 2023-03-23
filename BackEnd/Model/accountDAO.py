from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

def getLog(nick):
	try:
		with db.session() as s:
			statment = select(db.Account).where(db.Account.Nick == nick.strip())
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e