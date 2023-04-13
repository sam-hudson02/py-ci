# add src to path
import os
import sys
path_src = os.path.abspath('./src')
sys.path.insert(1, path_src)
from flask import Flask, request
from githook.githook import GitHook
from githook.event import Event
from dotenv import load_dotenv
from builder.builder import Build
from notify.discord_notify import discord_notify
import json
import threading as th

app = Flask('app')

load_dotenv('./secret/conf.env')

def get_secret():
    secret = os.getenv('GIT_SECRET')
    if secret is None:
        raise ValueError('No secret found')
    return secret

github_secret = get_secret()
github = GitHook(github_secret)
discord_webhook = os.getenv('DISCORD_WEBHOOK')

def save_event_to_json(event: dict):
    with open(f'./event_example.json', 'w') as f:
        json.dump(event, f, indent=4)

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.get_json()
    print(message)
    save_event_to_json(message)
    try:
        event = github.handle(request)
        th.Thread(target=handler, args=(event,)).start()
        return '', 200
    except Exception as e:
        print(e)
        return '', 404
    # return with status code 200
    


def handler(event: Event):
    on_push(event)

def on_push(event: Event):
    build = Build(event)
    build.run()
    discord_notify(build, discord_webhook)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)
