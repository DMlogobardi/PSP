import sys
import secrets
sys.path.append('./BackEnd/Model/')
import accountDAO as db_A

def gkGenerator():
    #prende la lista di gk di ogni utente
    listGK = db_A.getAllAccountGK()
    #crea una gk univoca di 4 caratteri comprendente lettere e numeri in formato esadecimale
    gk = secrets.token_hex(2)

    for GK in listGK:
        if gk != GK:
            return gk.strip()