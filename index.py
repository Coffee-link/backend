from flask import Flask
from flask import request

class Profile:
    def __init__(self, username, uuid, content, location):
        self.username = username
        self.uuid = uuid
        self.content = content
        self.location = location
        self.histories=[]

    def to_json(self):
        return {
            "username": self.username,
            "id": self.uuid,
            "content": self.content,
            "location": self.location
        }
    
    def add_meeting(self, meeting):
        self.histories.append(meeting)

    # def update(self, username=self.username, uuid=self.uuid, content=content, location=location):
    #     self.username = username
    #     self.uuid = uuid
    #     self.content = content
    #     self.location = location

profiles = []



app = Flask(__name__)

@app.route('/')
def hello():
    # show the user profile for that user
    return 'hello'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return {
        "user": username
    }

@app.route('/profile', methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        raw_profile = request.json
        profile = Profile(raw_profile)
        profiles.append(profile)
        return {
            'status': 1,
            'uuid': profile.uuid
        }
        # profile = Profile(username, uuid, content, location)
        # profiles.append(profile)
    elif request.method == 'GET':
        raw_profile = request.json
        id = raw_profile.id
        print('get profile')
        return 'get profile'
        # return profile
    elif request.method == 'DELETE':
        print('DELETE profile')
        return 'DELETE profile'
        # profiles.remove(profile)
    elif request.method == 'PUT':
        return 'hiiii'
        # profile.update(username, uuid, content, location)
