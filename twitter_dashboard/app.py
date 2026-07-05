import os
import io

import pandas as pd
from flask import Flask, redirect, render_template, request, send_file, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textblob import TextBlob

try:
    from .xquik_csv import normalize_tweet_frame
except ImportError:
    from xquik_csv import normalize_tweet_frame

app = Flask(__name__)

UPLOAD_FOLDER = "data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def dataset_path():
    return os.path.join(app.config["UPLOAD_FOLDER"], "tweets.csv")


def load_tweets():
    return normalize_tweet_frame(pd.read_csv(dataset_path()))

# Sentiment function
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def detect_bot(row):

    followers = row['followers']
    following = row['following']
    tweets_count = row['tweets_count']

    # Avoid division errors
    ratio = followers / (following + 1)

    if tweets_count > 5000 and ratio < 0.2:
        return "Bot"
    else:
        return "Human"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    df = load_tweets()

    total_tweets = len(df)
    total_users = df['user_id'].nunique()

    df['sentiment'] = df['tweet'].apply(get_sentiment)
    df['account_type'] = df.apply(detect_bot, axis=1)

    positive = len(df[df['sentiment'] == "Positive"])
    negative = len(df[df['sentiment'] == "Negative"])
    neutral = len(df[df['sentiment'] == "Neutral"])

    bots = len(df[df['account_type'] == "Bot"])
    humans = len(df[df['account_type'] == "Human"])

    # Convert dataframe to records for HTML
    tweets_data = df.to_dict(orient="records")

    return render_template(
        "dashboard.html",
        total_tweets=total_tweets,
        total_users=total_users,
        positive=positive,
        negative=negative,
        neutral=neutral,
        bots=bots,
        humans=humans,
        tweets=tweets_data
    )

@app.route('/download_report')
def download_report():
    df = load_tweets()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Twitter Analysis Report")

    c.setFont("Helvetica", 12)

    c.drawString(100, 700, f"Total Tweets: {len(df)}")
    c.drawString(100, 680, f"Total Users: {df['user_id'].nunique()}")

    df['sentiment'] = df['tweet'].apply(get_sentiment)
    df['account_type'] = df.apply(detect_bot, axis=1)

    positive = len(df[df['sentiment'] == "Positive"])
    negative = len(df[df['sentiment'] == "Negative"])
    neutral = len(df[df['sentiment'] == "Neutral"])

    bots = len(df[df['account_type'] == "Bot"])
    humans = len(df[df['account_type'] == "Human"])

    c.drawString(100, 650, f"Positive Tweets: {positive}")
    c.drawString(100, 630, f"Negative Tweets: {negative}")
    c.drawString(100, 610, f"Neutral Tweets: {neutral}")

    c.drawString(100, 580, f"Bots: {bots}")
    c.drawString(100, 560, f"Humans: {humans}")

    c.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], "tweets.csv")
        uploaded = normalize_tweet_frame(pd.read_csv(file))
        uploaded.to_csv(filepath, index=False)

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
