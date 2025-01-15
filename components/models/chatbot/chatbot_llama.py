from transformers import pipeline
import torch

def load_model():
    """
    Charge le modèle principal pour effectuer des tâches de génération de langage.
    """
    # Charger le modèle principal
    model_id = "meta-llama/Llama-3.2-3B-Instruct"

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map=device,
    )

    return model

def generate_response(message, model):
    """
    Génère une réponse à partir d'un message utilisateur en utilisant un modèle de langage pré-entraîné.
    """

    # Créer un prompt pour le modèle
    prompt = f"Respond to this message with a tone of annoyance but in a humorous way. Limit your reply to 100 characters: {message}"

    # Générer la réponse
    outputs = model(prompt, max_length=256, num_return_sequences=1, truncation=True)

    # Extraire la réponse après le prompt initial
    generated_text = outputs[0]["generated_text"]
    response = generated_text[len(prompt):].strip()

    print(generated_text)

    return response

if __name__ == "__main__":
    # Charger le modèle
    print("Chargement du modèle...")
    model = load_model()
    print("Modèle chargé :)")

    # Exemple d'utilisation
    message = "Bonjour, peux-tu te présenter ?"
    print("Chargement de la réponse...")
    response = generate_response(message, model)

    print(f"Message utilisateur : {message}")
    print(f"Réponse du chatbot : {response}")
