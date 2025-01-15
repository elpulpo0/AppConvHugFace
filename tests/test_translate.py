import sys
import os

# Ajouter dynamiquement la racine du projet au chemin de recherche
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from components.models.translate.translate import load_translation_model, translate_text

tokenizer, model = load_translation_model()

def clean_translation(text):
    """
    Nettoie la traduction générée pour éviter les erreurs liées à la ponctuation finale ou aux espaces inutiles.
    
    Args:
        text (str): Le texte traduit.

    Returns:
        str: Texte nettoyé.
    """
    return text.strip().rstrip(".")

def test_translate_simple():
    """
    Test de traduction d'un mot simple (Bonjour -> Hello).
    """
    french_text = "Bonjour"
    expected_translation = "Hello"
    actual_translation = clean_translation(translate_text(french_text, tokenizer, model))
    assert actual_translation == expected_translation, f"Expected: '{expected_translation}', but got: '{actual_translation}'"
    
def test_translate_sentence():
    """
    Test de traduction d'une phrase complète.
    """
    french_text = "Comment allez-vous ?"
    expected_translation = "How are you?"
    actual_translation = clean_translation(translate_text(french_text, tokenizer, model))
    assert actual_translation == expected_translation, f"Expected: '{expected_translation}', but got: '{actual_translation}'"