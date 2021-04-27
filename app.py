from flask import Flask, render_template, request, jsonify
import detect_fitur
import database
import extract_info

app = Flask(__name__)

app.config['SECRET_KEY'] = 'shafira'

@app.route('/')
def index():
    return render_template('example.html')

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return detect_fitur.get_bot_response(userText)
    # return str(get_bot_response(userText))

if __name__ == "__main__":
    app.run(debug=True)




