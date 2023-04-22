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
	
def deletVehicles(plate):
	try:
		with db.session() as s:
			statment = select(db.Vehicles).where(db.Vehicles.Plate == plate.strip())
			r = s.exec(statment)
			vehicle = r.one_or_none()
			if vehicle != None:
				s.delete(vehicle)
				s.commit()
				return vehicle.IdV
			else:
				return None
	except Exception as e:
		return e
	
def updateVehicles(plate, car:db.Vehicles):
	try:
		with db.session() as s:
			statment = select(db.Vehicles).where(db.Vehicles.Plate == plate.strip())
			r = s.exec(statment)
			vehicle = r.one_or_none()
			if vehicle != None:
				s.add(car)
				s.commit()
				s.refresh(vehicle)
				return vehicle.IdV
			else:
				return None	
	except Exception as e:
		return e
	
def insertVehicles(car:db.Vehicles):
	try:
		with db.session() as s:
			try:
				s.add(car)
				s.commit()
				return car.IdV
			except:
				return None
	except Exception as e:
		return e