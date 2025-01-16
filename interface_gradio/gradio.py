import gradio as gr
from components.models.chatbot.chatbot import generate_chatbot_response
# from components.models.sentiment_analysis.sentiment_analysis import analyze_sentiment
from components.models.translate.translate import translate_text_to_en

# ============================
# = Partie "pipeline" Gradio =
# ============================
def conversation_pipeline(user_input, history):
    # 1) Récupération du dernier message utilisateur
    user_msg = user_input

    # 2) Appel au chatbot pour générer la réponse
    bot_msg = generate_chatbot_response(user_msg, history)

    # 3) Traduire le message utilisateur et le message bot
    user_msg_en = translate_text_to_en(user_msg)
    bot_msg_en = translate_text_to_en(bot_msg)

    # 4) Analyser le sentiment des deux messages
    # user_sentiment = analyze_sentiment(user_msg)
    # bot_sentiment = analyze_sentiment(bot_msg)

    # 5) Mise en forme des informations pour l'historique
    #    On stocke un tuple (user_side, bot_side) où :
    #      - user_side est un dict contenant {texte, traduction, sentiment}
    #      - bot_side est un dict contenant {texte, traduction, sentiment}

    user_side = {
        "original": user_msg,
        "english": user_msg_en,
        # "sentiment": user_sentiment
    }
    bot_side = {
        "original": bot_msg,
        "english": bot_msg_en,
        # "sentiment": bot_sentiment
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
      1) Le texte en français
      2) Le texte en anglais
      3) Le sentiment
    """
    messages = []
    for (user_side, bot_side) in history:
        # Bloc de l'utilisateur
        user_content = (
            f"{user_side['original']}\n\n"
            f"{user_side['english']}\n\n"
            f"Sentiment : {user_side['sentiment']}"
        )
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        # Bloc du chatbot
        bot_content = (
            f"{bot_side['original']}\n\n"
            f"{bot_side['english']}\n\n"
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
    gr.Markdown("# Chatbot avec traduction FR/EN et analyse de sentiment")
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