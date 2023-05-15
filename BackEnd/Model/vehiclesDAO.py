import json
from typing import Any
from sqlmodel import select
import sys
sys.path.append('./BackEnd/DB/')
import dbSession as db
from codicefiscale import codicefiscale as Cf

def getVehiclesByPeople(cf):
	if Cf.is_valid(cf.strip()):
		try:
			with db.session() as s:
				statment = select(db.Vehicles).join(db.People).where(db.People.cf == cf.strip())
				r = s.exec(statment)
				return r.one_or_none()
		except Exception as e:
			return e
	else:
		return -1
	
def getAllVehicles():
	try:
		with db.session() as s:
			statment = select(db.Vehicles)
			r = s.exec(statment)
			return r.all()
	except Exception as e:
		return e
	
def deletVehicles(id):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Vehicles).where(db.Vehicles.idV == id)
				r = s.exec(statment)
				vehicle = r.one_or_none()
				if vehicle != None:
					s.delete(vehicle)
					s.commit()
					return vehicle.idV
				else:
					return None
		except Exception as e:
			return e
	else:
		return -1
	
def updateVehicles(id, car:db.Vehicles):
	if id > 0:
		try:
			with db.session() as s:
				statment = select(db.Vehicles).where(db.Vehicles.idV == id)
				r = s.exec(statment)
				vehicle = r.one_or_none()
				if vehicle != None:
					car_data = car.dict(exclude_unset=True)
					for key, value in car_data.items():
						setattr(vehicle, key, value)
					s.add(vehicle)
					s.commit()
					s.refresh(vehicle)
					return vehicle.idV
				else:
					return None	
		except Exception as e:
			return e
	else:
		return -1
	
def insertVehicles(car:db.Vehicles):
	try:
		with db.session() as s:
			try:
				s.add(car)
				s.commit()
				return car.idV
			except:
				return None
	except Exception as e:
		return e
	
def testFilterVehicles(data_payload: Any):
	try:
		with db.session() as s:
			
			data_filter = json.loads(data_payload)

			query = select(db.Vehicles)

			if data_filter:
				for field, value in data_filter.items():
					query = query.filter(getattr(db.Vehicles, field) == value)

			r = s.exec(query)

			return r.fetchall()
		
	except Exception as e:
		return e