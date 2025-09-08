import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    def assertDominant(self, text, expected):
        result = emotion_detector(text)
        self.assertIn("dominant_emotion", result, f"No dominant_emotion in {result}")
        self.assertEqual(
            result["dominant_emotion"], expected,
            f"Text: {text!r} -> expected {expected!r}, got {result['dominant_emotion']!r}\nFull: {result}"
        )

    def test_joy(self):
        self.assertDominant("I am glad this happened", "joy")

    def test_anger(self):
        self.assertDominant("I am really mad about this", "anger")

    def test_disgust(self):
        self.assertDominant("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        self.assertDominant("I am so sad about this", "sadness")

    def test_fear(self):
        self.assertDominant("I am really afraid that this will happen", "fear")

if __name__ == "__main__":
    unittest.main(verbosity=2)