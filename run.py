from flask import Flask, request, render_template_string, send_file
import requests
import os

app = Flask(__name__)

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    return response.text

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        response_text = search_google(query)
        save_to_file(response_text, 'response.html')
        return send_file('response.html')
    return '''
        <form method="post">
            <input type="text" name="query" placeholder="Enter your search query">
            <input type="submit" value="Search">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)