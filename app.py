from flask import Flask, render_template, request
import detect_fitur
import database
import extract_info

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jesicashafiradelisha'

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get")
# fungsi untuk mendapatkan response dari bot
def get_bot_response():
    userText = request.args.get('msg')
    return detect_fitur.get_bot_response(userText)

if __name__ == "__main__":
    app.run(debug=True)