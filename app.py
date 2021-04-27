from flask import Flask, render_template
from detect_fitur import get_bot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/',methods=['POST'])
def get_response(userMessage):
    # Run fungsi get bot response
    botMessage = get_bot_response(userMessage)
    
    return render_template('index.html',botMessage=botMessage)
# def index():
#     return render_template('index.html')

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text


if __name__ == "__main__":
    app.run(debug=True)