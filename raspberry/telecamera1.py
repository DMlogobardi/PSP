import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import threading
import time
import socket
import motore

class CameraScanner:

    def __init__(self, camera_id):
        self.reciverHost= '172.16.12.14'
        self.reciverPort= 12345
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.primaScansione = True
        self.funzione = False
        self.ultimo_tempo_scansione = 0
        self.cap = cv2.VideoCapture(camera_id)
        # Imposta la risoluzione del frame a 640x480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):
        while True:
            _, frame = self.cap.read()
            # Avvia il thread di scansione QR solo se è trascorso almeno 5 secondi dall'ultima scansione
            if time.time() - self.ultimo_tempo_scansione >= 5:
                qr_thread = threading.Thread(target=self.scan_qr_code, args=(frame,))
                qr_thread.start()
                self.ultimo_tempo_scansione = time.time()

            cv2.imshow("QR Scanner", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def scan_qr_code(self, frame):
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            res= obj.data.decode("utf-8")
            print("QR Code trovato! Contenuto: ", res)
            print(f"""QR = {res} primaScansione = {self.primaScansione} funzione={'Ingresso' if self.primaScansione else 'Uscita'}""")
            if res == "INGRESSO" and self.primaScansione:
                self.funzione= True
                self.primaScansione=False
            elif res == "USCITA" and self.primaScansione:
                self.funzione= False
                self.primaScansione=False
            else:
                motore.start()
                try:
                    print("SOCKET")
                    self.sock.connect((self.reciverHost,self.reciverPort))
                    self.sock.send(res.encode())
                    self.sock.close()
                except Exception as e:
                    print("Socket rotta")
                    print(e)
            time.sleep(10)

if __name__ == "__main__":
    camera_id = 1
    scanner = CameraScanner(camera_id)
    scanner.start()
