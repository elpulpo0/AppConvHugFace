import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

# Ajouter dynamiquement la racine du projet au chemin de recherche
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from components.models.chatbot.api import app

client = TestClient(app)

@patch("components.models.chatbot.api.AutoTokenizer.from_pretrained")
@patch("components.models.chatbot.api.AutoModelForCausalLM.from_pretrained")
def test_generate_response(mock_model, mock_tokenizer):
    """
    Teste l'API pour vérifier que la réponse générée par le modèle est correcte.
    """
    # Configurer le mock pour qu'il retourne un objet factice
    mock_tokenizer.return_value = "mocked_tokenizer"
    mock_model.return_value.generate.return_value = ["Mocked response"]

    message = "Bonjour, peux-tu te présenter ?"
    payload = {"message": message}

    # Effectuer la requête POST
    response = client.post("/generate_response/", json=payload)

    # Vérifier le statut de la réponse
    assert response.status_code == 200

    # Vérifier que la réponse contient une clé 'response'
    response_json = response.json()
    assert "response" in response_json

    # Vérifier que la réponse n'est pas vide
    assert len(response_json["response"]) > 0
    assert response_json["response"] == "Mocked response"

def test_generate_response_invalid_data():
    """
    Teste l'API avec des données invalides.
    """
    payload = {"invalid_key": "Some message"}

    # Effectuer la requête POST avec des données invalides
    response = client.post("/generate_response/", json=payload)

    # Vérifier le statut de la réponse (attend un code 422 pour les données invalides)
    assert response.status_code == 422
