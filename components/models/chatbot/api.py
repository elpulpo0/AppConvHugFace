from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN_LLAMA = os.getenv("TOKEN_LLAMA")

# Définir une application FastAPI
app = FastAPI()

class MessageRequest(BaseModel):
    message: str

# Charger le modèle au démarrage de l'application
print("Chargement du modèle...")
model_id = "meta-llama/Llama-3.2-3B-Instruct"

# Détection de l'appareil disponible (MPS, CUDA, ou CPU)
if torch.backends.mps.is_available():
    device = 'mps'
elif torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

# Charger le tokenizer et le modèle
tokenizer = AutoTokenizer.from_pretrained(model_id, token=TOKEN_LLAMA)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    token=TOKEN_LLAMA
)

# Initialiser le pipeline avec le modèle et le tokenizer
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if device == "cuda" else -1
)

print("Modèle chargé avec succès.")

@app.post("/generate_response/")
def generate_response(request: MessageRequest):
    """
    Endpoint pour générer une réponse en fonction du message utilisateur.
    """
    try:
        # Créer un prompt structuré pour LLaMA
        prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>"
            "You are an AI assistant responding to messages in a tone of annoyance but with humor. Be concise and witty."
            "<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>"
            f"{request.message}"
            "<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>"
        )

        # Générer la réponse
        outputs = generator(prompt, max_length=256, num_return_sequences=1, truncation=True)

        # Extraire uniquement la réponse après le prompt initial
        generated_text = outputs[0]["generated_text"].split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()

        return {"message": request.message, "response": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
