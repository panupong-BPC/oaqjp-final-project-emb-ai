import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def _none_result():
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

def emotion_detector(text_to_analyze: str) -> dict:
    try:
        payload = {"raw_document": {"text": text_to_analyze}}
        response = requests.post(URL, headers=HEADERS, json=payload, timeout=15)

        if response.status_code == 400:
            return _none_result()

        data = response.json()
        preds = data.get("emotionPredictions", [])
        emo = preds[0].get("emotion", {}) if preds else {}

        result = {
            "anger":   float(emo.get("anger", 0.0)) if emo else None,
            "disgust": float(emo.get("disgust", 0.0)) if emo else None,
            "fear":    float(emo.get("fear", 0.0)) if emo else None,
            "joy":     float(emo.get("joy", 0.0)) if emo else None,
            "sadness": float(emo.get("sadness", 0.0)) if emo else None,
        }
        if any(v is None for v in result.values()):
            return _none_result()

        result["dominant_emotion"] = max(result, key=result.get)
        return result
    except Exception:
        return _none_result()