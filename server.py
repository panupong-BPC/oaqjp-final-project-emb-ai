from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    if request.method == "POST":
        if request.is_json:
            text = (request.get_json(silent=True) or {}).get("text", "")
        else:
            text = request.form.get("textToAnalyze", "") or request.form.get("text", "")
    else:
        text = request.args.get("textToAnalyze", "") or request.args.get("text", "")

    text = (text or "").strip()
    if not text:
        return "Invalid input! Please provide text to analyze.", 400

    result = emotion_detector(text)
    anger   = result["anger"]
    disgust = result["disgust"]
    fear    = result["fear"]
    joy     = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    response_text = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )
    return response_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)