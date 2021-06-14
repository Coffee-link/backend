# -*- coding: UTF-8 -*-

from flask import Flask
from flask import request
from tinydb import TinyDB, Query
from tinydb import Query
import requests
import json

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

    def get_all(self):
        return self.profiles.all()

    def to_json(self, profile):
        return {
            "username": profile.get('username', ''),
            "id": profile.get('uuid', ''),
            "content": profile.get('content', ''),
            "location": profile.get('location', ''),
            "histories": profile.get('histories')
        }
    
    def add_meeting(self, id, meeting_data):
        profile = self.get(id)
        print(profile[0])
        prev_histories = profile[0].get('histories')
        prev_histories.append(meeting_data)
        self.profiles.update({ 'histories': prev_histories }, self.Profile.id == id)
        return prev_histories

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

def getId(request, key='id'):
    user_id = request.json.get(key, '')
    if not user_id:
        raise ValueError()
    return user_id

@app.route('/profile', methods=['POST', 'GET', 'DELETE', 'PUT'])
def profile():
    if request.method == 'POST':
        try:
            raw_profile = request.json
            profile = profileManager.add_profiles(
                raw_profile['username'], raw_profile['id'], raw_profile['content'], raw_profile['location']
            )[0]
            return {
                'status': 1,
                'id': profile['id']
            }
        except:
            return {
                'status': 0,
            }

    elif request.method == 'GET':
        try:
            user_id = request.args.get('id')
            print(user_id)
            profile = profileManager.get(user_id)[0]
            print(profile)
            return {
                'status': 1,
                'id': profile['id'],
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
                'id': profile['id']
            }
        except:
            return {
                'status': 0
            }

@app.route('/profile/history', methods=['GET', 'PUT', 'POST'])
def history():
    if request.method == 'GET':
        try:
            user_id = request.args.get('id')
            profile = profileManager.get(user_id)[0]
            return {
                'status': 1,
                'history': profile['histories']
            }
        except:
            return {
                'status': 0
            }

    elif request.method == 'POST':
        try:
            user_id = getId(request)
            meeting_data = meeting_data.loads(request.json['data'])
            to_user = meeting_data['to']
            
            histories = profileManager.add_meeting(user_id, meeting_data)
            profileManager.add_meeting(to_user, meeting_data)

            return {
                'status': 1,
                'id': user_id,
                'histories': histories
            }
        except:
            return {
                'status': 0
            }
    elif request.method == 'PUT':
        try:
            user_id = getId(request)
            history_id = getId(request, 'history_id')
            data = request.json['data']
            user = profileManager.get(user_id)[0]
            histories = user['histories']
            for i in range(len(histories)):
                if (histories[i]['id'] == history_id):
                    temp = {}
                    for key,value in histories[i].items():
                        temp[key] = value
                    for key, value in data.items():
                        temp[key] = value
                    histories[i] = temp
                    print(temp)
                    print(histories)
                    profileManager.profiles.update({ 'histories': histories }, profileManager.Profile.id == user_id)
                    break
            return {
                "status": 1
            }
        except:
            return {
                'status': 0
            }

@app.route('/profiles', methods=['GET'])
def profiles():
    if request.method == 'GET':
        try:
            user_id = request.args.get('id')
            profiles = profileManager.get_all()
            for i in range(len(profiles)):
                if (profiles[i]['id'] == user_id):
                    del profiles[i]
                    break
            return {
                'status': 1,
                'profiles': profiles
            }
        except:
            return {
                'status': 0
            }

@app.route('/wx/login', methods=['GET'])
def wx_login():
    jscode = request.args.get('jscode')
    url = "https://api.weixin.qq.com/sns/jscode2session"
    r = requests.get(url, params={
        'appid': 'wx78b952b8d9c46fa7',
        'secret': '39e5d67b0a8c79cab96f9e38c27f3e0a',
        'js_code': jscode,
        'grant_type':  'authorization_code'
    })

    return r.json()

@app.route('/wx/notify', methods=['POST'])
def wx_notify():
    print(request.json)
    raw_data = request.json
    from_user_id = raw_data.get('from')
    to_user_id = raw_data.get('to')
    addr = raw_data.get('addr')
    start_date = raw_data.get('range')[0]
    end_date = raw_data.get('range')[1]
    msg_id = raw_data.get('msg_id')

    fromUser = profileManager.get(from_user_id)

    if (not len(fromUser)):
        return {
            'status': '0'
        }

    fromUser = fromUser[0]

    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"

    r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params={
        'grant_type': 'client_credential',
        'appid': 'wx78b952b8d9c46fa7',
        'secret': '39e5d67b0a8c79cab96f9e38c27f3e0a'
    })

    token = r.json()['access_token']

    print("{url}/?access_token={token}".format(url=url, token=token))
    
    data={
        'touser': to_user_id,
        'template_id': '6mtp2i6Sf8wc0GRrASQs0gfN88Sb-p1ZJmjwHLiQ89I',
        'page': 'page/index/index',
        'miniprogramState': 'developer',
        'data': {
            'thing1': {
                'value': '{user}, 请您喝咖啡了'.format(user=fromUser.get('username'))
            },
            'time6': {
                'value': start_date
            },
            'time7': {
                'value': end_date
            },
            'thing2': {
                'value': addr
            }
        }
    }
    data = json.dumps(data)
    # 数据格式化
    # data = bytes(data, 'utf8')

    r = requests.post("{url}?access_token={token}".format(url=url, token=token),  data=data)

    print(r.json())

    return r.json()
