from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import tensorflow as tf


class Dlsta:
    def __init__(self):
        self.model = None

    ############################################################################
    ############################# Train the model ##############################
    ############################################################################
    def train_model(self, sequences, y):

        x = pad_sequences(sequences, padding="post")
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.99, random_state=42)
        print(len(x_train))
        
        x_train = np.array(x_train)
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=30000, output_dim=256),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
            tf.keras.layers.GlobalMaxPooling1D(),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(28, activation="sigmoid")  # Utilisation de sigmoid pour classification multi-étiquettes
        ])
        
        self.model.compile(
            loss="binary_crossentropy",  # Pour classification multi-étiquettes
            optimizer="adam",
            metrics=["accuracy"]
        )

        self.model.fit(x_train, y_train, epochs=5, batch_size=28)
        self.model.summary()
        return x_test,y_test

    ############################################################################
    ############################# Test the model ##############################
    ############################################################################
    def test_model(self, y_test, x_test):
        x_test = pad_sequences(x_test, padding="post")
        return self.model.evaluate(x_test, y_test)

    ############################################################################
    ############################ Predict the result ############################
    ############################################################################
    def predict(self, x_text):
        x_text = pad_sequences(x_text, padding="post")
        return self.model.predict(x_text)

    ############################################################################
    ############################ Analyze the texts  ############################
    ############################################################################
    def analyze_texts(self, x, labels):
        predict = self.predict(x)
        print(f"Émotion prédite : {labels[predict]}\n")


    ############################################################################
    ############################## Save bot ####################################
    ############################################################################
    def accuracy(self,y_predict,y_test):
        print(f"La précision sur le jeu de test : {accuracy_score(y_test,y_predict) * 100:.2f}%")
    
    ############################################################################
    ############################## Save bot ####################################
    ############################################################################
    def save_model(self):
        self.model.save("./components/models/sentiment_analysis/dlsta_model")

    def load_model(self):
        self.model = tf.keras.models.load_model("./components/models/sentiment_analysis/dlsta_model")