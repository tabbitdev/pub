import logging
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from redis import Redis

app = Flask(__name__)
CORS(app)  # Enable CORS
redis = Redis(host='localhost', port=6379, db=0, password='test')

# Set up logging
handler = logging.FileHandler('flask.log')  # logs to a file named flask.log
handler.setLevel(logging.INFO)  # Set the log level to INFO; This will write all INFO and higher level messages to the log file
app.logger.addHandler(handler)  # Add the handler to Flask's logger

@app.route('/api/ui/home')
def hello():
    redis.incr('hits')  # Increment the 'hits' key by 1
    hits = redis.get('hits')  # Get the value of the 'hits' key
    app.logger.info('Page hit: %s', hits.decode())  # Log page hit count
    return jsonify({"message" : 'hits'}),200

@app.route('/api/ui/health')
def health_check():
    return jsonify({"message": "true"}), 200


@app.route('/api/channel/health')
def health_check():
    return jsonify({"message": "true"}), 200




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
