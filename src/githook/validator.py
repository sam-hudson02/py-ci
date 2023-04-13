import hmac
import hashlib
from githook.errors import *

class Validator:
    def __init__(self, secret: str):
        self._secret = secret.encode('utf-8')

    def _get_digest(self, body):
        # convert body to bytes
        return hmac.new(self._secret, body, hashlib.sha1).hexdigest()
    
    # returns list of sig parts
    def _get_sig(self, message) -> list:
        headers = message.headers
        try:
            return headers['X-Hub-Signature'].split('=', 1)
        except KeyError:
            raise invalidRequest('No X-Hub-Signature header found', headers['REMOTE_ADDR'])
        
    def validate(self, message) -> None:
        sig = self._get_sig(message)
        headers = message.headers
        if len(sig) != 2:
            raise invalidRequest('X-Hub-Signature header is not a sha1 hash', headers['REMOTE_ADDR'])
        if sig[0] != 'sha1':
            raise invalidRequest('X-Hub-Signature header is not a sha1 hash', headers['REMOTE_ADDR'])
        if not hmac.compare_digest(sig[1], self._get_digest(message.body)):
            raise invalidRequest('X-Hub-Signature does not match body digest', headers['REMOTE_ADDR'])
