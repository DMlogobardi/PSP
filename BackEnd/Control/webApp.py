from typing import Any
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date
import sys
sys.path.append('./BackEnd/Model/')
import peopleDAO as db_P
import accountDAO as db_A
import classmDAO as db_C
import phonesDAO as db_PH
import vehiclesDAO as db_V
import entriesDAO as db_E
import otherQery as o_Q
sys.path.append('./BackEnd/DB/')
import dbSession as db
sys.path.append('./BackEnd/Control/')
import gkGenerator as gk_gen

webApp = FastAPI()
templates = Jinja2Templates (
	directory = 'FrontEnd/pages'
)

webApp.mount(
	'/static',
	app = StaticFiles(directory = 'FrontEnd/static'),
	name = 'static'
)

# start your main file
@webApp.get('/', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'index.html',
		{
			'request': req,
		}
	)

@webApp.exception_handler(404)
async def root(req: Request, exc):
	return templates.TemplateResponse(
		'error404.html',
		{
			'request': req,
		}
	)

@webApp.get('/login', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'login.html',
		{
			'request': req,
		}
	)

@webApp.get('/register1', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'registerPart1.html',
		{
			'request': req,
		}
	)

@webApp.get('/register2', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'registerPart2.html',
		{
			'request': req,
		}
	)

@webApp.get('/admin', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'adminV2.html',
		{
			'request': req,
		}
	)

@webApp.get('/profile', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'profile.html',
		{
			'request': req,
		}
	)

@webApp.get('/recoverPassword', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'password.html',
		{
			'request': req,
		}
	)

@webApp.get('/api/gk/{id}')
async def gk(id:int):
	gk = db_A.getAccountGK(id)
	
	if gk == -1:
		raise HTTPException(status_code=404, detail=f"{id} not valid")
	
	elif gk == None:
		raise HTTPException(status_code=404, detail=f"{id} not found")
	
	else:
		return{
			'message':'riding gk',
			'gk': gk
		}

@webApp.get('/class')
async def classm():
	return db_C.getValidClassm()

@webApp.get('/api/checkLog/{id}')
async def check(id:int):
	check = db_A.getAccountById(id)

	if check == -1:
		return{
			'message':'invalid id'
		}
	elif check.__class__ == Exception:
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
	elif check == None:
		raise HTTPException(status_code=404, detail=f"{id} not found")
	
	else:
		return{
			'message': True,
			'nick': check.nick
		}

@webApp.post('/api/log')
async def login(acc:db.Account):
	try: 
		account = db_A.getLog(acc.nick.strip())
		print(account)
		if account == None:
			return {
				'message':'Account not exist',
				'success': False
			}
		elif account.__class__ == Exception():
			raise HTTPException(status_code=502, detail=f"Bad Gatway")
		
		elif account.dataExp != None:
			return{
				'message':'Inactive account',
				'DataExp': account.dataExp.__str__(),
				'success': False
			}
		else:
			if account.getP_ass() == acc.getP_ass():
				if account.valid == 'T':
					return{
						'message':'reg2',
						'userId' : account.idAccount,
						'ruolo' : account.ruolo,
						'nick' : account.nick,
						'success': True
					}
				elif account.valid == 'O':
					return{
						'message':'log',
						'userId' : account.idAccount,
						'ruolo' : account.ruolo,
						'nick' : account.nick,
						'success': True
					}
				elif (account.dataReg - date.today()) == 31:
					p = db_P.getPeopleById(account.idPeople)
					db_A.deletAccount(account.nick)
					db_P.deletPeople(p.cf)
					return{
						'message':'account exp out of range',
						'success': False
					}
				else:
					return{
						'message':'account not activate',
						'success': False
					}
			else:
				return{
					'message':'wrong password',
					'success': False
				}

	except Exception as e:
		print(e)

@webApp.post('/api/reg1/student')
async def reg(classm:db.Classm, person:db.People, acc:db.Account):
	classe = db_C.getClassm(year=classm.year, carrel=classm.carrel)
	if classe == None and classe.__class__ == Exception:
		raise HTTPException(status_code=404, detail=f"Class not found")
	
	person.setIdClass(classe.idClass)
	persona = db_P.insertPeople(person)
	if persona == -1:
		return{
			'message':'cf not valid',
			'success': False
		}
	elif persona.__class__ == Exception():
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
	elif persona == None:
		return{
			'message': 'person alredy exist',
			'success': False
		}
	else:
		acc.setGK(gk_gen.gkGenerator())
		acc.idPeople = persona
		acc.valid = "F"
		account = db_A.insertAccount(acc)

		if account.__class__ == Exception():
			raise HTTPException(status_code=502, detail=f"Bad Gatway")
		
		elif account == None:
			db_P.deletPeople(person.cf)
			return{
				'message': 'account alredy exist',
				'success': False
			}
		else:
			return{
				'message':'perfetto',
				'success': True,
				'object' : account 
			}
		
