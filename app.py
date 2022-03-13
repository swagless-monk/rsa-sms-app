# Import user defined modules
from messaging import sms_reply

# Import third party modules
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home_page():
    return 'Hi! Please call me RSA. (pronounced "err-suh", Recent Sentiment Analysis)'

@app.route("/sms", methods=['GET', 'POST'])
def respond():
    # Get text input from user
    input_sms = request.form['Body']
    #input_sms_num = request.form['From']

    # Text replies to users
    return sms_reply(input_sms)

if __name__ == "__main__":
    app.run(debug=True)