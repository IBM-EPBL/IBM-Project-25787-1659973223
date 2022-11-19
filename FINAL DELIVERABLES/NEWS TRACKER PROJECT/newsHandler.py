from datetime import date
from newsdataapi import NewsDataApiClient


def getRecentNews():
    api = NewsDataApiClient(apikey="WNGTPRlRrRF7UKUDSZ3l65CKEJaQPhZs")
    news = []
    for i in range(10):
        l = [d for d in api.news_api(country = "in",page=i,language='en')['results'] if d['pubDate'][0:10]==date.today().strftime("%Y-%m-%d")]
        news = news + l
    return news