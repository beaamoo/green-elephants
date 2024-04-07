from twilio.rest import Client
import os

# Load environment variables
with open('.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=', 1)
        os.environ[key] = value

# Access environment variables
account_sid = os.environ.get('TWILIO_SID')
auth_token = os.environ.get('TWILIO_TOKEN')

# # Initialize Twilio client
client = Client(account_sid, auth_token)

# Define function to send messages
def send_initial_message(to, message):
    message = client.messages.create(
                    body=message,
                    from_='whatsapp:+14155238886',
                    to=to
                )
    print(f"Message sent to {to}: {message.sid}")

send_initial_message('whatsapp:+34686146727',' Welcome! Here you can tokenize your EU Carbon Emmision Report.')