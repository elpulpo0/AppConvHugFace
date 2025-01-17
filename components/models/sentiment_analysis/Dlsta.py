from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

class Dlsta:
    def __init__(self, model_name="bert-base-uncased", num_labels=28, max_length=128):
        """
        Initialize the EmotionClassifier with a specific model and tokenizer.

        Args:
            model_name (str): Hugging Face model name (e.g., 'bert-base-uncased').
            num_labels (int): Number of emotion labels (default: 28 for GoEmotions).
            max_length (int): Maximum token length for input text.
        """
        self.model_name = model_name
        self.num_labels = num_labels
        self.max_length = max_length

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels)

    def load_data(self, dataset_name="go_emotions"):
        """
        Load the dataset from Hugging Face Datasets.

        Args:
            dataset_name (str): The name of the dataset to load.
        """
        self.dataset = load_dataset(dataset_name)

    def preprocess(self):
        """
        Tokenize the dataset and prepare it for training.
        """
        def preprocess_function(examples):
            return self.tokenizer(examples["text"], padding="max_length", truncation=True, max_length=self.max_length)
        
        self.encoded_dataset = self.dataset.map(preprocess_function, batched=True)
        self.train_dataset = self.encoded_dataset["train"]
        self.validation_dataset = self.encoded_dataset["validation"]
        self.test_dataset = self.encoded_dataset["test"]

    def compute_metrics(self, pred):
        """
        Compute accuracy for evaluation.

        Args:
            pred: Predictions from the Trainer.

        Returns:
            dict: Accuracy metric.
        """
        predictions = np.argmax(pred.predictions, axis=1)
        labels = pred.label_ids
        accuracy = accuracy_score(labels, predictions)
        return {"accuracy": accuracy}

    def train(self, output_dir="./results", learning_rate=2e-5, batch_size=16, num_epochs=3):
        """
        Train the model using Hugging Face's Trainer.

        Args:
            output_dir (str): Directory to save training results.
            learning_rate (float): Learning rate for optimization.
            batch_size (int): Batch size for training and evaluation.
            num_epochs (int): Number of training epochs.
        """
        training_args = TrainingArguments(
            output_dir="./my_results",
            num_train_epochs=5,
            per_device_train_batch_size=32,
            per_device_eval_batch_size=64,
            warmup_steps=1000,
            weight_decay=0.02,
            learning_rate=3e-5
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.validation_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics,
        )

        self.trainer.train()

    def evaluate(self):
        """
        Evaluate the model on the test dataset.

        Returns:
            dict: Evaluation results.
        """
        results = self.trainer.evaluate(self.test_dataset)
        print("Evaluation Results:", results)

        predictions = self.trainer.predict(self.test_dataset)
        pred_labels = np.argmax(predictions.predictions, axis=1)
        true_labels = self.test_dataset["labels"]
        report = classification_report(true_labels, pred_labels, target_names=self.dataset["train"].features["labels"].names)
        print("\nClassification Report:\n", report)

    def predict(self, text):
        """
        Predict the emotion of a given text.

        Args:
            text (str): The input text.

        Returns:
            str: The predicted emotion.
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length)
        outputs = self.model(**inputs)
        predicted_label = np.argmax(outputs.logits.detach().numpy())
        emotion = self.dataset["train"].features["labels"].names[predicted_label]
        return emotion