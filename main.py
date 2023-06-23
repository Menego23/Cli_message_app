import redis
import hashlib

r = redis.Redis(
  host='IlTuoHost',
  port=12114,
  password='LaTuaPassword')

def registrazione():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    # Verifica se l'utente esiste già
    if r.hget('utenti', username):
        print("L'utente esiste già.")
        return

    # Creazione del salt e hash della password
    salt = hashlib.sha256(username.encode()).hexdigest()
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Salva le informazioni dell'utente in Redis
    r.hset('utenti', username, hashed_password)
    r.hset('salt', username, salt)

    print("Registrazione completata con successo.")

def accesso():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    # Verifica se l'utente esiste
    if not r.hget('utenti', username):
        print("L'utente non esiste.")
        return

    # Verifica la password
    stored_password = r.hget('utenti', username).decode()
    salt = r.hget('salt', username).decode()
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    if hashed_password != stored_password:
        print("Password errata.")
        return

    print("Accesso effettuato.")

def invia_messaggio():
    username = input("Inserisci il nome utente: ")
    message = input("Inserisci il messaggio: ")

    # Genera un nuovo ID messaggio
    message_id = r.incr('message_id')

    # Salva il messaggio nella lista dei messaggi dell'utente
    r.lpush(f"messaggi:{username}", message)

    print("Messaggio inviato con successo.")
    print("ID messaggio:", message_id)

def elimina_account():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    # Verifica se l'utente esiste
    if not r.hget('utenti', username):
        print("L'utente non esiste.")
        return

    # Verifica la password
    stored_password = r.hget('utenti', username).decode()
    salt = r.hget('salt', username).decode()
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    if hashed_password != stored_password:
        print("Password errata.")
        return

    # Elimina l'account dell'utente
    r.hdel('utenti', username)
    r.hdel('salt', username)
    r.delete(f"messaggi:{username}")

    print("Account eliminato con successo.")

def visualizza_messaggi():
    username = input("Inserisci il nome utente: ")

    # Verifica se l'utente esiste
    if not r.hget('utenti', username):
        print("L'utente non esiste.")
        return

    # Ottieni tutti i messaggi dell'utente
    messaggi = r.lrange(f"messaggi:{username}", 0, -1)

    print(f"\nMessaggi di {username}:")
    for idx, messaggio in enumerate(messaggi, start=1):
        print(f"ID messaggio: {idx}")
        print(f"Messaggio: {messaggio.decode()}")
        print()

    print("Fine messaggi.")

def visualizza_utenti():
    # Recupera tutti gli utenti dal dizionario 'utenti' di Redis
    utenti = r.hkeys('utenti')
    
    print("\nElenco utenti registrati:")
    for utente in utenti:
        print(utente.decode())

# Menu principale
while True:
    print("\n=== Messaggistica CLI ===")
    print("1. Registrazione")
    print("2. Accesso")
    print("3. Invia messaggio")
    print("4. Elimina account")
    print("5. Visualizza messaggi")
    print("6. Visualizza utenti")
    print("0. Esci")

    scelta = input("\nSeleziona un'opzione: ")

    if scelta == "1":
        registrazione()
    elif scelta == "2":
        accesso()
    elif scelta == "3":
        invia_messaggio()
    elif scelta == "4":
        elimina_account()
    elif scelta == "5":
        visualizza_messaggi()
    elif scelta == "6":
        visualizza_utenti()
    elif scelta == "0":
        break
    else:
        print("Opzione non valida.")
