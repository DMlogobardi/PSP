import uvicorn
import sys
sys.path.append('./BackEnd/Control/')
from webApp import webApp

if __name__ == '__main__':
		uvicorn.run(
			'webApp:webApp',
			host = '0.0.0.0',
			port = 5000,
			reload = True,
			http = 'httptools'
		)
   