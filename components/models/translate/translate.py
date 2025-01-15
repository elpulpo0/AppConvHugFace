from transformers import MarianMTModel, MarianTokenizer

# Chargement du modèle et du tokenizer
def load_translation_model():
    model_name = "Helsinki-NLP/opus-mt-en-fr"  # Modèle pour traduire de l'anglais vers le français
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Fonction de traduction
def translate_text(text, tokenizer, model):
    """
    Traduit un texte de l'anglais vers le français.

    Args:
        text (str): Le texte en anglais à traduire.
        tokenizer: Le tokenizer associé au modèle MarianMT.
        model: Le modèle MarianMT pré-entraîné.

    Returns:
        str: Le texte traduit en français.
    """
    # Tokenisation
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    # Génération de la traduction
    outputs = model.generate(**inputs)
    # Décodage
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

if __name__ == "__main__":
    # Charger le modèle et le tokenizer
    tokenizer, model = load_translation_model()

    # Exemple de texte à traduire
    english_text = "Hello, how are you?"
    translated_text = translate_text(english_text, tokenizer, model)

    print(f"Texte original : {english_text}")
    print(f"Texte traduit : {translated_text}")