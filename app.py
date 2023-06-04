import datetime
import flask
from flask import Flask, request, render_template, redirect, Response, session
import redis

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://:test@localhost:6379/0'
app.secret_key = 'some_unique_and_secret_key'
app.config['SERVER_NAME'] = 'www.bones2peaches.com'
r = redis.StrictRedis.from_url(app.config['REDIS_URL'], charset="utf-8", decode_responses=True)

def event_stream():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('messages')
    for message in pubsub.listen():
        yield 'data: {}\n\n'.format(message['data'])

@app.route('/api/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/api/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']
        user = session.get('user', 'anonymous')
        now = datetime.datetime.now().replace(microsecond=0).time()
        r.publish('messages', '[%s] %s: %s' % (now.isoformat(), user, message))
        return redirect('http://www.bones2peaches.com/api/')
    return render_template('chat.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect('http://www.bones2peaches.com/api/')
    return render_template('login.html')

@app.route('/api/ui/health')
def health_check():
    return {"status": "ok"}

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True , host = '0.0.0.0' , port = '5000' )
