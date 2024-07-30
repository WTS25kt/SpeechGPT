import openai
import speech_recognition as sr
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数の取得
openai.api_key = os.getenv('OPENAI_API_KEY')

# 音声認識の設定
recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='ja-JP')
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    spoken_text = recognize_speech()
    if spoken_text:
        response = generate_response(spoken_text)
        print(f"AI Response: {response}")