@webApp.post('/api/reg1/other')
async def reg(person:db.People, acc:db.Account):

	persona = db_P.insertPeople(person)
	if persona == -1:
		return{
			'message':'cf not valid',
			'success': False
		}
	elif persona.__class__ == Exception():
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
	elif persona == None:
		return{
			'message': 'person alredy exist',
			'success': False
		}
	else:
		acc.setGK(gk_gen.gkGenerator())
		acc.idPeople = persona
		acc.valid = "F"
		account = db_A.insertAccount(acc)

		if account.__class__ == Exception():
			raise HTTPException(status_code=502, detail=f"Bad Gatway")
		
		elif account == None:
			db_P.deletPeople(person.idPeople)
			return{
				'message': 'account alredy exist',
				'success': False
			}
		else:
			return{
				'message':'perfetto',
				'success': True
			}
		
@webApp.post('/api/reg2/{id}')
async def reg(id: int, phone:db.Phones, vehicle:db.Vehicles):
	
	if id != None and id > 0:
		acc = db_A.getAccountById(id)

		if acc == None:
			raise HTTPException(status_code=404, detail=f"{id} not found")
		
		elif acc.__class__ == Exception():
			raise HTTPException(status_code=502, detail=f"Bad Gatway")
		
		else:
			person = db_P.getPeopleById(acc.idPeople)

			if person == None:
				return{
					'message':'id person not exists',
					'success': False
				}
			elif person.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				phone.setIdPeople(person.idPeople)
				ph = db_PH.insertPhones(phone)
	
				if ph == None:
					return{
						'message':'phone already exists',
						'success': False
					}
				elif ph.__class__ == Exception():
					raise HTTPException(status_code=502, detail=f"Bad Gatway")
				else:
					vehicle.setIdPeople(person.idPeople)
					vec = db_V.insertVehicles(vehicle)
					if vec == None:
						db_PH.deletPhones(ph)
						return{
							'message':'vehicle already exists',
							'success': False
						}
					elif ph.__class__ == Exception():
						db_PH.deletPhones(ph)
						raise HTTPException(status_code=502, detail=f"Bad Gatway")
					else:
						acc.valid = "O"
						a= db_A.updateAccount(id= acc.idAccount, acc= acc)
						
						if a == None:
							db_PH.deletPhones(ph)
							db_V.deletVehicles(vec)
							return{
								'message': 'account not exist',
								'success': False
							}
						elif a.__class__ == Exception():
							db_PH.deletPhones(ph)
							db_V.deletVehicles(vec)
							raise HTTPException(status_code=502, detail=f"Bad Gatway")
						else:
							return{
								'message':'finish registration',
								'success': True
							}
	else:
		raise HTTPException(status_code=404, detail=f"{id} not found")
	

@webApp.get('/api/read/{object}')
async def read(object: str):
	try:
		if object.strip().lower() == "person":
			return db_P.getAllPeople()
		
		elif object.strip().lower() == "classm":
			return db_C.getAllClassm()
		
		elif object.strip().lower() == "phone":
			return db_PH.getAllPhones()
		
		elif object.strip().lower() == "vehicle":
			return db_V.getAllVehicles()
		
		elif object.strip().lower() == "account":
			return db_A.getAllAccount()
		
		elif object.strip().lower() == "entris":
			return db_E.getAllEntries()
		
		else:
			raise HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		print(e)
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.delete('/api/delete/{object}')
async def read(object: str, listId: list[int]):
	try:
		if object.strip().lower() == "person":
			for id in listId:
				if id > 0 != None:
					acc =db_A.getAccountByIdPeople(id)
					if acc != None and acc.__class__ != Exception():
						acc.dataExp = date.today()
						db_A.updateAccount(id= acc.idAccount, acc= acc)
						db_P.deletPeople(id)

		elif object.strip().lower() == "classm":
			for id in listId:
				if id > 0 != None:
					db_C.deletClassm(id)

		elif object.strip().lower() == "phone":
			for id in listId:
				if id > 0 != None:
					db_PH.deletPhones(id)

		elif object.strip().lower() == "vehicle":
			for id in listId:
				if id > 0 != None:
					db_V.deletVehicles(id)

		elif object.strip().lower() == "account":
			for id in listId:
				if id > 0 != None:
					db_A.deletAccount(id)

		elif object.strip().lower() == "entris":
			for id in listId:
				if id > 0 != None:
					db_E.deletEntries(id)
			
		else:
			raise HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.put('/api/update/{object}/{id}')
