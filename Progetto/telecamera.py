import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from threading import Thread
import time
from socket import AF_INET, SOCK_STREAM, socket
from datetime import datetime, date
import secrets
import motore

class CameraScanner:


	def __init__(self, camera_id):
		self.reciverHost = '172.16.22.39'
		self.reciverPort = 12346
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.primaScansione = True
		self.funzione = ""
		self.ultimo_tempo_scansione = 0
		self.sock.connect((self.reciverHost, self.reciverPort))
		self.cap = cv2.VideoCapture(camera_id)
		# Imposta la risoluzione del frame a 640x480
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	def start(self):
		while True:
			_, frame = self.cap.read()
			# Avvia il thread di scansione QR solo se è trascorso almeno 5 secondi dall'ultima scansione
			if time.time() - self.ultimo_tempo_scansione >= 5:
				qr_thread = Thread(target=self.scan_qr_code, args=(frame,))
				qr_thread.start()
				self.ultimo_tempo_scansione = time.time()
			cv2.imshow("QR Scanner", frame)

			key = cv2.waitKey(1) & 0xFF

			if key == ord('q'):
				break

		self.cap.release()
		cv2.destroyAllWindows()

	def ingresso(self, res):
		listResult = res.split("!")
		#data TERZO CAMP
		data = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		gen1 = secrets.token_hex(2)
		listToSent = f"""{gen1}!i!{listResult[1]}!{listResult[2]}!{listResult[3]}!{data}!{listResult[5]}""".strip()
		return listToSent

	def uscita(self,res):
		listResult = res.split("!")
		print(f"LIST RESULT {listResult}")
		#data TERZO CAMP
		data = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		gen1 = secrets.token_hex(2)
		listToSent = f"""{gen1}!u!{listResult[1]}!{listResult[2]}!{listResult[3]}!{data}!{listResult[5]}""".strip()
		print(f"\n\n\n STRINGONE DA INVIARE = {listToSent}")
		return listToSent

	def sendFunction(self, stringa=""):
		self.sock.send(stringa.encode())
		print("INVIO EFFETTUATO")
		data = self.sock.recv(1024).decode()
		if data == "success":
			print("Inserimento riuscito, Buona giornata")
			motore.start()

	def isValidData(self,data_stringa = "23/05/17 09:30:00"):
		return True
		# Conversione della stringa in un oggetto datetime
		data = datetime.strptime(data_stringa, "%Y/%m/%d %H:%M:%S")
		# Calcolo dell'orario attuale
		orario_attuale = datetime.now()
		differenza_minuti = (orario_attuale - data).total_seconds() / 60
		# Verifica se sono trascorsi meno di 15 minuti e se la data è già passata
		if differenza_minuti < 15 and differenza_minuti > 0:
			return True
		else:
			return False
						
	def scan_qr_code(self, frame):
		decodedObjects = pyzbar.decode(frame)
		strRis = ""
		for obj in decodedObjects:
			res= obj.data.decode("utf-8")
			print("QR Code trovato! Contenuto: ", res)
			try :
				listResult = res.split("!")
				if (self.primaScansione == True ) and (res == "INGRESSO"):
					print("TELECAMERA IMPOSTATA COME INGRESSO")
					self.funzione = "INGRESSO"
					self.primaScansione = False
				elif (self.primaScansione == True ) and (res == "USCITA"):
					print("TELECAMERA IMPOSTATA USCITA")
					self.funzione = "USCITA"
					self.primaScansione = False
				elif (self.primaScansione == True):
					print("IMPOSTARE LA FUNZIONE TRAMITE QR")
		
				elif (self.primaScansione == False ) and (self.funzione == "INGRESSO"):
					strRis = self.ingresso(res)
					print(f"strRis = {strRis}")
				elif (self.primaScansione == False ) and (self.funzione == "USCITA"):
					strRis = self.uscita(res)
				
				if (self.primaScansione == False):
					if (int(listResult[1]) > 0):
						print(listResult[4])
						if (self.isValidData(listResult[4])):
							print(f"Invio della stringa: {strRis}")
							self.sendFunction(strRis)
					else:
						print("QR NON Valido")
			except :
				pass
			
			time.sleep(5)

if __name__ == "__main__":
	camera_id = 0
	scanner = CameraScanner(camera_id)
	scanner.start()

