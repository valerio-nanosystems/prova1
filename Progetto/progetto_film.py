from fastapi import FastAPI, HTTPException, APIRouter
import sqlite3

router = APIRouter()

# FASE 2 / ESERCITAZIONE 2: Endpoint per la ricerca testuale parziale
@router.get("/film/cerca")
def cerca_film(keyword: str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Permette di leggere i risultati come dizionari Python
    cursor = conn.cursor()
    
    # Utilizziamo LIKE con i caratteri jolly % prima e dopo la stringa
    cursor.execute("SELECT * FROM film WHERE titolo LIKE ?", (f"%{keyword}%",))
    risultati = cursor.fetchall()
    conn.close()
    
    return risultati


# FASE 4 / ESERCITAZIONE 4: Endpoint di dettaglio per ID del singolo Film
@router.get("/film/{id_film}")
def dettaglio_film(id_film: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Cerchiamo la riga esatta corrispondente all'ID richiesto dall'URL
    cursor.execute("SELECT * FROM film WHERE id = ?", (id_film,))
    film = cursor.fetchone()
    conn.close()
    
    # Se il film cercato tramite ID non esiste nel database locale
    if film is None:
        raise HTTPException(status_code=404, detail="Film non trovato nel database locale.")
        
    return film