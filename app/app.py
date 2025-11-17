import os
import re
import json
from io import BytesIO
from datetime import datetime

from flask import Flask, request, render_template, send_file
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai

# Load environment variables (GOOGLE_API_KEY, APP_ACCESS_TOKEN)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the exact model name you saw in list_models()
MODEL_NAME = "models/gemini-2.5-flash"  # <-- change if needed

app = Flask(__name__)

# Simple "restricted access" token so it's not open to everyone
ACCESS_TOKEN = os.getenv("APP_ACCESS_TOKEN", "secret123")

SYSTEM_INSTRUCTIONS = """
You are an assistant that classifies public comments responding to an article.

For each comment, you MUST return a STRICT JSON object with:
- sentiment: one of ["positive", "neutral", "negative"]
- stance: one of ["supports_topic", "criticizes_topic", "mixed", "unrelated"]
- toxicity: one of ["none", "low", "medium", "high"]
- topic: a short phrase summarizing the main issue (e.g., "women in music", "nostalgia", "diversity", "industry sexism", "housing policy").
- explanation: 1-2 sentences explaining your labels in plain language.

Return ONLY valid JSON. Do not include code fences or extra commentary.
"""

model = genai.GenerativeModel(MODEL_NAME)


def parse_json_from_response(text: str) -> dict:
    """Clean up the model output and parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        # remove ```json ... ``` wrapper if present
        text = text.strip("`")
        text = re.sub(r"^json", "", text, flags=re.IGNORECASE).strip()
    return json.loads(text)


def classify_comment(text: str) -> dict:
    """Send a single comment to the LLM and get labels back."""
    prompt = f"""{SYSTEM_INSTRUCTIONS}

Comment: "{text}"

Respond with JSON now."""
    response = model.generate_content(prompt)
    raw = response.text
    try:
        return parse_json_from_response(raw)
    except Exception as e:
        # Fallback so the pipeline doesn't crash
        return {
            "sentiment": "neutral",
            "stance": "mixed",
            "toxicity": "none",
            "topic": "unknown",
            "explanation": f"Parsing error: {e}"
        }


@app.route("/", methods=["GET"])
def index():
    """Render the upload page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle CSV upload, run LLM classification, return labeled CSV."""
    token = request.form.get("token")
    if token != ACCESS_TOKEN:
        return "Access denied: invalid token", 403

    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    # Read CSV
    try:
        df = pd.read_csv(file)
    except Exception:
        return "Could not read CSV. Make sure it is a valid CSV file.", 400

    if "comment_text" not in df.columns:
        return "CSV must contain a 'comment_text' column.", 400

    # Quick cleaning
    df["comment_clean"] = (
        df["comment_text"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Run classification
    results = []
    for text in df["comment_clean"].tolist():
        results.append(classify_comment(text))

    df_labels = pd.DataFrame(results)
    df_out = pd.concat(
        [df.reset_index(drop=True), df_labels.reset_index(drop=True)],
        axis=1
    )

    # Write to in-memory buffer
    buf = BytesIO()
    df_out.to_csv(buf, index=False)
    buf.seek(0)

    filename = f"comments_labeled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="text/csv"
    )


if __name__ == "__main__":
    # Run the app (for local testing)
    app.run(debug=True, port=5001)
    
@app.route("/test")
def test():
    files = os.listdir(TEMPLATE_DIR)
    return f"Templates folder: {TEMPLATE_DIR}<br>Files: {files}"

