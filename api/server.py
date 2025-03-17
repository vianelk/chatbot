from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modèle de données pour la requête POST
class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
def read_root():
    return {"message": "Serveur Python sur le port 9000"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item créé avec succès", "item": item}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
