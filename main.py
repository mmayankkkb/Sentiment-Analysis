import random
import numpy as np
from textblob import TextBlob
from dataclasses import dataclass

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@dataclass
class Mood:
    emoji: str
    sentiment: float
    subjectivity: float
    reply: str




def get_mood(input_text: str) -> Mood:

    document=[i for i in input_text.split(".")]
    sents=[]
    subjects=[]

    for i in document:
        sents.append(TextBlob(i).sentiment.polarity)
        subjects.append(TextBlob(i).sentiment.subjectivity)
    
    subjects.append(TextBlob(input_text).sentiment.subjectivity)
    sents.append(TextBlob(input_text).sentiment.polarity)

    sentiment: float = np.median(sents)
    subjectivity: float =np.median(subjects)
    reply=""
 

    if sentiment > 0.5:
        emoji = '🤩'
        replies = ["That sounds amazing!", "I love your energy!", "Keep those good vibes coming!"]
    elif sentiment > 0:
        emoji = '🙂'
        replies = ["Glad to hear that.", "Sounds good.", "Nice!"]
    elif sentiment < -0.5:
        emoji = '😡'
        replies = ["That sounds really frustrating.", "I'm sorry you're dealing with that.", "Take a deep breath."]
    elif sentiment < 0:
        emoji = '🙁'
        replies = ["I'm sorry to hear that.", "That's unfortunate.", "Hope things get better."]
    else:
        emoji = '😐'
        replies = ["I see.", "Interesting.", "Tell me more."]

    reply=random.choice(replies)
    return Mood(emoji, sentiment, subjectivity, reply)



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/get', methods=['POST'])
def get_bot_response():
    # 1. Get the message from the HTML (JavaScript)
    data = request.get_json()
    user_text = data.get('message', '')

    # 2. Perform Sentiment Analysis
    mood = get_mood(user_text)

    # 3. Create the response string
    
    bot_reply = f" {mood.reply}    | Mood: {mood.emoji} | Sentiment Score: {mood.sentiment:.2f} | Subjectivity: {mood.subjectivity:.2f}"

    # 4. Send JSON back to the HTML
    return jsonify({'reply': bot_reply})





if __name__ == '__main__':
    app.run(debug=True)



