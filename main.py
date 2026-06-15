from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"messaggio": "funziona!"}

@app.get("/somma/{n1}/{n2}")
def somma(n1, n2):
    return int(n1) + int(n2)

@app.get("/somma2/{n1}/{n2}")
def somma(n1: int, n2: int):
    return n1 + n2

@app.get("/calcola")
def somma(n1: int, n2: int, op: str):
    match op:
        case "somma" | "+":
            return {"risultato": n1 + n2}
        case "sottrazione" | "-":
            return {"risultato": n1 - n2}
        case "moltiplicazione" | "*":
            return {"risultato": n1 * n2}
        case "divisione" | "/":
            if n2 == 0:
                raise HTTPException(status_code=400, detail="Impossibile dividere per zero")
            return {"risultato": n1 / n2}
        case _:
            # Questo corrisponde al "default" dello switch-case
            raise HTTPException(status_code=400, detail="Operazione non valida")

prodotti = [
    {"id": 1, "nome": "Tastiera Meccanica", "prezzo": 89.99},
    {"id": 2, "nome": "Mouse Wireless", "prezzo": 45.50},
    {"id": 3, "nome": "Monitor 4K", "prezzo": 349.00}
]

@app.get("/prodotto/{id_cercato}")
def ottieni_prodotto(id_cercato: int):
    for prodotto in prodotti:
        if prodotto["id"] == id_cercato:
            return prodotto
            
    raise HTTPException(status_code=404, detail="Prodotto non trovato")

#miopro = ProdottoIn("asd", 1)

class ProdottoIn(BaseModel):
    nome: str
    prezzo: float

#mioprodotto = ProdottoIn("shampo", 1.20)

@app.get("/prodotti")
def lista_prodotti():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@app.post("/prodotti", status_code=201)
def crea_prodotto(dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", (dati.nome, dati.prezzo))
    conn.commit()
    conn.close()
    return {"status": "Prodotto registrato con successo"}

@app.put("/prodotto/{id_prodotto}")
def aggiorna_prodotto(id_prodotto: int, dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?", (dati.nome, dati.prezzo, id_prodotto))
    conn.commit()
    conn.close()
    return {"status": "Modifica salvata"}

@app.delete("/prodotto/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM prodotti WHERE id=?",
        (id_prodotto,)
    )
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}