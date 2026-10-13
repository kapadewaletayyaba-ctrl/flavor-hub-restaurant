from flask import Flask, render_template, request, jsonify
import os

# Set template_folder to the current directory '.' since index.html is right next to app.py
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
