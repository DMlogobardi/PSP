import socket
from datetime import datetime
import hashlib
import sys
sys.path.append('./BackEnd/Model/')
sys.path.append('./BackEnd/DB/')
import dbSession as db
import accountDAO as db_A
import entriesDAO as db_E

HOST = 'localhost'
PORT = 12345

s = socket.socket()		
print(f'TCP Server Listening on {HOST}:{PORT}..')

s.bind((HOST, PORT))
s.listen(1)

while True:
	con, addr = s.accept()
	stringone  = con.recv(312).decode().strip().split("!")
	print(f"""Stringone:{stringone}""")

	acc = db_A.getAccountById(int(stringone[2]))
	if acc != None:
		if stringone[4].strip() == hashlib.sha1(acc.GK.encode()).hexdigest():
			if stringone[1] == "i":
				i = db_E.getEntriescheck(acc.Nick)
				if i == None:
					print(stringone[5])
					ing = db.Entries(DataIn=datetime.strptime(stringone[5], '%y/%m/%d %H:%M:%S'), IdAccount=acc.IdAccount)
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
					e.setDataOut(datetime.strptime(stringone[5], '%y/%m/%d %H:%M:%S.%f'))
					load = db_E.updateEntries(e.IdIng, e)

					if load.__class__ == Exception():
						print(e)
						con.send("error".encode())
					elif load == None:
						con.send("falled".encode())
					else:
						con.send("success".encode())
		else:
			con.send("falled".encode())
