"""Flask web server for Watson Emotion Detection.

Exposes two routes:
- "/" renders the provided index.html.
- "/emotionDetector" analyzes input text and returns a formatted summary.
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

ROUTE_ANALYZE = "/emotionDetector"
ERR_MSG = "Invalid text! Please try again!"

app = Flask(__name__)


@app.route("/")
def index():
    """Render the landing page supplied in templates/index.html."""
    return render_template("index.html")


def _extract_text_from_request(req: request) -> str:
    """Extract user text from JSON, form, or query string."""
    if req.method == "POST":
        if req.is_json:
            return (req.get_json(silent=True) or {}).get("text", "") or ""
        return req.form.get("textToAnalyze", "") or req.form.get("text", "") or ""
    return req.args.get("textToAnalyze", "") or req.args.get("text", "") or ""


def _format_result(result: dict) -> str:
    """Format the analysis dictionary into the required human-readable sentence."""
    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]
    return (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )


@app.route(ROUTE_ANALYZE, methods=["GET", "POST"])
def emotion_detector_route():
    """Analyze text and return the formatted response or an error message."""
    text = _extract_text_from_request(request).strip()
    result = emotion_detector(text)
    if result.get("dominant_emotion") is None:
        return ERR_MSG, 400
    return _format_result(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
