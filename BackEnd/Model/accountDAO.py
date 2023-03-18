from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db

try:
     with db.session() as s:
        res = s.exec(select(db.Account))
        for account in res:
            print(f"{account.__str__()}")
except Exception as e:
    print(e) 
