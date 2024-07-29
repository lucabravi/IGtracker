# IGtracker

Questo progetto Python utilizza l'API di Ensta per raccogliere dati sugli account e sui post di un profilo specifico e salva questi dati in un database MariaDB utilizzando SQLAlchemy. Il programma è configurato per aggiornare i dati ogni 10 minuti, mantenendo uno storico completo delle variazioni.

## Requisiti

- Python >= 3.6 and < 3.12
- MariaDB
- Moduli Python: ensta, SQLAlchemy, PyMySQL


## Installazione

1. Clona il repository:

    ```sh
    git clone https://github.com/lucabravi/IGtracker.git
    cd IGtracker
    ```

2. Crea e attiva un ambiente virtuale (opzionale ma consigliato):

    ```sh
    python -m venv venv
    source venv/bin/activate  # Su Windows usa `venv\Scripts\activate`
    ```

3. Installa le dipendenze:

    ```sh
    pip install -r requirements.txt
    ```


## Configurazione

Copia il file .env.example rinominandolo in .env

```sh
cp .env.example .env
```

e modifica il contenuto con le credenziali del tuo database MariaDB per permettere la corretta connessione allo stesso


## Esecuzione

Esegui lo script, seguito dalla lista di utenti da monitorare, per raccogliere e salvare i dati su database:

```sh
python main.py username1 username2 username3 ...
```

Lo script non rimarrà automaticamente in esecuzione, è stato pensato per essere eseguito tramite schedulazione tramite cron (su Linux) o Utilità di Pianificazione (su Windows).


## Struttura del Database

Il database è composto da quattro tabelle principali:

accounts: Contiene i dati anagrafici degli account.
account_history: Contiene lo storico delle variazioni degli account.
posts: Contiene i dati anagrafici dei post.
post_history: Contiene lo storico delle variazioni dei post.


## Esempio di Utilizzo

Lo script raccoglierà i seguenti dati

Per ogni account:

- Conto dei follower
- Conto dei following
- Conto totale dei post

Per ogni post dei suddetti account:

- ID del post
- Tipo di media
- Data di pubblicazione
- Conto dei commenti
- Conto dei like




