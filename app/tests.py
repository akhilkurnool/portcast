import unittest

from peewee import EXCLUDED

from app.helpers import *
from app.models import *


class DatabaseTests(unittest.TestCase):
  def setUp(self):
    db = SqliteDatabase(':memory:')
    db.bind([WordFrequency, Paragraphs])
    db.connect()
    db.create_tables([WordFrequency, Paragraphs])
  
  def tearDown(self):
    # Drop the test database
    db = BaseModel._meta.database
    db.drop_tables([WordFrequency, Paragraphs])
    db.close()

  def test_add_new_paragraph(self):
    dummy = "lorem ipsum lorem ipsum"
    noOfRows = Paragraphs(paragraph=dummy).save()
    if noOfRows != 1:
      raise Exception('Paragraph not added!')

  def test_add_word_frequency(self):
    word_dict = {'word1': 10, 'word2': 20, 'word3': 30}
    word_frequencies_tuple = [(w,f) for w,f in word_dict.items()]
    query = WordFrequency.insert_many(word_frequencies_tuple, fields=[WordFrequency.word, WordFrequency.frequency])
    with db.atomic():
      query.on_conflict(
        conflict_target=WordFrequency.word,
        preserve=WordFrequency.frequency,
        update={WordFrequency.frequency: WordFrequency.frequency + EXCLUDED.frequency}
      ).execute()
    words = WordFrequency.select()
    for word in words:
      if word_dict[word.word] != word.frequency:
        raise Exception('Incorrect values inserted')

class HelpersTests(unittest.TestCase):

  def test_remove_chars(self):
    test_str = '#test,1.test'
    new_str = remove_chars(test_str)
    self.assertEqual(new_str, 'test1test')
  
  def test_parsed_word_list(self):
    paragraph = "#Abcd abcd oplo."
    parsed = parsed_word_list(paragraph)
    self.assertListEqual(parsed, ['abcd', 'abcd', 'oplo'])
  
  def test_merge_count_dicts(self):
    d1 = {'a': 1, 'b': 2}
    d2 = {'b': 2, 'c': 3}
    merged = merge_count_dicts(d1, d2)
    self.assertDictEqual(merged, {'a': 1, 'b': 4, 'c': 3})
  
  def test_validate_search_query_false(self):
    self.assertFalse(validate_search_query([]))
  
  def test_validate_search_query_false(self):
    self.assertFalse(validate_search_query(['', 'abcd']))
  
  def test_validate_search_query_true(self):
    self.assertTrue(validate_search_query(['word2', 'word1']))

if __name__ == '__main__':
  unittest.main()
