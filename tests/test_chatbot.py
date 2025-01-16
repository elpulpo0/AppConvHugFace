import requests
from unittest.mock import patch
from components.models.chatbot.chatbot import get_response_from_api

# Mock de la fonction de l'API
def mock_requests_post(url, json):
    class MockResponse:
        def __init__(self, response_data, status_code):
            self.status_code = status_code
            self.json_data = response_data

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            if not (200 <= self.status_code < 300):
                raise requests.exceptions.HTTPError(f"HTTP {self.status_code} Error")

    if url == "http://127.0.0.1:8000/generate_response/":
        return MockResponse({"message": json["message"], "response": "Je suis un chatbot sarcastique et drôle!"}, 200)
    return MockResponse({}, 404)

# Test de la fonction avec patch appliqué à requests.post
@patch('requests.post', side_effect=mock_requests_post)
def test_get_response_from_api(mock_post):
    """
    Teste la fonction get_response_from_api pour vérifier que la réponse est générée correctement.
    """
    message = "Bonjour, peux-tu te présenter ?"

    # Appeler la fonction pour obtenir la réponse
    response = get_response_from_api(message)

    # Vérifier la réponse générée
    assert response == "Je suis un chatbot sarcastique et drôle!"
