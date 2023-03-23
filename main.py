import uvicorn
import sys
sys.path.append('./BackEnd/Control/')
from webbApp import webApp

if __name__ == '__main__':
		uvicorn.run(
			'webbApp:webApp',
			host = '0.0.0.0',
			port = 8080,
			reload = True,
			http = 'httptools'
		)
   