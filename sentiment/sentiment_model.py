import torch
from transformers import BertTokenizer, BertModel
import torch.nn as nn
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import os
# Function to check if NLTK resource is downloaded
def download_nltk_resource(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split('/')[-1])

# Check and download necessary NLTK resources
nltk_resources = ['tokenizers/punkt', 'corpora/stopwords', 'corpora/wordnet', 'corpora/omw-1.4']
for resource in nltk_resources:
    download_nltk_resource(resource)

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Tokenize text
    words = word_tokenize(text)

    # Remove punctuation
    words = [word for word in words if word.isalnum()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize words
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join words back into a single string
    return ' '.join(words)

class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        pooled_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )['pooler_output']
        output = self.drop(pooled_output)
        return self.out(output)

# Load the tokenizer from the local directory
tokenizer = BertTokenizer.from_pretrained('sentiment/model/tokenizer')
model = SentimentClassifier(n_classes=3)
model.load_state_dict(torch.load('sentiment/model/news_sentiment_model.pth', map_location=torch.device('cpu')))
model.eval()

def predict_sentiment(text):
    processed_text = preprocess_text(text)
    encoding = tokenizer(
        processed_text,
        max_length=512,
        truncation=True,
        padding='max_length',
        add_special_tokens=True,
        return_tensors='pt'
    )

    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        _, prediction = torch.max(outputs, dim=1)
        sentiment = prediction[0].item()
    return sentiment