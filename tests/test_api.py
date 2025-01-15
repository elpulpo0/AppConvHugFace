import pytest
from fastapi.testclient import TestClient
from components.models.chatbot.api import app  # Assurez-vous que l'import correspond à votre fichier

client = TestClient(app)

def test_generate_response():
    """
    Teste l'API pour vérifier que la réponse générée par le modèle est correcte.
    """
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

def test_generate_response_invalid_data():
    """
    Teste l'API avec des données invalides.
    """
    payload = {"invalid_key": "Some message"}

    # Effectuer la requête POST avec des données invalides
    response = client.post("/generate_response/", json=payload)

    # Vérifier le statut de la réponse (attend un code 422 pour les données invalides)
    assert response.status_code == 422
