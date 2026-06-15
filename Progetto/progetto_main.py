from fastapi import FastAPI 

# Importo il resto del progetto
from .progetto_prodotti import router as prodotti_router
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
