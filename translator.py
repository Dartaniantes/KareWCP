from google.cloud import translate_v2 as tr
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

trClient = tr.Client()


def get_ukr(text):
    return trClient.translate(text, "uk", source_language="en").get('translatedText')


def get_rus(text):
    return trClient.translate(text, "ru", source_language="en").get('translatedText')


def detect(text):
    return trClient.detect_language(text)

