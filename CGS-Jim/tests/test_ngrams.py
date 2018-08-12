import pytest
import numpy as np
from CGS_parcels.ngrams import getNgrams,use_ngram

@pytest.fixture
def example_data():
    query='cat,never_exist_word'
    year_start=1800
    year_end=2000
    smoothing=0
    caseInsensitive=False
    return (query,year_start,year_end,smoothing,caseInsensitive)

@pytest.fixture
def example_word():
    word_meaning = {'apple':[('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)],\
                  'tomato':[('red',0.3,20),('fruit',0.3,40),('vegetable',0.4,15)]}
    return word_meaning

def test_getNgrams(example_data):
    data = getNgrams(*example_data)
    with pytest.raises(Exception):
        data['never_exist_word']
    assert np.allclose(data['cat'][0],9.76e-6)

def test_use_ngram(example_word):
    wrd_mean = use_ngram(example_word,1800)
    assert wrd_mean['apple'][1] == [('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)]
    assert np.allclose(wrd_mean['apple'][0],9.01e-6) 
