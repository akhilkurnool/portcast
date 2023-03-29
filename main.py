from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from error_codes import Error
from models import db
from controller import update_word_freq_and_para, search_paragraphs, get_top_words_definition, Operators
from helpers import validate_search_query
from constants import Url, Misc

import requests

app = FastAPI()

formatedParaUrl = Url.PARAGRAPH_URL.format(Misc.NO_OF_PARAGRAPHS, Misc.NO_OF_SENTENCES)

@app.get("/", response_class=PlainTextResponse)
async def get():
  response = requests.get(formatedParaUrl)
  if response.status_code != 200:
    raise HTTPException(status_code=500, detail=Error.GET_PARAGRAPH_FAILED)
  update_word_freq_and_para(response.text)
  return response.text

@app.get("/search")
async def search(q, op):
  if op != Operators.IN and op != Operators.AND:
    raise HTTPException(status_code=400, detail=Error.INVALID_SEARCH_OPERATOR)
  s = q.strip().split(',')
  if not validate_search_query(s):
    raise HTTPException(status_code=400, detail=Error.INVALID_SEARCH_QUERY)
  return search_paragraphs(s, op)

@app.get('/dictionary')
async def dictionary():
  return get_top_words_definition(Misc.NO_OF_TO_WORDS)

