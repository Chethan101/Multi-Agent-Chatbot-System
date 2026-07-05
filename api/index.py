import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from graph import get_graph
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('input')
        openai_api_key = data.get('openai_api_key')
        
        if not user_input or not openai_api_key:
            return jsonify({'error': 'Missing required fields: input and openai_api_key'}), 400
        
        os.environ['OPENAI_API_KEY'] = openai_api_key
        
        graph = get_graph()
        response = graph.invoke({"input": user_input})
        
        return jsonify({'response': response.get('response', 'No response generated')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Multi-Agent Chatbot API', 'endpoints': {'/api/health': 'GET', '/api/chat': 'POST'}})

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
