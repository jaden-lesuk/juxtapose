from flask import Flask, abort, jsonify, request
from flask_cors import CORS
import joblib
from model import *
from flask_pymongo import PyMongo
import json
from bson import json_util
from twitter_api import  *

pipeline = joblib.load('./passagg.sav')

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://admin:735uK74dOMDBA@lesuk.8p4iy.mongodb.net/juxtapose?retryWrites=true&w=majority"
mongo = PyMongo(app)
db_operations = mongo.db.predictions


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/api/v1/predictions")
def get_predictions():
    predictions = db_operations.find()
    # new = {'text': 'This is a test', 'prediction': '1'}
    # db_operations.insert_one(new)
    output = [{
        'id': parse_json(entry['_id']),
        'title': entry['title'],
        'source': entry['source'],
        'link': entry['link'],
        'text': entry['text'],
        'prediction': entry['prediction']} for entry in predictions]
    # 'id': entry['_id'],
    result = {'result': 'successful'}
    return jsonify(output)


@app.route('/api/v1/newprediction', methods=['POST'])
def post_prediction():
    result = request.json
    query_title = result['title']
    query_text = result['maintext']
    query_source = result['source']
    query_link = result['link']
    query = get_all_query(query_title, query_text)
    pred = pipeline.predict(query)
    pred = pred.tolist()

    new = {'source': query_source, 'link': query_link, 'title': query_title, 'text': query_text, 'prediction': pred[0]}
    db_operations.insert_one(new)
    return jsonify(pred[0])


@app.route('/api/v1/tweets')
def twitter_stream():
    tweets = retrieve_tweets()
    output = [{
            'id': tweet[0],
            'user': tweet[1],
            'text': tweet[2],
            'prediction': int(tweet[3])} for tweet in tweets]
    return jsonify(output)
