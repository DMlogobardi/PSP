import socket
from datetime import datetime
import hashlib
import sys
sys.path.append('./BackEnd/Model/')
sys.path.append('./BackEnd/DB/')
import dbSession as db
import accountDAO as db_A
import entriesDAO as db_E

HOST = '0.0.0.0'
PORT = 12345

s = socket.socket()		
print(f'TCP Server Listening on {HOST}:{PORT}..')

s.bind((HOST, PORT))
s.listen(1)

while True:
	con, addr = s.accept()
	stringone  = con.recv(312).decode().strip().split("!")

	id = int(stringone[2])
	acc = db_A.getAccountById(id)
	if acc != None:
		if stringone[4].strip() == hashlib.sha1(acc.GK.encode()).hexdigest():
			if stringone[1] == "i":
				i = db_E.getEntriescheck(nick= acc.Nick)
				if i == None:
					data_in = datetime.strptime(stringone[5], "%Y/%m/%d %H:%M:%S")
					ing = db.Entries(DataIn= data_in, IdAccount=acc.IdAccount)
					msg = db_E.insertEntries(ing)
					
					if msg.__class__ == Exception():
						print(msg)
						con.send("error".encode())
					else:
						con.send("success".encode())
				elif i.__class__ == Exception():
					print(i)
					con.send("error".encode())
				else:
					con.send("falled".encode())
			else:
				e = db_E.getEntriescheck(acc.Nick)

				if e.__class__ == Exception():
					print(e)
					con.send("error".encode())
				elif e == None:
					con.send("falled".encode())
				else:
					e.DataOut = datetime.strptime(stringone[5], '%Y/%m/%d %H:%M:%S')
					load = db_E.updateEntries(id=e.IdIng, ing=e)

					if load.__class__ == Exception():
						print(e)
						con.send("error".encode())
					elif load == None:
						con.send("falled".encode())
					else:
						con.send("success".encode())
		else:
			con.send("falled".encode())