async def read(object: str, id: int , data: Any = Body()):
	try:
		if object.strip().lower() == "person":
			if id > 0 and id != None:
				person = db.createPeople(data)
				r = db_P.updatePeople(id= id, person= person)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					raise HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "classm":
			if id > 0 and id != None:
				classm = db.createClassm(data)
				r = db_C.updateClassm(id= id, clas= classm)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					raise HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "phone":
			if id > 0 and id != None:
				phone = db.createPhones(data)
				r = db_PH.updatePhones(id= id, cell= phone)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					raise HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "vehicle":
			if id > 0 and id != None:
				vehicle = db.createVehicles(data)
				r = db_V.updateVehicles(id= id, car= vehicle)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					raise HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "account":
			if id > 0 and id != None:
				account = db.createAccount(data)
				r = db_A.updateAccount(id= id, acc= account)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					raise HTTPException(status_code=404, detail=f"{id} not found")
		
		else:
			raise HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.put('/api/insert/{object}')
async def read(object: str, data: Any = Body()):
	try:
		if object.strip().lower() == "person":
			person = db.createPeople(data)
			r= db_P.insertPeople(person)

			if r == None:
				raise HTTPException(status_code=404, detail=f"person alredy exist")

			elif r.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
		
		elif object.strip().lower() == "classm":
			classm = db.createClassm(data)
			r= db_C.insertClassm(classm)

			if r == None:
				raise HTTPException(status_code=404, detail=f"classm alredy exist")
			elif r.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
			
		elif object.strip().lower() == "phone":
			phone = db.createPhones(data)
			r= db_PH.insertPhones(phone)

			if r == None:
				raise HTTPException(status_code=404, detail=f"phone alredy exist")
			elif r.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
			
		elif object.strip().lower() == "vehicle":
			vehicle = db.createVehicles(data)
			r= db_V.insertVehicles(vehicle)

			if r == None:
				raise HTTPException(status_code=404, detail=f"vehicle alredy exist")
			elif r.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r

		elif object.strip().lower() == "account":
			account = db.createAccount(data)
			r= db_A.insertAccount(account)

			if r == None:
				raise HTTPException(status_code=404, detail=f"account alredy exist")
			elif r.__class__ == Exception():
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r

		else:
			raise HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		 raise HTTPException(status_code=502, detail=f"Bad Gatway")

@webApp.put('/api/filter/{object}')
async def read(object: str, data: Any = Body()):
	try:
		if object.strip().lower() == "person":
			r = db_P.testFilterPeople(data)
			return r
		
		elif object.strip().lower() == "classm":
			r = db_C.testFilterClassm(data)
			return r
		
		elif object.strip().lower() == "phone":
			r = db_PH.testFilterPhones(data)
			return r
		
		elif object.strip().lower() == "vehicle":
			r = db_V.testFilterVehicles(data)
			return r
		
		elif object.strip().lower() == "account":
			r = db_A.testFilterAccount(data)
			return r
		
		elif object.strip().lower() == "entris":
			r = db_E.testFilterEntries(data)
			return r
		
		elif object.strip().lower() == "join":
			r = o_Q.testReadJoin(data)
			return r

		else:
			raise HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception:
		raise HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.put('/api/validate')
async def read(listId: list[int]):
	try:
		listException = []
		for id in listId:
			acc =db_A.getAccountById(id)
			if acc != None and acc.__class__ != Exception() and acc != -1:
				if acc.valid == "F":
					acc.valid = "T"
					db_A.updateAccount(id= acc.idAccount, acc= acc)
				else:
					listException.append(HTTPException(status_code=404, detail=f"{id}: is valid"))
			else:
				listException.append(HTTPException(status_code=502, detail=f"{id}: Bad Gatway"))
		
		if len(listException) == 0:
			return{
				'message': 'validate all list'
			}
		else:
			return listException
		
	except Exception as e:
		raise HTTPException(status_code=502, detail=f"Bad Gatway")

@webApp.put('/api/forgotPassword/{nick}')
async def read(nick: str, passw: dict = Body()):
	try:
		if nick.strip().lower() != "admin" and len(passw['passw']) == 64:
			acc =db_A.getLog(nick)
			if acc != None and acc.__class__ != Exception() and acc != -1:
					if acc.valid != "F" or acc.dataExp != None:
						raise HTTPException(status_code=402, detail=f"{acc.idAccount}: Is invalid account")
					acc.p_ass = passw["passw"]
					if db_A.updateAccount(id= acc.idAccount, acc= acc) != None:
						return True
					return False
			else:
				raise HTTPException(status_code=502, detail=f"Bad Gatway")
		return False

	except Exception as e:
		raise e
