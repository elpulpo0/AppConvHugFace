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
