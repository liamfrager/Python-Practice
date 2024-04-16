from pypdf import PdfReader
import requests as req
from dotenv import load_dotenv
import os

load_dotenv()
VOICE_RSS_API_KEY = os.environ['VOICE_RSS_API_KEY']
VOICE_RSS_API_URL = 'https://api.voicerss.org/'


def pdf_to_text(file: str) -> str:
    '''Takes the file path to a PDF as a parameter and returns its text as a string.'''
    reader = PdfReader(file)
    full_text = ''
    for page in reader.pages:
        full_text += page.extract_text()
    return reader.pages[0].extract_text()


def text_to_speech(text: str):
    params = {
        'key': VOICE_RSS_API_KEY,
        'hl': 'en-us',
        'src': text,
        'c': 'MP3'
    }
    res = req.get(VOICE_RSS_API_URL, params=params)
    print(res)
    return


text = pdf_to_text('example.pdf')
print(text)
text_to_speech(text)
