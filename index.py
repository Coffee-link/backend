from flask import Flask
from flask import request
from tinydb import TinyDB, Query
from tinydb import Query

db = TinyDB('./db.json')

class ProfileManager:
    def __init__(self):
        self.profiles = db.table('profiles')
        self.Profile = Query()

    def add_profiles(self, username, uuid, content, location):
        results = self.get(uuid)
        if (len(results) == 0):
            profile = {
                "username": username,
                "uuid": uuid,
                "content": content,
                "location": location,
                "histories": []
            }
            self.profiles.insert(self.to_json(profile))
            return self.get(uuid)
        else:
            return []

    def to_json(self, profile):
        return {
            "username": profile.get('username', ''),
            "id": profile.get('uuid', ''),
            "content": profile.get('content', ''),
            "location": profile.get('location', ''),
            "histories": profile.get('histories')
        }
    
    def add_meeting(self, meeting):
        return True

    def get(self, id):
        return self.profiles.search(self.Profile.id == id)
    
    def delete(self, id):
        profiles = self.profiles.search(self.Profile.id == id)
        self.profiles.remove(doc_ids=[profile.doc_id for profile in profiles])        

    def update(self, id, data):
        for k in data.keys():
            print('key', k)
            self.profiles.update({k: data[k]}, self.Profile.id == id)
        return self.get(id)

profileManager = ProfileManager()

app = Flask(__name__)

@app.route('/')
def hello():
    # show the user profile for that user
    return 'mainpage'

def getId(request):
    user_id = request.json.get('id', '')
    if not user_id:
        raise ValueError()
    return user_id

@app.route('/profile', methods=['POST', 'GET', 'DELETE', 'PUT'])
def add():
    if request.method == 'POST':
        try:
            raw_profile = request.json
            profile = profileManager.add_profiles(
                raw_profile['username'], raw_profile['id'], raw_profile['content'], raw_profile['location']
            )[0]
            return {
                'status': 1,
                'uuid': profile['id']
            }
        except:
            return {
                'status': 0,
            }

    elif request.method == 'GET':
        try:
            user_id = getId(request)
            profile = profileManager.get(user_id)[0]
            print(profile)
            return {
                'status': 1,
                'username': profile['username'],
                'content': profile['content'],
                'location': profile['location']
            }
        except:
            return {
                'status': 0
            }

    elif request.method == 'DELETE':
        try:
            user_id = getId(request)
            profileManager.delete(request.json)
            return {
                'status': 1
            }
        except:
            return {
                'status':0
            }

    elif request.method == 'PUT':
        try:
            user_id = getId(request)
            profile = profileManager.update(user_id, request.json.get('data', {}))[0]
            print(profile)
            return {
                'status': 1,
                'uuid': profile['id']
            }
        except:
            return {
                'status': 0
            }
        

        # profile.update(username, uuid, content, location)
