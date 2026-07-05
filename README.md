# Twitter Bot Usage Analysis for Indian Political Issues

## 📌 Project Overview

This project is a Flask-based web application that analyzes Twitter data related to Indian political issues. It performs sentiment analysis on tweets and identifies potentially automated (bot) accounts using rule-based heuristics. The application provides interactive visualizations, searchable tweet records, dataset upload functionality, and downloadable PDF reports.

The objective of this project is to demonstrate how social media data can be analyzed to understand public sentiment and detect suspicious account activity.

---

## 🚀 Features

- Upload Twitter dataset (CSV)
- Upload Xquik or other Twitter/X export CSV files without renaming columns
- Sentiment Analysis (Positive, Negative, Neutral)
- Rule-based Bot Detection
- Interactive Pie Charts using Chart.js
- Tweet Search Functionality
- PDF Report Generation
- Dark Mode
- User Statistics Dashboard

---

## 🛠️ Technologies Used

- Python
- Flask
- Pandas
- TextBlob
- HTML5
- CSS3
- JavaScript
- Chart.js
- ReportLab

---

## 📂 Project Structure

```
Twitter-Bot-Analysis/
│
├── app.py
├── data/
│   └── tweets.csv
├── static/
│   ├── style.css
│
├── templates/
│   ├── index.html
│   └── dashboard.html
├── README.md
└── requirements.txt
```

---


## 📊 Dashboard Features

- Displays total tweets and users
- Shows sentiment distribution
- Detects bot and human accounts
- Interactive charts
- Search tweets instantly
- Download analysis report as PDF

## CSV Upload Format

The dashboard stores uploads as `data/tweets.csv` with these columns:

| Column | Meaning |
|--------|---------|
| `user_id` | User, handle, or author identifier |
| `tweet` | Tweet text |
| `followers` | Follower count |
| `following` | Following count |
| `tweets_count` | Lifetime tweet/status count |

Uploads from Xquik and common Twitter/X exports are normalized automatically.
Aliases such as `username`, `screen_name`, `full_text`, `tweet_text`,
`followers_count`, `following_count`, and `tweet_count` are accepted. Missing
numeric bot-detection fields default to `0`, and blank tweet rows are skipped.

---

## 🎯 Future Enhancements

- Machine Learning-based bot detection
- Twitter API integration
- Keyword frequency analysis
- Word Cloud visualization
- Trending hashtag detection
- Export reports in Excel format
- Real-time Twitter data analysis

---

## 👨‍💻 Developed By

**SIRI SHETTY**
