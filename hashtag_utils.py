import re

from flask import jsonify
from flask.typing import ResponseReturnValue

def generate_hashtag(text):
  words = re.findall(r'\b\w+\b', text)
  hashtags = ['#' + word.capitalized() for word in words if len(word) > 2]
  return hashtags

def is_valid_hashtag(hashtag):
  return bool(re.match(r'^#[A-Za-z0-9_]+$', hashtag))

def save_hashtags(hashtags, filename='hashtags.txt'):
  with open(filename, 'a') as file:
    for hashtag in hashtags:
      file.write(hashtag + '\n')

def load_hashtags(filename='hashtags.txt'):
  try:
    with open(filename, 'r') as file:
      hashtags =file.read().splitlines()
    return hashtags
  except FileNotFoundError:
    return []

# requirement.txt