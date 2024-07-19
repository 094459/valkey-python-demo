from flask import Flask, render_template, request, redirect, url_for
import asyncio
from glide import GlideClient, GlideClientConfiguration, NodeAddress

app = Flask(__name__)

# Create an event loop
loop = asyncio.get_event_loop()

# Create a GlideClient instance
async def create_glide_client():
    addresses = [NodeAddress(host="127.0.0.1", port=6379)]
    config = GlideClientConfiguration(addresses)
    return await GlideClient.create(config)

glide_client = loop.run_until_complete(create_glide_client())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        loop.run_until_complete(async_push_message(message))

    glide_client = loop.run_until_complete(create_glide_client())
    raw_messages = loop.run_until_complete(glide_client.lrange('messages', 0, -1))
    return render_template('index.html', messages=raw_messages)

async def async_push_message(message):
    print (message)
    await glide_client.rpush('messages', [message])

async def async_get_messages():
    messages = await glide_client.lrange('messages', 0, -1)
    return [msg for msg in messages]

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    loop.run_until_complete(async_delete_message())
    return redirect(url_for('index'))

async def async_delete_message():
    await glide_client.rpop('messages')

if __name__ == '__main__':
    app.run(debug=True)
