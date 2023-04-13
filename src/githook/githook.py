from githook.validator import Validator
from githook.errors import *
from githook.event import Event
from flask import request
import json

def save_event_to_json(event: dict):
    with open(f'./event_example.json', 'w') as f:
        json.dump(event, f, indent=4)

class GitHook:
    def __init__(self, secret: str):
        self._validator = Validator(secret)

    def handle(self, req: request) -> Event:
        # set request body to bytes
        req.body = req.data
        # parse req.data to json
        self._validator.validate(req)
        message = {}
        message['event'] = req.headers['X-GitHub-Event']
        message['payload'] = req.get_json()
        return Event(message)