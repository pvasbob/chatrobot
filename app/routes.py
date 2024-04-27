from app import app
from flask import request

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/example')
def example():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    
    result = f"Received parameters: param1={param1}, param2={param2}"
    
    return result