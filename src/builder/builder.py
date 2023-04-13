from githook.event import Event
import os
import subprocess
import time
import sys
# add scripts folder to path
path_src = os.path.abspath('./scripts')
sys.path.insert(1, path_src)


class Build():
    def __init__(self, event: Event):
        self.repository = event.repository.name
        self.is_private = event.repository.private
        self.branch = event.payload.branch
        self.committer = event.payload.head_commit.committer
        self.commit_message = event.payload.head_commit.message
        self.commit_url = event.payload.head_commit.url
        self.build_dir = f'./builds/{self.repository}'
        self.script_dir = f'scripts/{self.repository}.py'
        self.repo_url = event.repository.html_url
        self.stage = 'init'
        self.error = ''
        self.build_time = 0
        self.success = False

    def check_directory(self):
        self.stage = 'Check Directory'
        if not os.path.exists(self.build_dir):
            self.clone()

    def clone(self):
        self.stage = 'Clone'
        if not os.path.exists('./builds'):
            print('Creating builds directory')
            os.mkdir('./builds')
        os.chdir('./builds')
        print(f'Cloning {self.repo_url} into {self.repository}')
        subprocess.run(['gh', 'repo', 'clone', self.repo_url])
        os.chdir('../')

    def pull(self):
        self.stage = 'Pull'
        os.chdir(self.build_dir)
        print(f'Pulling {self.repo_url}')
        subprocess.run(['git', 'pull', 'origin', self.branch])
        os.chdir('../..')

    def switch_branch(self):
        self.stage = 'Branch Checkout'
        os.chdir(self.build_dir)
        print(f'Checking out {self.branch}')
        subprocess.run(['git', 'checkout', self.branch])
        os.chdir('../..')

    def run_script(self):
        print(f'Running {self.repository}.py')
        self.stage = 'Run Script'
        try:
            # run python script
            proc = subprocess.run(['python3', self.script_dir])
            if proc.returncode == 0:
                self.success = True
            else:
                raise Exception('Script returned non-zero exit code')
        except Exception as e:
            print(e)
            self.success = False

    def run(self):
        start = time.time()
        print(f'Building {self.repository}')
        try:
            self.check_directory()
            self.switch_branch()
            self.pull()
            self.run_script()
        except Exception as e:
            print('Build Failed with error:', e)
            self.error = e.__str__()
            self.success = False
        end = time.time()
        self.build_time = end - start
