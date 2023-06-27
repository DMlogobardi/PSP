import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from sqlmodel import text

def testReadJoin(data_payload: Any):
	try:
		with db.session() as s:
			
			data_json = json.dumps(data_payload)
			data_filter = json.loads(data_json)

			if data_filter:
				query = select(getattr(db, data_filter["class"])).join(getattr(db, data_filter["join"])).where(getattr(getattr(db, data_filter["class"]), data_filter["condiction"]) == data_filter["value"])

			r = s.exec(query)

			return r.all()
		
	except Exception as e:
		return e
