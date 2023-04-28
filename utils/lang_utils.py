import langid
import requests
def lang_detect(text):
    return langid.classify(text)[0]

url = "http://localhost:3001/translate"

def translate(text):
    lang = lang_detect(text)
    if lang == "zh":
        resp = requests.post(url=url, json={"text": text, "lang": "zh2en"})
    else:
        resp = requests.post(url=url, json={"text": text, "lang": "en2zh"})
    if resp.json()["status"] == 1:
        return resp.json()["text"]
