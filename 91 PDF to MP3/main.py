from pypdf import PdfReader
import requests as req
from dotenv import load_dotenv
import os

load_dotenv()
VOICE_RSS_API_KEY = os.environ['VOICE_RSS_API_KEY']
VOICE_RSS_API_URL = 'https://api.voicerss.org/'


def pdf_to_text(file: str, page_range='all'):
    '''Takes the file path to a PDF as a parameter and returns its text as a string. You can supply a range of pages as a zero indexed tuple where the first number is the starting page and the last number is a non-inclusive range end.'''
    reader = PdfReader(file)
    full_text = ''
    if page_range == 'all':
        for page in reader.pages:
            full_text += page.extract_text()
    else:
        for i in range(*page_range):
            full_text += reader.pages[i].extract_text()
    return full_text


def text_to_speech(text: str, ):
    '''Takes the a string as a parameter and converts it to audio data with the Voice RSS API.'''
    params = {
        'key': VOICE_RSS_API_KEY,
        'hl': 'en-us',
        'src': text,
        'c': 'MP3'
    }
    res = req.get(VOICE_RSS_API_URL, params=params)
    return res.content


def speech_to_mp3(speech, file_name="text_to_speech"):
    '''Takes audio data and writes it to an MP3 file.'''
    with open(f'{file_name}.mp3', "wb") as f:
        f.write(speech)
        print('File successfully written.')


text = pdf_to_text('example.pdf')
speech = text_to_speech(text)
speech_to_mp3(speech)
