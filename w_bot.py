import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Set up your OpenAI API key
openai.api_key = os.environ['openai_api_key']

app = Flask(__name__)

#bot role:
bot_role = "You are a helpful assistant."

@app.route('/bot', methods=['POST'])
def bot():
    # Get the user's message from the incoming request
    user_msg = request.form.get('Body')
    user_name = request.form.get('ProfileName') or 'User'

    # Check if the message is from a group chat
    is_group = request.form.get('NumMedia') == '0' and 'ProfileName' in request.form

    if is_group:
        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages = [{"role": "system", "content": bot_role},
                        {"role": "user", "content": f"{user_name} in a group chat asks: {user_msg}"}],
          max_tokens= 250,
          temperature= 0.7,
          n= 1
        )
    else:
        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages = [{"role": "system", "content": bot_role},
                        {"role": "user", "content": user_msg}],
          max_tokens= 250,
          temperature= 0.7,
          n= 1
        )

    gpt_response = response['choices'][0]['message']['content'].strip()

    # Send the response back to the user via WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(gpt_response)

    return str(twilio_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
