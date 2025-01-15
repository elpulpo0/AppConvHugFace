import requests

def get_response_from_api(message: str) -> str:
    """
    Appelle l'API pour obtenir la réponse générée par le modèle pour le message fourni.
    """
    url = "http://127.0.0.1:8000/generate_response/"
    payload = {"message": message}

    try:
        # Effectuer la requête POST vers l'API
        response = requests.post(url, json=payload)

        # Vérifier si la requête a réussi
        response.raise_for_status()

        # Récupérer la réponse JSON
        response_json = response.json()

        # Extraire la réponse générée
        return response_json.get("response", "Pas de réponse générée.")

    except requests.exceptions.RequestException as e:
        # Gérer les erreurs de requête (connexion, timeout, etc.)
        print(f"Erreur lors de la requête à l'API : {e}")
        response_json = response.json()
        return response_json.get("detail")

if __name__ == "__main__":
    # Exemple d'utilisation
    message = "Can you please intriduce yourself?"
    response = get_response_from_api(message)

    print(f"Message utilisateur : {message}")
    print(f"Réponse du chatbot : {response}")