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
    client = openai.OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    response_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    return response_text

if __name__ == "__main__":
    spoken_text = recognize_speech()
    if spoken_text:
        response = generate_response(spoken_text)
        print(f"\nAI Response: {response}")
