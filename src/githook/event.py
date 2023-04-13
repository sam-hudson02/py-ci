from githook.errors import *

class User():
    def __init__(self, user: dict):
        self.id = user['id']
        self.name = user['name']
        self.login = user['login']
        self.avatar_url = user['avatar_url']
        self.html_url = user['html_url']
        self.type = user['type']
        self.site_admin = user['site_admin']

class UserShort():
    def __init__(self, user: dict):
        self.name = user['name']
        self.email = user['email']
        self.username = user['username']

class Pusher():
    def __init__(self, pusher: dict):
        self.name = pusher['name']
        self.email = pusher['email']

class Repository():
    def __init__(self, repo: dict):
        self.id = repo['id']
        self.full_name = repo['full_name']
        self.name = self.full_name.split('/')[-1]
        self.owner = User(repo['owner'])
        self.private = repo['private']
        self.html_url = repo['html_url']
        self.description = repo['description']

class Commit():
    def __init__(self, commit: dict):
        self.id = commit['id']
        self.author = UserShort(commit['author'])
        self.committer = UserShort(commit['committer'])
        self.message = commit['message']
        self.tree_id = commit['tree_id']
        self.url = commit['url']
        self.added = commit['added']
        self.removed = commit['removed']
        self.modified = commit['modified']

class Push():
    def __init__(self, payload: dict):
        self.ref = payload['ref']
        self.before = payload['before']
        self.after = payload['after']
        self.commits = [Commit(commit) for commit in payload['commits']]
        self.head_commit = Commit(payload['head_commit'])
        self.pusher = Pusher(payload['pusher'])
        self.branch = self.ref.split('/')[-1]

event_type_map = {
    'push': Push
}

class Event():
    def __init__(self, event: dict):
        try:
            self.type = event['event']
            self.payload = event_type_map[self.type](event['payload'])
            self.repository = Repository(event['payload']['repository'])
        except KeyError as e:
            raise invalidPayload(e, event['ip'])
        