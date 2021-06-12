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
            "uuid": self.uuid,
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

@app.route('/profile', methods=['POST', 'GET', 'DELETE', 'PUT'])
def add():
    if request.method == 'POST':
        try:
            raw_profile = request.json
            profile = Profile(raw_profile[username], raw_profile[uuid], raw_profile[content], raw_profile[location])
            profiles.append(profile)
            return {
                'status': 1,
                'uuid': profile.uuid
            }
        except:
            return {
                'status': 0,
            }
    elif request.method == 'GET':
        try:
            profile = profiles.get(request.json)
            return {
                'status': 1,
                'username': profile.username,
                'content': profile.content,
                'location': profile.location
            }
        except:
            return {
                'status': 0
            }
        # return profile
    elif request.method == 'DELETE':
        try:
            profiles.delete(request.json)
            return {
                'status': 1
            }
        except:
            return {
                'status':0
            }
    elif request.method == 'PUT':
        try:
            profiles.update(request.json)
            return {
                'status': 1,
                'uuid': profile.uuid
            }
        except:
            return {
                'status': 0
            }
        

        # profile.update(username, uuid, content, location)
