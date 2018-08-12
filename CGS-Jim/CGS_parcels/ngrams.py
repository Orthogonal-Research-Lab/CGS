import requests
import re
from ast import literal_eval
from pandas import DataFrame

def getNgrams(query, startYear, endYear,smoothing=0,case_insensitive=False):
    """Get google ngram data from https://books.google.com/ngrams
    and store the data in pandas.DataFrame form.
    """
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=15, smoothing=smoothing, case_insensitive=case_insensitive)
    params.pop('case_insensitive') if params['case_insensitive'] is False else _
    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    res = re.findall('var data = (.*?);\\n', req.text)
    if res:
        data = {qry['ngram']: qry['timeseries']
                for qry in literal_eval(res[0])}
        df = DataFrame(data)
        df.insert(0, 'year', list(range(startYear, endYear+1)))
    else:
        df = DataFrame()
    return df

def use_ngram(word_meaning,year):
    """Fetch word frequency data from google ngrams.
    word_meaning should be in the form as below:
    word_meaning = {'apple':[('red',0.15,20),('fruit',0.6,30),('eatable',0.25,5)],\
                  'tomato':[('red',0.3,20),('fruit',0.3,40),('vegetable',0.4,15)]}
    """
    words = word_meaning.keys()
    query = ','.join(words)
    df = getNgrams(query,year,year+1)
    freqs = {}
    for wrd in words:
        try:
            freqs[wrd] = df[wrd].loc[0]
        except:
            # Raise exception when data of word cannot be found from google ngrams
            raise RuntimeError('Can not find "{}" in year {}'.format(wrd,year))
    wrd_mean = {wrd:(freqs[wrd],word_meaning[wrd]) for wrd in words}
    return wrd_mean
