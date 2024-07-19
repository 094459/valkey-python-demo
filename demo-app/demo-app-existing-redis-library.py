from flask import Flask, render_template, request, redirect, url_for

import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        r.rpush('messages', message)

    messages = r.lrange('messages', 0, -1)
    return render_template('index.html', messages=messages)

@app.route('/delete', methods=['GET','POST'])
def delete():
    r.rpop('messages')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
