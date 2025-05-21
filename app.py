from flask import Flask, render_template, request, jsonify
from setup import llm_chain
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_query = request.json.get('query', '')
    if not user_query.strip():
        return jsonify({'error': 'Please enter a valid query'}), 400
    
    try:
        result = llm_chain(user_query)
        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 