from collections import Counter

def remove_chars(string):
    chars_to_remove = set(['.', ',', '!', '#'])
    return ''.join(char for char in string if char not in chars_to_remove)

def parsed_word_list(paragraph):
  if type(paragraph) != str:
    raise TypeError('`str` type is expected as input argument')
  return [w.lower() for w in remove_chars(paragraph.strip()).split()]

def word_count(paragraph):
  return Counter(parsed_word_list(paragraph))

def word_set(paragraph):
  return set(parsed_word_list(paragraph))

def merge_count_dicts(dict1, dict2):
  count = Counter()
  for word, freq in dict1.items():
    count[word] += freq
  for word, freq in dict2.items():
    count[word] += freq
  return count

def dict_to_tuple(dict):
  if not dict: return []
  return [(k,v) for k,v in dict.items()]

def validate_search_query(q):
  if not q:
    return False
  for word in q:
    if word == '': return False
  return True