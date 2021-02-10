import tweepy
import re
from stop_words import get_stop_words
import joblib

pipeline = joblib.load('./passagg.sav')
api_key = 'vXX3C78YxnCgfYvtBFIBF60t9'
api_key_secret = 'kZmCl59oszinoDnf3Galj2iLeuPm8aOdGedUze2fOPCgzLbmff'
access_token = '875017236079104001-i1rCz2EbqPMKHFUIoGLwIaEG820zKt8'
access_token_secret = 'rfY06KqiHhzXSDn9LmfAJOJYJ0doUnMLBWeAAL3ugtjru'


def remove_stopwords(s):
    stop_words = get_stop_words('en')
    s = ' '.join(word for word in s.split() if word not in stop_words)
    return s


def tweet_preprocessor(text):
    # Converting to Lowercase
    text = str(text).lower()
    # Removing punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Removing links
    text = re.sub(r'http\S+', '', text)
    # Removing stop words
    text = remove_stopwords(text)
    # Remove Hashtags and Usernames & urls
    ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    return text


def retrieve_tweets():
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    all_tweets = []

    for tweet in tweepy.Cursor(api.search, q="Kenya News -filter:retweets", count=100, result_type="recent",
                               include_entities=True, lang="en", tweet_mode='extended').items(100):
        if not tweet.user.verified:
            frame = []
            tweet_id = tweet.id
            user = tweet.user.name
            name = tweet.full_text
            total = str(user) + ' ' + str(name)
            total = [tweet_preprocessor(total)]
            prediction = pipeline.predict(total)
            prediction = prediction.tolist()
            prediction = prediction[0]
            frame.append([tweet_id, user, name, prediction])
            all_tweets.extend(frame)

    return all_tweets
