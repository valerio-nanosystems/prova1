from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from .progetto_prodotti import router as prodotti_router

# Importo il resto del progetto
from .progetto_db import dbinit

# Inizializzo il DB
dbinit()

# Dichiaro FastAPI
app = FastAPI()
app.include_router(prodotti_router)

# Creo una chiamata base di benvenuto
@app.get("/")
def root():
    return {"messaggio": "Benvenuto!"}
