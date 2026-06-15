from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

# Avere una costante per i dati fissi usati nel codice è sempre una buona idea
DB_PATH = "database.db"

# Inizializzazione del database (eseguita una volta all'avvio)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prodotti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                prezzo REAL
            )
        """)
        # Popolo con dati di esempio solo se la tabella è vuota
        e_vuoto = conn.execute("SELECT 1 FROM prodotti LIMIT 1").fetchone() is None
        if e_vuoto:
            dati_esempio = [
                ("Mouse Wireless", 25.50),
                ("Tastiera Meccanica", 89.90),
                ("Monitor 24 Pollici", 149.00),
                ("Cuffie Gaming", 45.00),
                ("Tappetino XL", 15.00),
            ]
            conn.executemany(
                "INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", dati_esempio
            )
        conn.commit()
    finally:
        conn.close()

# Eseguo l'inizializzazione
init_db()

# Dependency per la connessione: apre, fornisce, e chiude sempre
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # le righe diventano dict-like
    try:
        yield conn
    finally:
        conn.close()  # eseguito sempre, anche se l'endpoint solleva un'eccezione

# Definisco i modelli Pydantic 
class ProdottoIn(BaseModel):
    nome: str
    prezzo: float

class ProdottoOut(ProdottoIn):
    id: int

app = FastAPI()

@app.get("/")
def root():
    return {"messaggio": "Benvenuto!"}

@app.get("/prodotti", response_model=list[ProdottoOut])
def leggi_prodotti(conn: sqlite3.Connection = Depends(get_db)):
    righe = conn.execute("SELECT * FROM prodotti").fetchall()
    return [dict(r) for r in righe]

@app.get("/prodotti/{id_prodotto}", response_model=ProdottoOut)
def leggi_prodotto_singolo(
    id_prodotto: int, conn: sqlite3.Connection = Depends(get_db)
):
    riga = conn.execute(
        "SELECT * FROM prodotti WHERE id = ?", (id_prodotto,)
    ).fetchone()
    if riga is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    return dict(riga)

@app.post("/prodotti", response_model=ProdottoOut, status_code=201)
def crea_prodotto(dati: ProdottoIn, conn: sqlite3.Connection = Depends(get_db)):
    cur = conn.execute(
        "INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)",
        (dati.nome, dati.prezzo),
    )
    conn.commit()
    return {"id": cur.lastrowid, "nome": dati.nome, "prezzo": dati.prezzo}

@app.put("/prodotti/{id_prodotto}", response_model=ProdottoOut)
def aggiorna_prodotto(
    id_prodotto: int,
    dati: ProdottoIn,
    conn: sqlite3.Connection = Depends(get_db),
):
    esiste = conn.execute(
        "SELECT 1 FROM prodotti WHERE id = ?", (id_prodotto,)
    ).fetchone()
    if esiste is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    conn.execute(
        "UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?",
        (dati.nome, dati.prezzo, id_prodotto),
    )
    conn.commit()
    return {"id": id_prodotto, "nome": dati.nome, "prezzo": dati.prezzo}

@app.delete("/prodotti/{id_prodotto}")
def elimina_prodotto(
    id_prodotto: int, conn: sqlite3.Connection = Depends(get_db)
):
    esiste = conn.execute(
        "SELECT 1 FROM prodotti WHERE id = ?", (id_prodotto,)
    ).fetchone()
    if esiste is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    conn.execute("DELETE FROM prodotti WHERE id = ?", (id_prodotto,))
    conn.commit()
    return {"status": "Cancellato"}