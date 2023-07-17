import hashlib
import sys
import secrets
sys.path.append('./BackEnd/Model/')
import accountDAO as db_A

#mmmm
def gkGenerator():
    #prende la lista di gk di ogni utente
    listGK = db_A.getAllAccountGK()
    #crea una gk univoca di 4 caratteri comprendente lettere e numeri in formato esadecimale
    gk = hashlib.sha1(secrets.token_hex(2).encode()).hexdigest()
    

    if gk not in listGK:
        return gk.strip()
