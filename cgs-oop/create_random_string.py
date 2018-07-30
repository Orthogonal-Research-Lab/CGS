import random
from string import ascii_lowercase
from nltk.corpus import words
import time

letters = [ c for c in ascii_lowercase] + ['']*2

def get_random_word(real_word=True,size=0):

    if real_word:
        return pull_word_from_dict(size)
    else:
        return make_word(size)

def make_word(size):
    word = ''
    if size==0:
        size = random.randint(2,12) 
    for i in range(size):
        word += random.choice(letters)

    return word

def pull_word_from_dict(size):
    if size==0: 
        return random.choice(words.words())
