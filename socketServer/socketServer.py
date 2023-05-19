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
	try:
		stringone  = con.recv(312).decode().strip().split("!")
		print(stringone)
		id = int(stringone[2])
		acc = db_A.getAccountById(id)
		if acc != None:
			if stringone[4].strip() == acc.gK:
				if stringone[1] == "i":
					i = db_E.getEntriescheck(nick= acc.nick)
					if i == None:
						data_in = datetime.strptime(stringone[5], "%Y/%m/%d %H:%M:%S")
						ing = db.Entries(dataIn= data_in, idAccount=acc.idAccount)
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
					e = db_E.getEntriescheck(acc.nick)

					if e.__class__ == Exception():
						print(e)
						con.send("error".encode())
					elif e == None:
						con.send("falled".encode())
					else:
						e.dataOut = datetime.strptime(stringone[5], '%Y/%m/%d %H:%M:%S')
						load = db_E.updateEntries(id=e.idIng, ing=e)

						if load.__class__ == Exception():
							print(e)
							con.send("error".encode())
						elif load == None:
							con.send("falled".encode())
						else:
							con.send("success".encode())
			else:
				con.send("falled".encode())
	except Exception as e:
		print(e)
		con.send("falled".encode())