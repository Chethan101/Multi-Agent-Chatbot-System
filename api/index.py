from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Add repo root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import get_graph

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
        
        # Set OpenAI API key
        os.environ['OPENAI_API_KEY'] = openai_api_key
        
        # Get and invoke the graph
        graph = get_graph()
        result = graph.invoke({"input": user_input})
        
        return jsonify({
            'response': result.get('response', 'No response generated'),
            'plan': result.get('plan', []),
            'past_steps': result.get('past_steps', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export for Vercel
handler = app
