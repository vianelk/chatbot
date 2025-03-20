import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import asyncio
from typing import List
# Initialisation de FastAPI
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (* = tous les domaines)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)
load_dotenv()
# Chargement des variables d'environnement
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT") 
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
#print(AZURE_STORAGE_CONNECTION_STRING)

# Nom du conteneur (à remplacer par le tien)
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Initialisation du client Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@app.get("/")
def read_root():
    return {"message": "Serveur FastAPI sur le port 9000"}

@app.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    """
    Endpoint permettant d'uploader un fichier vers Azure Blob Storage.
    """
    try:
        for file in files:
            # Crée le client Blob pour chaque fichier
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)

            # Lecture du fichier et upload
            with file.file as data:
                blob_client.upload_blob(data, overwrite=True)

        return {"message": f"✅ {len(files)} fichier(s) uploadé(s) avec succès!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialiser le client Azure OpenAI Service
client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
    api_version="2024-05-01-preview",
)

# Fonction de streaming des tokens
async def generate_response(prompt: str):
    print(prompt)
    try:
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Vous êtes un(e) assistant(e) IA qui permet aux utilisateurs de trouver des informations. sois bref et conscit "
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        # Activation du mode streaming
        response = client.chat.completions.create(
            model=OPENAI_DEPLOYMENT_NAME,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=True  # ⚡ Active le streaming
        )

        # Lire les tokens au fur et à mesure
        for chunk in response:
            if chunk.choices:
                yield chunk.choices[0].delta.content  # Envoie chaque morceau au client
                await asyncio.sleep(0)  # Laisse FastAPI gérer l'async

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de chat avec streaming
@app.post("/openai/chat/")
async def chat_with_openai(prompt: str):
    print(prompt)
    return StreamingResponse(generate_response(prompt), media_type="text/plain")


@app.post("/test/")
def test(msg:str):
    print("okey")
    return { msg : "ok"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
