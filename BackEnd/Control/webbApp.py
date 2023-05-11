from fastapi import FastAPI, Request
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

@webApp.get('/api/gk/{id}')
async def gk(id:int):
	gk = db_A.getAccountGK(id)
	if gk == -1:
		return{
			'message':'Invalid id'
		}
	elif gk == None:
		return{
			'message':'Account not exist'
		}
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
		return{
			'message':check.__str__()
		}
	elif check == None:
		return{
			'message': 'id not exist'
		}
	else:
		return{
			'message': True,
			'nick': check.Nick
		}

@webApp.post('/api/log')
async def login(acc:db.Account):
	try: 
		account = db_A.getLog(acc.Nick.strip())
		print(account)
		if account == None:
			return {
				'message':'Account not exist',
				'success': False
			}
		elif account.__class__ == Exception():
			return{
				'message': account.__str__(),
				'success': False
			}
		elif account.DataExp != None:
			return{
				'message':'Inactive account',
				'DataExp': account.DataExp.__str__(),
				'success': False
			}
		else:
			if account.getPass() == acc.getPass():
				if account.valid == 'T':
					return{
						'message':'reg2',
						'userId' : account.IdAccount,
						'ruolo' : account.Ruolo,
						'nick' : account.Nick,
						'success': True
					}
				elif account.valid == 'O':
					return{
						'message':'log',
						'userId' : account.IdAccount,
						'ruolo' : account.Ruolo,
						'nick' : account.Nick,
						'success': True
					}
				elif (account.DataReg - date.today()) == 31:
					p = db_P.getPeopleById(account.IdPeople)
					db_A.deletAccount(account.Nick)
					db_P.deletPeople(p.cf)
					return{
						'message':'account exp out of range',
						'success': False
					}
				else:
					return{
						'message':'account not acctivate',
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
	classe = db_C.getClassm(year=classm.Year, carrel=classm.Carrel)
	if classe == None:
		return{
				'massage':'ok manco una lista sai usare',
				'success': False
			}
	
	person.setIdClass(classe.IdClass)
	persona = db_P.insertPeople(person)
	if persona == -1:
		return{
			'message':'cf not valid',
			'success': False
		}
	elif persona.__class__ == Exception():
		return{
			'message': 'person alredy exist',
			'error': persona,
			'success': False
		}
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
			return{
				'message': account.__str__(),
				'success': False
			}
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
		return{
			'message': 'person alredy exist',
			'error': persona,
			'success': False
		}
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
			return{
				'message': account.__str__(),
				'success': False
			}
		elif account == None:
			db_P.deletPeople(person.cf)
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
			return{
				'message':'id ERROR',
				'success': False
			}
		elif acc.__class__ == Exception():
			return{
				'message':'ERROR',
				'success': False
			}
		else:
			person = db_P.getPeopleById(acc.idPeople)

			if person == None:
				return{
					'message':'id not exists',
					'success': False
				}
			elif person.__class__ == Exception():
				return{
					'message':'ok sono esploso male',
					'success': False
				}
			else:
				phone.setIdPeople(person.idPeople)
				ph = db_PH.insertPhones(phone)
	
				if ph == None:
					return{
						'message':'phone already exists',
						'success': False
					}
				elif ph.__class__ == Exception():
					return{
						'message':'ok sono esploso male',
						'success': False
					}
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
						return{
							'message':'ok sono esploso male',
							'success': False
						}
					else:
						acc.valid = "O"
						a= db_A.updateAccount(nick= acc.Nick, acc= acc)
						
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
							return{
								'message':'ok sono esploso male',
								'success': False
							}
						else:
							return{
								'message':'finish registration',
								'success': True
							}
	else:
		return{
			'message':'id ERROR',
			'success': False
		}
	

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
			return{
				'message':'not have table'
			}
	except Exception as e:
		return e
	
@webApp.delete('/api/delete/{object}')
async def read(object: str, listId: list[int]):
	try:
		if object.strip().lower() == "person":
			for id in listId:
				p= db_P.getPeopleById(id)

				if p != None and p.__class__ != Exception():
					ph= db_PH.getPhonesByPeople(p.cf)

					if ph != None and ph.__class__ != Exception():
						v= db_V.getVehiclesByPeople(p.cf)

						if v != None and v.__class__ != Exception():
							acc= db_A.getAccountByPeople(p.cf)

							if acc != None and acc.__class__ != Exception():
								acc.idPeople = None
								acc.DataExp = date().today()
								acc2= db_A.updateAccount(nick= acc.Nick, acc= acc)

								if acc2 != None and acc2.__class__ != Exception():
									db_PH.deletPhones(ph.IdPhones)
									db_V.deletVehicles(v.IdV)
									db_P.deletPeople(id)
								else:
									return{
										'id': id,
										'message':'id not deleted'
									}
							else:
								return{
										'id': id,
										'message':'id not deleted'
									}
						else:
							return{
										'id': id,
										'message':'id not deleted'
									}
					else:
						return{
							'id': id,
							'message':'id not deleted'
						}
				else:
					return{
						'id': id,
						'message':'id not deleted'
					}
				
		elif object.strip().lower() == "classm":
			for id in listId:
				person = db_P.getPeopleByClassm(id)

				if person != None and person.__class__ != Exception():
					for p in person:
						p.IdClass = None
						db_P.updatePeople(cf= p.cf, person= p)
					db_C.deletClassm()

		elif object.strip().lower() == "phone":
			for id in listId:
				db_PH.deletPhones(id)

		elif object.strip().lower() == "vehicle":
			for id in listId:
				db_V.deletVehicles(id)

		elif object.strip().lower() == "account":
			for id in listId:
				e= db_E.getEntriesByIdAccount(id)
				if e != None and e.__class__ != Exception():
					for entre in e:
						db_E.deletEntries(entre.IdIng)
					db_A.deletAccount(id)

		elif object.strip().lower() == "entris":
			for id in listId:
				db_E.deletEntries(id)
			
		else:
			return{
				'message':'not have table'
			}
	except Exception as e:
		return e
	
@webApp.put('/api/update/people/{cf}')
async def read(cf: str, people:db.People):
	pass

@webApp.put('/api/update/classm/{id}')
async def read(id: int, classm:db.Classm):
	pass

@webApp.put('/api/update/entries/{id}')
async def read(id: int, entrie:db.Entries):
	pass

@webApp.put('/api/update/account/{nick}')
async def read(nick: str, classm:db.Classm):
	pass