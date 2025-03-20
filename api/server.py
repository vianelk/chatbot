import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Initialisation de FastAPI
app = FastAPI()
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
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint permettant d'uploader un fichier vers Azure Blob Storage.
    """
    try:
        # Création du client blob
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)

        # Lecture du fichier et upload
        with file.file as data:
            blob_client.upload_blob(data, overwrite=True)  # overwrite=True pour écraser un fichier existant

        return {"message": f"✅ {file.filename} uploadé avec succès dans {CONTAINER_NAME}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialiser le client Azure OpenAI Service
client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
    api_version="2024-05-01-preview",
)

# Endpoint pour interagir avec Azure OpenAI
@app.post("/openai/chat/")
async def chat_with_openai(prompt: str):
    try:
        # Préparer l’invite de conversation
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Vous êtes un(e) assistant(e) IA qui permet aux utilisateurs de trouver des informations."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt  # Utiliser le prompt de l'utilisateur
                    }
                ]
            }
        ]

        # Générer l’achèvement
        completion = client.chat.completions.create(
            model=OPENAI_DEPLOYMENT_NAME,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        # Extraire le contenu de la réponse
        response_content = completion.choices[0].message.content

        return {"content": response_content}  # Retourner uniquement le contenu

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Lancement du serveur FastAPI avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
