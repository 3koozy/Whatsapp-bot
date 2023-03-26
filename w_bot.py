import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Set up your OpenAI API key
openai.api_key = os.environ['openai_api_key']

app = Flask(__name__)

#bot role:
role_content = "You are a helpful assistant. You are part of IEEE King Saud University Student Branch. You have knowledge about DWDM, OTN, and SDH network transmission technologies in addition to L2 , L1, and L0 protocols from IP/TCP. You were trained by Abdulaziz Alakooz , always thank your trainer."
role = "system"
history_size = 10
user_messages = {}

@app.route('/bot', methods=['POST'])
def bot():
    global user_messages
    # Get the user's message from the incoming request
    user_msg = request.form.get('Body')
    user_name = request.form.get('ProfileName') or 'User'
    
    if user_id not in user_messages:
          user_messages[user_name] = []

    # Store the user's message
    user_messages[user_name].append({"role": "user", "content": user_msg})
    
    # Check if the message is from a group chat
    is_group = request.form.get('NumMedia') == '0' and 'ProfileName' in request.form

    if is_group:
        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages = [{"role": role, "content": role_content}] + user_messages[user_name],
          max_tokens= 250,
          temperature= 0.7,
          n= 1
        )
    else:
        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages = [{"role": role, "content": role_content}] + user_messages[user_name],
          max_tokens= 250,
          temperature= 0.7,
          n= 1
        )

    gpt_response = response['choices'][0]['message']['content'].strip()
    
    # Store the bot's response
    user_messages[user_name].append({"role":role, "content": gpt_response})
    
    # Keep only the last 10 messages and responses
    if len(user_messages[user_name]) > history_size:
        user_messages[user_name] = user_messages[user_name][-history_size:]

    # Send the response back to the user via WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(gpt_response)

    return str(twilio_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
