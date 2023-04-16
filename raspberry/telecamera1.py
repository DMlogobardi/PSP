import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import threading
import time

class CameraScanner:

    def __init__(self, camera_id):
        self.primaScansione = True
        self.cap = cv2.VideoCapture(camera_id)
        # Imposta la risoluzione del frame a 640x480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):
        while True:
            _, frame = self.cap.read()
            # Avvia il thread di scansione QR
            qr_thread = threading.Thread(target=self.scan_qr_code, args=(frame,))
            qr_thread.start()

            cv2.imshow("QR Scanner", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def scan_qr_code(self, frame):
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            print("QR Code trovato! Contenuto: ", obj.data)
            
            if obj.data == "INGRESSO" and self.primaScansione:
                self.funzione= True
                self.primaScansione=False
            elif obj.data == "USCITA" and self.primaScansione:
                self.funzione= False
                self.primaScansione=False
            else:
                pass
                #SEND SOCKET

            time.sleep(10)

if __name__ == "__main__":
    camera_id = 1
    scanner = CameraScanner(camera_id)
    scanner.start()
