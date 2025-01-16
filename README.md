# Brief

## Application conversationnelle avec traduction et analyse de sentiment

### Énoncé :

Créez une application conversationnelle qui permet à l'utilisateur de dialoguer avec un chatbot. Pour chaque message de l'utilisateur et chaque réponse du chatbot, l'application doit :
- Afficher le message original.
- Afficher la traduction anglaise du message.
- Afficher le sentiment exprimé dans le message (positif, négatif, neutre).

Détails :
- Utilisez un modèle de chatbot pré-entraîné de Hugging Face (ex: microsoft/DialoGPT-medium).
- Utilisez un modèle de traduction pré-entraîné de Hugging Face (ex: Helsinki-NLP/opus-mt-fr-en).
- Utilisez un modèle d'analyse de sentiment pré-entraîné de Hugging Face (ex: nlptown/bert-base-multilingual-uncased-sentiment).

Description détaillée :
- L'utilisateur pourra dialoguer avec un chatbot via une interface Gradio. Pour chaque message de l'utilisateur et chaque réponse du chatbot, l'application affichera le message original, sa traduction anglaise et le sentiment exprimé (positif, négatif, neutre). L'analyse de sentiment et la traduction seront effectuées en temps réel grâce aux modèles Hugging Face.

Bibliothèques :
- transformers
- gradio

### Calendrier :

Jour 1 :
- Configuration de l'environnement et installation des bibliothèques.
- Chargement et test du modèle de chatbot.
- Implémentation de la conversation de base avec le chatbot.

Jour 2 :
- Chargement et test des modèles de traduction et d'analyse de sentiment.
- Intégration de la traduction et de l'analyse de sentiment pour chaque message.

Jour 3 :
- Création de l'interface utilisateur avec Gradio.
- Affichage des messages, traductions et sentiments dans l'interface.
- Écriture de tests unitaires et du fichier README.md.

## Installation

**Create Virtual environnement**

`python -m venv .venv`

**Connect to the venv**

- mac/linux
  `source .venv/bin/activate.fish`
- windows
  `.venv/Scripts/activate` or `.venv/Scripts/activate.ps1`
- bash(windows)
`source .venv/Scripts/activate`

**Install the librairies**

`python.exe -m pip install --upgrade pip`

`pip install -r requirements.txt`

## Exécution

SOON

--- Mathieu ---

### **Fonctionnalité de Traduction**
Cette partie de l'application gère la traduction des messages de **anglais** vers **français** en utilisant le modèle pré-entraîné **Helsinki-NLP/opus-mt-en-fr** de Hugging Face.

#### **Description**
- Le fichier `translate.py` implémente une fonction permettant de traduire un texte de l'anglais vers le français.
- Utilise les bibliothèques suivantes :
  - **transformers** : pour le modèle et le tokenizer.
  - **torch** : pour l'exécution des modèles.
  - **sentencepiece** : requis par le tokenizer.

---

#### **Structure du Code**
- **load_translation_model()** :
  - Charge le modèle et le tokenizer nécessaires pour la traduction.
  - Modèle utilisé : `Helsinki-NLP/opus-mt-en-fr`.

- **translate_text(text, tokenizer, model)** :
  - Prend un texte en entrée et retourne le texte traduit.
  - Utilise les étapes suivantes :
    1. Tokenisation du texte en entrée.
    2. Génération de la traduction.
    3. Décodage de la traduction.

---

#### **Exemple d'utilisation**
1. Charger le modèle et le tokenizer :
   ```python
   from translate import load_translation_model, translate_text

   tokenizer, model = load_translation_model()
   ```
2. Traduire un texte :
   ```python
   english_text = "Hello, how are you?"
   translated_text = translate_text(english_text, tokenizer, model)
   print(f"Texte original : {english_text}")
   print(f"Texte traduit : {translated_text}")
   ```

---

#### **Dépendances**
Assurez-vous d'installer les dépendances suivantes avant d'exécuter le script :
```bash
pip install transformers torch sentencepiece
```

---

#### **Tests Unitaires**
Des tests unitaires sont en cours de développement pour valider la robustesse de la fonctionnalité de traduction. Ils sont situés dans le dossier `tests/`.

Exemple de test unitaire (fichier `test_translate.py`) :
```python
from translate import load_translation_model, translate_text

def test_translate_simple():
    tokenizer, model = load_translation_model()
    assert translate_text("Bonjour", tokenizer, model) == "Hello"
```

---

#### **Emplacement**
Le fichier de traduction est situé dans :
```
components/models/translate/translate.py
```
