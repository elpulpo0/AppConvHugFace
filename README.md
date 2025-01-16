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

**Update pip**

`python.exe -m pip install --upgrade pip`

**Install Torch**

Choose the version that suit your environment.

**Install the other librairies**

`pip install -r requirements.txt`

## Exécution

- Rename .env_example to .env and add your Llama Token
- Run the API : `uvicorn components.models.chatbot.api:app --host 127.0.0.1 --port 8000`
- Run the app : `python app.py`

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

--- Chris ---

### **Fonctionnalité de chat**
Cette partie de l'application gère la génération de réponse à un message en utilisant le modèle pré-entraîné **Llama-3.2-3B-Instruct** de Meta via Hugging Face.

#### **Description**
- Le fichier `api.py` distribue une API qui implémente une fonction sur la route "/generate_response" permettant de générer une réponse à un texte en anglais.
- Utilise les bibliothèques suivantes :
  - **transformers** : pour le modèle et le tokenizer.
  - **torch** : pour l'exécution des modèles.
  - **fastapi** : pour l'API.

- Le fichier `chatbot.py` distribue implémente une fonction qui fait appel à l'API avec un message pour lequel on attend une réponse.
- Utilise la bibliothèques suivante :
  - **requests** : pour réaliser la requête à l'API.

---

#### **Structure du Code**
##### api.py
  - Charge les variables d'environnement, le modèle et le tokenizer.

- **generate_response** :
  - Prend un texte en entrée et génère une réponse.

##### chatbot.py
- **get_response_from_api** :
  - Envoie un texte dans une requête API.

---

#### **Exemple d'utilisation**
1. Charger le modèle et le tokenizer :
   ```python
   from translate import load_translation_model, translate_text

   tokenizer, model = load_translation_model()
   ```
2. Traduire un texte :
   ```python
   message = "Can you please intriduce yourself?"
   response = get_response_from_api(message)
   ```

---

#### **Tests Unitaires**
Des tests unitaires sont en cours de développement pour valider la robustesse de la fonctionnalité de génération. Ils sont situés dans le dossier `tests/`.

Exemple de test unitaire (fichier `test_chatbot.py`) :
```python
from components.models.chatbot.api import app

def mock_requests_post():
    return MockResponse({"message": json["message"], "response": "Je suis un chatbot sarcastique et drôle!"}, 200)
def test_get_response_from_api()
    response = get_response_from_api(message)
    assert response == "Je suis un chatbot sarcastique et drôle!"

```

---

#### **Emplacement**
Les fichiers `chatbot.py` et `api.py` sont situés dans :
```
components/models/chatbot/
```

### Analyse of feels

The bot mush have a comprehension of the feeling of the user. For this there will be 2 way with one working right now.

- [ ] **Dlsta :**
  Analyse the feelings in the text with a a multiple labels possible by text. We can have a list of 28 labels possible but right now there is a little probleme with the detection of feelings. There the list :

  - Amusement
  - Admiration
- [ ] **DistiBERT :**
  Analyse the emotion of the message of everyone and say it's good or bad. There will be only 3 category possible :

  - Positive
  - Neutral
  - Negative

## Annexes

### Database

- [Database of emotions from text]([https://huggingface.co/datasets/google-research-datasets/go_emotions](https://huggingface.co/datasets/google-research-datasets/go_emotions "https://huggingface.co/datasets/google-research-datasets/go_emotions")) ( en cours de programmation )
- [Model DistiBERT](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)