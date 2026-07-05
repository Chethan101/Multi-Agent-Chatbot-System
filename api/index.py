from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Multi-Agent Chatbot API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/api/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/api/chat': {
                'method': 'POST',
                'description': 'Send a message to the chatbot',
                'request_body': {
                    'input': 'str - Your question or message',
                    'openai_api_key': 'str - Your OpenAI API key'
                }
            }
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        user_input = data.get('input')
        openai_api_key = data.get('openai_api_key')
        
        if not user_input or not openai_api_key:
            return jsonify({'error': 'Missing required fields: input and openai_api_key'}), 400
        
        # Placeholder response - integrate your graph logic here
        return jsonify({
            'response': f'Echo: {user_input}',
            'message': 'Chat endpoint is working. Replace this with your graph implementation.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export for Vercel
handler = app
