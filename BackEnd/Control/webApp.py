import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
			'title': 'ShoppingList',
		}
	)

@webApp.get('/login', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'login.html',
		{
			'request': req,
			'title': 'ShoppingList',
		}
	)

@webApp.get('/qr', response_class = HTMLResponse)
async def root(req: Request):
	return templates.TemplateResponse(
		'createQR.html',
		{
			'request': req,
			'title': 'ShoppingList',
		}
	)

if __name__ == '__main__':
	uvicorn.run(
		'webApp:webApp',
		host = '0.0.0.0',
		port = 80,
		reload = True,
		http = 'httptools'
	)