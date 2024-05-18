from google.cloud import translate_v2 as tr
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

trClient = tr.Client()


def get_ukr(text):
    data = str(text).split("\n")
    result = ''
    for info in data:
        result += trClient.translate(info, "uk", source_language="en").get('translatedText') + "\n"

    return result


def get_rus(text):
    data = str(text).split("\n")
    result = ''
    for info in data:
        result += trClient.translate(info, "ru", source_language="en").get('translatedText') + "\n"
    return result


def detect(text):
    return trClient.detect_language(text)

