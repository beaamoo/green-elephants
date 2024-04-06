import openai
import os
import logging

openai.api_key = os.getenv('OPENAI_API_KEY')
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
        script = """You are a helpful assistant knowledgeable about farming practices, 
        designed to collect detailed reports from farmers about their farm conditions. 
        Please ensure you collect accurate information on the farm's name, location, size and
        store the information in a python format hashmap and return it to the user as soon as you get all this info."""
        
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
    