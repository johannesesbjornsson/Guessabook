from random import randint
from google.appengine.api import urlfetch
import json
import re

def get_book():
  book = get_random_book()
  url = "https://www.googleapis.com/books/v1/volumes?q="+book+"&country=AU"
  try:
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      book_info = handle_api_resnponse(result.content)
      return {"book_info": book_info }
    else:
      return {"error": result.status_code}
  except urlfetch.DownloadError:
    return {"error": "error fetching URL" }
  except Exception as e:
    return {'error': e.message}

def handle_api_resnponse(response):
  decoded_response = response.decode("utf-8")
  response_json = json.loads(response)
  book_info = {}
  book_info["title"] = response_json["items"][0]["volumeInfo"]["title"].strip()
  book_info["author"] = response_json["items"][0]["volumeInfo"]["authors"][0].strip()
  book_info["description"] = response_json["items"][0]["volumeInfo"]["description"].strip()
  book_info["image"] = response_json["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"].strip()
  
  replace_author = re.compile(re.escape(book_info['author']), re.IGNORECASE)
  replace_title = re.compile(re.escape(book_info['title']), re.IGNORECASE)
  book_info["description"] = replace_author.sub("[Author]",book_info["description"]  )
  book_info["description"] = replace_title.sub("[Book Title]",book_info["description"]  )

  return book_info

def eval_guess(guess,book): 
  book = book.replace('+', ' ').lower()
  guess = guess.lower()
  if guess == book:
    return {'message' : "correct"}
  elif guess in book or book in guess:
    if len(guess) > 2:
      return {'message' : "you almost got it"}
    else:
      return {'message' : "wrong"}
  else:
    return {'message' : "wrong, don't you know your books? Get a grip"}

def get_random_book():

  index = randint(0, 10)
  list_of_books = [
    "catcher+in+the+rye",
    "the+picture+of+dorian+gray",
    "lord+of+the+flies",
    "never+let+me+go",
    "of+mice+and+men",
    "catch+me+if+you+can",
    "nausea",
    "1984",
    "to+kill+a+mockingbird",
    "lord+of+the+rings",
    "fight+club",

  ]
  book = list_of_books[index]
  return book


