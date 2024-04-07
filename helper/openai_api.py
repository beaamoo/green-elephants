import openai
import os
import logging

# Load environment variables
with open('.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

# Access environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
latest_response = ""


def chat_complition(prompt: str) -> dict:
    '''
    Call OpenAI API for text completion
    Parameters:
        - prompt: user query (str)
    Returns:
        - dict
    '''
    try:
        # Script providing context for the Assistant's responses
        script = """
You are a farmer assistant. I want you to ask for the following information from the farmer (user) 
and save the answers as key:value python dictionary. 
questions are 1. what is the farmer id? 2. what is the location of the farm ? 3. what is the farm livestock count?  
4. what is the amount of milk production? 5. what is the amount of feed production 6. what is the ammount of methane emission ?.
the Dictionary will have the following keys, and you need to fill the values based on the information you gathered.
keys : "farmerId", "location", "livestockCount", "milkProduction", "feedConsumption", "methaneEmissions".
make sure both keys and values in the Dictionary are in string format, surronded by "".
"""
        
        messages = [
            {"role": "system", "content": script},
            {"role": "user", "content": prompt}
        ]

        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = chat_response.choices[0].message['content']
        logging.info(f"Answer reeived: {response}")
        # print(response)
        
        # Saving response to a variable
        latest_response = response
        # print(latest_response)
        return {
            'status': 1,
            'response': response,
            'latest_response': latest_response
        }
    except Exception as e:
        logging.error(f"Error communicating with ChatGPT: {str(e)}")
        return {
            'status': 0,
            'response': '',
            'latest_response': ''
        }
    