from typing import Any
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date
import hashlib
import sys
sys.path.append('./BackEnd/Model/')
import peopleDAO as db_P
import accountDAO as db_A
import classmDAO as db_C
import phonesDAO as db_PH
import vehiclesDAO as db_V
import entriesDAO as db_E
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
		'index.html',
		{
			'request': req,
		}
	)

@webApp.exception_handler(502)
async def root(req: Request, exc):
	return templates.TemplateResponse(
		'index.html',
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

@webApp.get('/qr', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'createQR.html',
		{
			'request': req,
		}
	)

@webApp.get('/admin', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'admin.html',
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

@webApp.get('/api/gk/{id}')
async def gk(id:int):
	gk = db_A.getAccountGK(id)
	
	if gk == -1:
		return HTTPException(status_code=404, detail=f"{id} not valid")
	
	elif gk == None:
		return HTTPException(status_code=404, detail=f"{id} not found")
	
	else:
		return{
			'message':'riding gk',
			'gk': hashlib.sha256(gk.__str__().encode()).hexdigest() 
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
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
	elif check == None:
		return HTTPException(status_code=404, detail=f"{id} not found")
	
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
			return HTTPException(status_code=502, detail=f"Bad Gatway")
		
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
	if classe == None:
		return HTTPException(status_code=404, detail=f"Class not found")
	
	person.setIdClass(classe.idClass)
	persona = db_P.insertPeople(person)
	if persona == -1:
		return{
			'message':'cf not valid',
			'success': False
		}
	elif persona.__class__ == Exception():
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
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
			return HTTPException(status_code=502, detail=f"Bad Gatway")
		
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
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
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
			return HTTPException(status_code=502, detail=f"Bad Gatway")
		
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
			return HTTPException(status_code=404, detail=f"{id} not found")
		
		elif acc.__class__ == Exception():
			return HTTPException(status_code=502, detail=f"Bad Gatway")
		
		else:
			person = db_P.getPeopleById(acc.idPeople)

			if person == None:
				return{
					'message':'id person not exists',
					'success': False
				}
			elif person.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				phone.setIdPeople(person.idPeople)
				ph = db_PH.insertPhones(phone)
	
				if ph == None:
					return{
						'message':'phone already exists',
						'success': False
					}
				elif ph.__class__ == Exception():
					return HTTPException(status_code=502, detail=f"Bad Gatway")
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
						return HTTPException(status_code=502, detail=f"Bad Gatway")
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
							return HTTPException(status_code=502, detail=f"Bad Gatway")
						else:
							return{
								'message':'finish registration',
								'success': True
							}
	else:
		return HTTPException(status_code=404, detail=f"{id} not found")
	

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
			return HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
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
			return db_A.getAllAccount()

		elif object.strip().lower() == "entris":
			for id in listId:
				if id > 0 != None:
					db_E.deletEntries(id)
			
		else:
			return HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.put('/api/update/{object}/{id}')
async def read(object: str, id: int , data: Any= Header(None)):
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
					return HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "classm":
			if id > 0 and id != None:
				classm = db.createClassm(data)
				r = db_C.updateClassm(id= id, clas= classm)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					return HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "phone":
			if id > 0 and id != None:
				phone = db.createPhones(data)
				r = db_PH.updatePhones(id= id, cell= phone)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					return HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "vehicle":
			if id > 0 and id != None:
				vehicle = db.createVehicles(data)
				r = db_V.updateVehicles(id= id, car= vehicle)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					return HTTPException(status_code=404, detail=f"{id} not found")
		
		elif object.strip().lower() == "account":
			if id > 0 and id != None:
				account = db.createAccount(data)
				r = db_A.updateAccount(id= id, acc= account)
				if r != None and r.__class__ != Exception():
					return{
						'message': 'ok'
					}
				else:
					return HTTPException(status_code=404, detail=f"{id} not found")
		
		else:
			return HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		print(e)
		return HTTPException(status_code=502, detail=f"Bad Gatway")
	
@webApp.put('/api/insert/{object}')
async def read(object: str, data: Any= Header(None)):
	try:
		if object.strip().lower() == "person":
			person = db.createPeople(data)
			r= db_P.insertPeople(person)

			if r == None:
				return HTTPException(status_code=404, detail=f"person alredy exist")

			elif r.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
		
		elif object.strip().lower() == "classm":
			classm = db.createClassm(data)
			r= db_C.insertClassm(classm)

			if r == None:
				return HTTPException(status_code=404, detail=f"classm alredy exist")
			elif r.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
			
		elif object.strip().lower() == "phone":
			phone = db.createPhones(data)
			r= db_PH.insertPhones(phone)

			if r == None:
				return HTTPException(status_code=404, detail=f"phone alredy exist")
			elif r.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r
			
		elif object.strip().lower() == "vehicle":
			vehicle = db.createVehicles(data)
			r= db_V.insertVehicles(vehicle)

			if r == None:
				return HTTPException(status_code=404, detail=f"vehicle alredy exist")
			elif r.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r

		elif object.strip().lower() == "account":
			account = db.createAccount(data)
			r= db_A.insertAccount(account)

			if r == None:
				return HTTPException(status_code=404, detail=f"account alredy exist")
			elif r.__class__ == Exception():
				return HTTPException(status_code=502, detail=f"Bad Gatway")
			else:
				return r

		else:
			return HTTPException(status_code=404, detail=f"{object} not found")
		
	except Exception as e:
		return HTTPException(status_code=502, detail=f"Bad Gatway")
'''	
@webApp.put('/api/filter/{object}')
async def read(object: str):
	try:
		if object.strip().lower() == "person":
			pass
		
		elif object.strip().lower() == "classm":
			pass
		
		elif object.strip().lower() == "phone":
			pass
		
		elif object.strip().lower() == "vehicle":
			pass
		
		elif object.strip().lower() == "account":
			pass
		
		elif object.strip().lower() == "entris":
			pass
		
		else:
			return{
				'message':'not have table'
			}
	except Exception as e:
		return e'''