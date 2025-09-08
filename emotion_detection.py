import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyze: str) -> dict:
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, headers=HEADERS, json=payload, timeout=15)

    data = response.json()
    preds = data.get("emotionPredictions", [])
    emo_raw = preds[0].get("emotion", {}) if preds else {}

    result = {
        "anger":   float(emo_raw.get("anger", 0.0)),
        "disgust": float(emo_raw.get("disgust", 0.0)),
        "fear":    float(emo_raw.get("fear", 0.0)),
        "joy":     float(emo_raw.get("joy", 0.0)),
        "sadness": float(emo_raw.get("sadness", 0.0)),
    }

    result["dominant_emotion"] = max(result, key=result.get) if result else None
    return result