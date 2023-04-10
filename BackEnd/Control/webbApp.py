from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
sys.path.append('./BackEnd/Model/')
import accountDAO as db_A
from dbSession import Account

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

@webApp.get('/qr', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'createQR.html',
		{
			'request': req,
		}
	)

@webApp.post('/api')
async def login(acc:Account):
	try: 
		account = db_A.getLog(nick=acc.getNick().strip())
		if account == None:
			return{
				'message':'Account not exist',
				'success': False
			}
		elif account.__class__ == Exception():
			return{
				'message': account.__str__(),
				'success': False
			}
		else:
			if account.getPass() == acc.getPass():
				return{
					'message':'log',
					'userId' : account.IdAccount,
					'success': True
				}
			else:
				return{
					'message':'wrong password',
					'success': False
				}

	except Exception as e:
		print(e)