import os  
import base64
from openai import AzureOpenAI  

endpoint = os.getenv("ENDPOINT_URL", "https://trainingopenaiestiamvk.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4")  
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://aisearchforcwyod.search.windows.net")  
search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")  
search_index = os.getenv("SEARCH_INDEX_NAME", "businessdata-index")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  

# Initialiser le client Azure OpenAI Service avec une authentification basée sur une clé    
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)
  
    
# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

#Préparer l’invite de conversation 
chat_prompt = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "est ce t'as accès au facture"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Les informations demandées ne sont pas trouvées dans les données récupérées. Veuillez essayer une autre requête ou sujet."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "dis moi je totales des factures d'eau du mois de mars"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Voici les totaux des factures d'eau pour le mois de mars 2025 pour le client Voto Paris fournies par Veolia :\n\n- Facture EAU-004 : 276.16 EUR [doc1]\n- Facture EAU-003 : 496.58 EUR [doc2]\n- Facture EAU-010 : 397.95 EUR [doc3]\n- Facture EAU-007 : 340.98 EUR [doc4]\n- Facture EAU-006 : 320.35 EUR [doc5]\n\nLe total combiné des factures d'eau pour le mois de mars 2025 est donc 1,832.02 EUR."
            }
        ]
    }
] 
    
# Inclure le résultat de la voix si la voix est activée  
messages = chat_prompt  
    
# Générer l’achèvement  
completion = client.chat.completions.create(  
    model=deployment,
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False,
    extra_body={
      "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": "businessdata-index",
            "semantic_configuration": "semsearchconf",
            "query_type": "semantic",
            "fields_mapping": {
              "content_fields_separator": "\n",
              "content_fields": [
                "content"
              ],
              "filepath_field": "metadata_storage_path",
              "title_field": None,
              "url_field": None,
              "vector_fields": []
            },
            "in_scope": True,
            "role_information": "",
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            }
          }
        }]
    }
)

print(completion.to_json())