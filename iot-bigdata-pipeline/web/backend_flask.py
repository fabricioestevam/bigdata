from flask import Flask, jsonify
from src.core.storage import MongoDBStore

app = Flask(__name__)
storage = MongoDBStore()

@app.route("/latest")
def latest():
    doc = storage.collection.find().sort("timestamp", -1).limit(1)
    return jsonify(list(doc))

if __name__ == "__main__":
    app.run(debug=True)
