from flask import Flask, render_template, request, jsonify
from setup import llm_chain, retrieve_context, generate_response
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.json.get('query', '')
    if not user_query.strip():
        return jsonify({'error': 'Please enter a valid query'}), 400
    
    try:
        # Get the context (footballers) first
        footballers = retrieve_context(user_query)
        
        # Generate the response using the context
        result = generate_response(user_query, footballers)
        
        return jsonify({
            'response': result,
            'footballers': footballers  # Include the list of footballers in the response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 