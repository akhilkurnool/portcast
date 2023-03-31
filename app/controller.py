from peewee import EXCLUDED

from app.helpers import word_count, dict_to_tuple, word_set
from app.models import WordFrequency, Paragraphs, db
from app.constants import Url, Operators

import requests
import concurrent.futures

def update_word_freq_and_para(paragraph, db_instance=None):
  if not db_instance:
    db_instance = db
  count = word_count(paragraph)
  word_frequencies_tuple = dict_to_tuple(count)
  query = WordFrequency.insert_many(word_frequencies_tuple, fields=[WordFrequency.word, WordFrequency.frequency])
  paragraph = Paragraphs(paragraph=paragraph)
  with db_instance.atomic():
    query.on_conflict(
      conflict_target=WordFrequency.word,
      preserve=WordFrequency.frequency,
      update={WordFrequency.frequency: WordFrequency.frequency + EXCLUDED.frequency}
    ).execute()
    paragraph.save()

def search_paragraphs(search_words, op):
  paragraphs = Paragraphs.select()
  res = []
  for para in paragraphs:
    para_word_set = word_set(para.paragraph)
    exists = [word in para_word_set for word in search_words]
    if op == Operators.IN and any(exists):
      res.append(para.paragraph)
    elif op == Operators.AND and all(exists):
      res.append(para.paragraph)
  return res

def make_request(args):
  word, url = args
  response = requests.get(url)
  return (word, response.json())

def get_top_words_definition(num=10):
  most_frequent_words = WordFrequency.select().order_by(WordFrequency.frequency.desc()).limit(num)
  freq_map = {word.word: word.frequency for word in most_frequent_words}
  urls = [(word.word, Url.DICTIONARY_URL.format(word.word)) for word in most_frequent_words]
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(make_request, urls)
  return {word: {'frequency': freq_map[word],'definition': res} for (word, res) in results}
