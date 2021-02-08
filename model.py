from stop_words import get_stop_words
import re


def remove_stopwords(s):
    stop_words = get_stop_words('en')
    s = ' '.join(word for word in s.split() if word not in stop_words)
    return s


def get_all_query(title, text):
    total = title + " " + text
    total = preprocessor(total)
    total = [total]
    return total


def preprocessor(text):
    # Converting to Lowercase
    text = str(text).lower()
    # Removing punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Removing links
    text = re.sub(r'http\S+', '', text)
    # Removing stop words
    text = remove_stopwords(text)
    return text
