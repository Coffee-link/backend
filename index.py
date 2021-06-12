# from flask import Flask
# from flask import request
from tinydb import TinyDB, Query
from tinydb import operations
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
            return True
        else:
            return False

    def to_json(self, profile):
        return {
            "username": profile.get('username', ''),
            "id": profile.get('uuid', ''),
            "content": profile.get('content', ''),
            "location": profile.get('location', ''),
            "histories": profile.get('histories')
        }
    
    def add_meeting(self, meeting):
        self.histories.append(meeting)

    def get(self, id):
        return self.profiles.search(self.Profile.id == id)
    
    def delete(self, id):
        profiles = self.profiles.search(self.Profile.id == id)
        self.profiles.remove(doc_ids=[profile.doc_id for profile in profiles])        

    def update(self, id, data):
        for k in data.keys():
            self.profiles.update({k: data[k]}, self.Profile.id == id)

m = ProfileManager()
m.add_profiles('1', '2', '3', '4')
print(m.get('2'))
m.update('2', {
    'location': '1234'
})
print(m.get('2'))
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     # show the user profile for that user
#     return 'hello'

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return {
#         "user": username
#     }

# @app.route('/profile', methods=["POST", "GET", "DELETE", "PUT"])
# def add():
#     if request.method == 'POST':
#         raw_profile = request.json
#         profile = Profile(raw_profile)
#         profiles.append(profile)
#         return {
#             'status': 1,
#             'uuid': profile.uuid
#         }
#         # profile = Profile(username, uuid, content, location)
#         # profiles.append(profile)
#     elif request.method == 'GET':
#         raw_profile = request.json
#         id = raw_profile.id
#         print('get profile')
#         return 'get profile'
#         # return profile
#     elif request.method == 'DELETE':
#         print('DELETE profile')
#         return 'DELETE profile'
#         # profiles.remove(profile)
#     elif request.method == 'PUT':
#         return 'hiiii'
#         # profile.update(username, uuid, content, location)
