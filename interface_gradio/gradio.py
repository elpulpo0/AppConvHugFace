import gradio as gr
from components.models.chatbot.chatbot import get_response_from_api
from components.models.translate.translate import load_translation_model, translate_text
from components.models.sentiment_analysis.DistiBERT import DistiBERT

# ============================
# = Partie "pipeline" Gradio =
# ============================
def conversation_pipeline(user_input, history):
    analyzer_feel = DistiBERT()
    # 1) Récupération du dernier message utilisateur
    user_msg = user_input

    # 2) Appel au chatbot pour générer la réponse
    bot_msg = get_response_from_api(user_msg)

    # 3) Traduire le message utilisateur et le message bot
    load_translate = load_translation_model()
    user_msg_en = translate_text(user_msg, load_translate[0], load_translate[1])
    bot_msg_en = translate_text(bot_msg, load_translate[0], load_translate[1])

    # # 4) Analyser le sentiment des deux messages
    result = analyzer_feel.analyze([user_msg_en])
    user_sentiment = analyzer_feel.result(results=result,texts=[user_msg])
    result = analyzer_feel.analyze([bot_msg_en])
    bot_sentiment = analyzer_feel.result(texts=[bot_msg],results=result)

    # 5) Mise en forme des informations pour l'historique
    #    On stocke un tuple (user_side, bot_side) où :
    #      - user_side est un dict contenant {texte, traduction, sentiment}
    #      - bot_side est un dict contenant {texte, traduction, sentiment}

    user_side = {
        "original": user_msg,
        "french": user_msg_en,
        "sentiment": user_sentiment
    }
    bot_side = {
        "original": bot_msg,
        "french": bot_msg_en,
        "sentiment": bot_sentiment
    }

    # 6) On met à jour l'historique
    #    Pour Gradio, on retourne l'historique mis à jour ET
    #    le texte “brut” du bot (si on veut l'afficher).
    #    Mais on va gérer l'affichage personnalisé via un custom component.
    history = history + [(user_side, bot_side)]
    return history, bot_msg

def format_conversation_display_as_messages(history):
    """
    Convertit l'historique en une liste de dicts:
      [{"role": "user"|"assistant", "content": "..."}]
    
    On veut trois lignes, séparées par des retours à la ligne :
      1) Le texte en anglais
      2) Le texte en français 
      3) Le sentiment
    """
    messages = []
    for (user_side, bot_side) in history:
        # Bloc de l'utilisateur
        user_content = (
            f"{user_side['original']}\n\n"
            f"{user_side['french']}\n\n"
            f"Sentiment : {user_side['sentiment']}"
        )
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        # Bloc du chatbot
        bot_content = (
            f"{bot_side['original']}\n\n"
            f"{bot_side['french']}\n\n"
            f"Sentiment : {bot_side['sentiment']}"
        )
        messages.append({
            "role": "assistant",
            "content": bot_content
        })
    return messages

def on_user_submit(user_msg, history):
    new_history, bot_msg = conversation_pipeline(user_msg, history)
    messages = format_conversation_display_as_messages(new_history)
    return new_history, messages

# ---------------------------------------
# Ajout d'un CSS personnalisé
# ---------------------------------------
MY_CUSTOM_CSS = """
.user.message .message-content {
    background-color: #6C2BD9 !important; /* violet flash */
    color: white !important;
}

.bot.message .message-content {
    background-color: #34C759 !important; /* vert */
    color: white !important;
}
"""

with gr.Blocks(css=MY_CUSTOM_CSS) as conv:
    gr.Markdown("# Chatbot avec traduction EN/FR et analyse de sentiment")
    conversation_state = gr.State([])

    # Composant Chatbot en mode "messages"
    conversation_display = gr.Chatbot(
        label="Historique de la conversation",
        type="messages"
    )
    
    user_input = gr.Textbox(label="Votre message")

    send_button = gr.Button("Envoyer")

    send_button.click(
        fn=on_user_submit,
        inputs=[user_input, conversation_state],
        outputs=[conversation_state, conversation_display]
    )

    user_input.submit(
        fn=on_user_submit,
        inputs=[user_input, conversation_state],
        outputs=[conversation_state, conversation_display]
    )