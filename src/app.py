from flask import Flask, request, jsonify
import sys
import os
import re
import json
import subprocess
from nodejs import node



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
        type(sender_id)
        print('sender_id:'+ sender_id)

        # Get response from Openai
        result = chat_complition(message)
        print(type(result['response']))
        if result['status'] == 1 and result['response'].find('{') < result['response'].find('}'):
            # Extract hashmap from the response field
            print('final state')
            print(result['response'])
            # Convert the string into a Python dictionary using json.loads()
            final = extract_dictionary_from_string(result['response'])
            print(final)
            send_message(sender_id, result['response'])
            print('the type of final is', type(final))
            # final_response = print(extract_hashmap(result['response']))
            # Convert the string to a hashmap (dictionary)
            # hashmap = json.loads(extract_hashmap(result['response']))
            # Call Node.js script and pass JSON data
            # print(final_response)
            # send_message(sender_id, final_response)
            # Check if condition is met to stop the server:
            # Convert data to JSON string
            # json_data = json.dumps(hashmap)
            # Run Node.js script and pass JSON data as an argument
            send_message(sender_id, "Information received. Processing...")
            send_message(sender_id, "Minting NFT...")
            json_data = json.dumps(final)
            # Define the command to call the Python script
            command = ['python', '/Users/adnanbhanji/Documents/GitHub/green-elephants/mintNFT.py', json_data]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Wait for the process to finish and get the output
            output, error = process.communicate()
            # Get the exit code of the process
            exit_code = process.returncode
            # Print the output and error
            print("Output is:", output.decode())
            print(type(output.decode()))
            send_message(sender_id, "Operation Successful. NFT Minted.")
            send_message(sender_id, "Here are your details: " + output.decode())
            send_message(sender_id, "Thank you for using Green Elephants. Have a great day!")
            exit()
        if result['status'] == 1:
            send_message(sender_id, result['response'])
            print('not final state')
            print(1)
    except:
        pass

    return 'OK', 200


def extract_dictionary_from_string(input_string):
    # Find the start and end index of the dictionary portion
    start_index = input_string.find('{')
    if start_index == -1:
        return None  # Return None if the opening brace '{' is not found

    end_index = input_string.rfind('}') + 1
    if end_index == 0:
        return None  # Return None if the closing brace '}' is not found

    # Extract the dictionary portion
    dictionary_string = input_string[start_index:end_index]

    # Remove any leading/trailing whitespace
    dictionary_string = dictionary_string.strip()

    try:
        # Convert the dictionary string into a Python dictionary
        dictionary = json.loads(dictionary_string)
        return dictionary
    except json.JSONDecodeError:
        return None  # Return None if there's an error parsing the JSON
