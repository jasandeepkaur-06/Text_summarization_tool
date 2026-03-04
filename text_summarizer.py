# Import necessary libraries
import nltk
import string
import heapq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Import HuggingFace transformer model (T5)
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load pretrained T5 model and tokenizer
# This loads only once when server starts
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# EXTRACTIVE SUMMARIZATION

def extractive_summary(text, limit_sentences=5):
    """
    This function performs extractive summarization.
    It selects the most important sentences based on word frequency.
    """

    # Get English stopwords (common words like is, the, and)
    stop_words = set(stopwords.words("english"))

    # Tokenize text into words
    words = word_tokenize(text)

    # Dictionary to store frequency of important words
    word_frequencies = {}

    for word in words:
        # Ignore stopwords and punctuation
        if word.lower() not in stop_words and word.lower() not in string.punctuation:
            word_frequencies[word.lower()] = word_frequencies.get(word.lower(), 0) + 1

    # Split text into sentences
    sentences = sent_tokenize(text)

    # Score each sentence based on word frequency
    sentence_scores = {}

    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    # Select top 'limit_sentences' important sentences
    summary_sentences = heapq.nlargest(limit_sentences, sentence_scores, key=sentence_scores.get)

    # Join selected sentences
    return " ".join(summary_sentences)


# ABSTRACTIVE SUMMARIZATION
def abstractive_summary(text):
    """
    This function performs abstractive summarization
    using the T5 transformer model.
    """

    # Add "summarize:" prefix 
    input_text = "summarize: " + text

    # Convert text into tokens 
    inputs = tokenizer.encode(
        input_text,
        return_tensors="pt",      # Return PyTorch tensors
        max_length=512,           # Maximum input size
        truncation=True           # Cut if too long
    )

    # Generate summary using beam search
    summary_ids = model.generate(
        inputs,
        max_length=200,           # Maximum summary length
        min_length=60,            # Minimum summary length
        length_penalty=2.0,       # Controls summary size
        num_beams=4,              # Beam search (quality control)
        early_stopping=True       # Stop when best result found
    )

    # Convert tokens back to normal text
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# HYBRID FUNCTION

def generate_hybrid_summary(text):
    """
    Hybrid approach:
    Step 1 -> Extractive summarization
    Step 2 -> Abstractive summarization
    """

    # First reduce text using extractive method
    extracted_text = extractive_summary(text, limit_sentences=8)

    # Then rewrite using abstractive model
    final_summary = abstractive_summary(extracted_text)

    return final_summary