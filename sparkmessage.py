#!/usr/bin/env python

import json
import os
import requests

from flask import Flask
from flask import make_response
from flask import request



# Flask app should start in global layout
app = Flask(__name__)

##
# Authorization token for Spark. Required for working with Spark's API.
#
AUTH = "ZDcxYTdiZjEtZTM4My00ZjAyLTlmN2YtODA2NGFkMWZjZDA4ZjRkZDI5ZDAtZTRh"

##
# Request header for Spark Web API
#
HEADERS = {'Authorization':'Bearer ' + AUTH}

##
# Spark Web API URLs
#
BASE_URL = "https://api.ciscospark.com/v1/"
ROOMS_URL = BASE_URL+"rooms"
MESSAGES_URL = BASE_URL+"messages"
#ROOM_ID = "05d3bfaf-3bca-3767-b767-7c00c10e8a1c"
ROOM_ID = "12a8f8e0-2922-11e7-9841-0b019e058365"

@app.route('/transcription', methods=['POST', 'PATCH'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    
    trascriptedMessage = req.get("result").get("transcription")
    status = req.get("result").get("status")
    guid = req.get("result").get("guid")
    identifier = req.get("result").get("identifier")
    response = send_message(ROOM_ID, trascriptedMessage)
    json_dump = json.dumps(response)
    print(json_dump)
    return json_dump

def send_message(room_id, message):
    data = { "roomId" : room_id,
             "text" : message }
    resp = requests.post(MESSAGES_URL,json=data, headers=HEADERS)
    return json.loads(resp.text)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
