from flask import Flask, render_template
app = Flask(__name__)
from markov_Nth_order import Markov

app = Flask(__name__)

@app.route('/')
def tweet_deploy():
    sample = 'yoga.txt'
    markov = Markov(sample, 2)
    sentence = markov.generate_sentence()
    return render_template('index.html', sentence=sentence)

if __name__ == "__main__":
    """To run the Flask server, execute `python app.py` in your terminal.
       To learn more about Flask's DEBUG mode, visit
       https://flask.palletsprojects.com/en/2.0.x/server/#in-code"""
    app.run(debug=True)
