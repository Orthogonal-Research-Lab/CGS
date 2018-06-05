Dataset Links:

Google n-Gram: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html

* use the English 1-gram files. They are fairly large, so I'm not sure how you want to handle them.

World Color Survey: http://www1.icsi.berkeley.edu/wcs/

I realize that building a database from the Google n-gram source data might be a bit too much hard-core data science for your projects. So there is another option for working with n-gram data. If you want to run queries in the viewer at https://books.google.com/ngrams, you can scrape the results using either a Python scraper or use a program that extracts data from graphs. This will provide you with a fairly rich numerical dataset without too much overhead.

Scrapers:
1) https://github.com/econpy/google-ngrams
2) https://github.com/jbowens/google-ngrams-scraper
3) https://github.com/dimazest/google-ngram-downloader

Graph extractors:
1) https://automeris.io/WebPlotDigitizer/
2) http://connectedresearchers.com/graph-digitizer-comparison-16-ways-to-digitize-your-data/
