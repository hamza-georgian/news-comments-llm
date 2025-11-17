Comment Analyzer — LLM-Powered Text Classification

A lightweight research tool for analyzing public comments using Google Gemini (Google AI Studio)

This project provides a complete pipeline for collecting, cleaning, classifying, and analyzing comments related to online news articles. It includes:

A Jupyter Notebook for scraping article text and running LLM-based classification

A Flask web app that allows researchers to upload a CSV of comments and download a labeled version

Integration with Google AI Studio (Gemini) for sentiment, stance, toxicity, and topic extraction

A clean, expandable structure suitable for academic research or graduate research assistant (RA) positions

Features:

1. Comment Collection

The Jupyter notebook allows users to:

Scrape article text from CBC or other online news sources

Prepare a dataset of comments (manually, scraped, or imported from Reddit/news sources)

2. Data Cleaning

Each comment is cleaned for:

Whitespace normalization

Unicode normalization

Removal of unwanted characters

3. LLM Classification (Google Gemini)

Each comment is passed through a Google Gemini model (e.g., models/gemini-2.5-flash-001) to produce:

Field	Description
sentiment	positive / neutral / negative
stance	supports_topic / criticizes_topic / mixed / unrelated
toxicity	none / low / medium / high
topic	short phrase describing issue
explanation	natural-language justification

Models are configurable in app.py and the notebook.

4. Flask Web Interface

A simple web interface lets researchers:

Upload a CSV with a column named comment_text

Run LLM classification

Download the enriched CSV with label fields added

Optional restricted access using an environment token (APP_ACCESS_TOKEN).

5. Ready for Deployment

Includes:

requirements.txt for dependency management

Procfile for deployment on services like Render

Project Structure:

cbc_comments_project/
│
├── app/
│   ├── app.py                  # Flask web app
│   └── templates/
│       └── index.html          # Upload/download interface
│
├── data/
│   ├── cbc_lilith_article.txt  # Scraped article text (example)
│   ├── cbc_lilith_comments_raw.csv
│   └── cbc_lilith_comments_labeled.csv
│
├── notebooks/
│   └── 01_cbc_lilith_fair_comments.ipynb   # Full pipeline notebook
│
├── .env                        # API keys (excluded from Git)
├── .gitignore                  # Ignore secrets + venv
├── requirements.txt
└── Procfile                    # Deployment config

Installation & Setup:

1. Clone this repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Add your .env file
Create a .env file in the project root:
GOOGLE_API_KEY=your_google_ai_studio_key_here
APP_ACCESS_TOKEN=some_secure_password

5. Run the Flask app locally
cd app
python app.py

Then open:
http://127.0.0.1:5000

Using the Web App:

Prepare a CSV file with at least one column named comment_text

Enter the access token from .env

Upload the CSV

A processed CSV with LLM labels will be automatically downloaded

You’ll receive additional columns:

comment_clean
sentiment
stance
toxicity
topic
explanation

Deployment (Render Example):

This repo includes a Procfile:
web: gunicorn app.app:app

To deploy:

Create a free account at https://render.com
Click New Web Service
Connect this GitHub repo
Set environment variables:
GOOGLE_API_KEY
APP_ACCESS_TOKEN
Deploy

Render will give you a public URL like:
https://your-app-name.onrender.com

Development Notes:

Works with Google AI Studio’s Gemini API (v1beta & v1)
Uses generate_content and strict JSON prompting
Tested on Windows 10/11 and Python 3.10+
Easily extendable to support:
batch uploads
database storage
multi-model analysis
housing policy–specific labels

README.md (this file!)

.gitignore to protect secrets and exclude virtual environments

License:
You may choose to make this MIT, Apache, or leave unlicensed.

Author

Syed Hamza
Toronto, ON
www.hamzasyed.ca
