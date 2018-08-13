import logging
from flask import Flask, render_template, request,session,app,redirect
import logic

app = Flask(__name__)
app.secret_key = b'Some_bytes' # Not same as my own

@app.route('/')
def home():
  book= logic.get_book()
  session['guess_correct'] = "false" 

  if 'error' in book:
    with app.app_context():
      return render_template('book_guesser.html',response=book)
    
  session['book_info'] = book['book_info']
  session.modified = True
  
  response = {'message': 'Enter the title of the book you think it is'}
  with app.app_context():
    return render_template('book_guesser.html', response=response,description=session['book_info']['description'],author=session['book_info']['author'],show_author="false")

@app.route('/guess', methods=['POST'])
def guess():
  try:
    guessed_book = request.form['book']
    show_author = request.form['show_author']
  except Exception as e:
    show_author = "false"
    return render_template('book_guesser.html', response=e.message,description=session['book_info']['description'],author=session['book_info']['author'],show_author=show_author)

  guessed_book = verify_user_input(guessed_book)
  if 'error' in guessed_book:
    evaluated_guess = guessed_book 
  else:
    evaluated_guess = logic.eval_guess(session['book_info']['title'], guessed_book['guess'])
    if evaluated_guess['message'] == "correct":
      session['guess_correct'] = "true" 
      return redirect('/end')

  return render_template('book_guesser.html', response=evaluated_guess,description=session['book_info']['description'],author=session['book_info']['author'],show_author=show_author)


@app.route('/end',  methods=['GET', 'POST'])
def end():
  if request.method == 'POST':
    return render_template('game_end.html',correct_answer=session['guess_correct'],title=session['book_info']['title'],image=session['book_info']['image'])
  else:
    with app.app_context():
      return render_template('game_end.html',correct_answer=session['guess_correct'],title=session['book_info']['title'],image=session['book_info']['image'])

def verify_user_input(guess):
  guess_without_white_spaces  = guess.replace(' ','')
  if guess_without_white_spaces == "":
    return {'error': 'Please enter something'}
  if len(guess) > 100:
    return {'error': 'Guess to long'}
  if len(guess) < 2:
    return {'error': 'Guess to short'}
  guess = guess.strip()
  
  return {'guess': guess}


