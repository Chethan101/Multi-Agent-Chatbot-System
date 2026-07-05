from flask import Flask, request, jsonify
from graph import get_graph
import os
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
            return jsonify({'error': 'Missing required fields'}), 400
        
        os.environ['OPENAI_API_KEY'] = openai_api_key
        
        graph = get_graph()
        response = graph.invoke({"input": user_input})
        
        return jsonify({'response': response.get('response', 'No response generated')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False)
