from flask import Flask, request, jsonify
import sys
import os
import re
import json


# Adding the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'helper')))
from openai_api import chat_complition
from twilio_api import send_message

app = Flask(__name__)
final_response = ""
hashmap = {}

# @app.route('/')
# def home():
#     return jsonify(
#         {
#             'status': 'OK',
#             'wehook_url': 'BASEURL/twilio/receiveMessage',
#             'message': 'The webhook is ready.',
#             'video_url': 'https://youtu.be/y9NRLnPXsb0'
#         }
#     )


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    global hashmap
    try:
        # Extract incomng parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from Openai
        result = chat_complition(message)
        if result['status'] == 1:
            send_message(sender_id, result['response'])
            print(1)
        if extract_hashmap(result['response']):
            final_response = extract_hashmap(result['response'])
            # Convert the string to a hashmap (dictionary)
            hashmap = json.loads(extract_hashmap(result['response']))
            send_message(sender_id, final_response)
    except:
        pass

    print(hashmap)
    print(type(hashmap))
    return 'OK', 200

def extract_hashmap(text):
    # Regex pattern to match the hashmap
    pattern = r'\{(?:\s*".*?"\s*:\s*".*?",?)*\s*\}'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    if match:
        return match.group()
    else:
        return None
    