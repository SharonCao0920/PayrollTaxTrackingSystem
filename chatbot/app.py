from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Replace "your_openai_api_key" with your actual OpenAI API key
openai.api_key = 'your_openai_api_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=user_message,
      max_tokens=150,
      temperature=0.7,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
