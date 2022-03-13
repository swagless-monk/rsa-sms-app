# Import user defined functions
from config_secrets import twitter_api_key as key, twitter_api_secret as api_secret, twitter_access_token as access, twitter_access_secret as acc_secret, crypto_lexicon_update as clu, cmc_api_key
from create_gauge_chart import create_guage_chart

# Import third party modules
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
from coinmarketcapapi import CoinMarketCapAPI as API
from tweepy import OAuthHandler, API
import pandas as pd

# Import python standard lib
from datetime import datetime as dt

# Twitter search and language adjustment
class TwitterSearch:
    # Connect to twitter and search api
    def twitter_search(self, query):
        # API details
        auth = OAuthHandler(key, api_secret)
        auth.set_access_token(access, acc_secret)
        api = API(auth)
        
        # Search twitter for tweets (using upper case and lower case)
        try:
            tweets_search = api.search_tweets(q=query, lang="en", count=200)
        except:
            print('[UNKNOWN ISSUE] Problem occurred when trying to connect to/search api')

        return tweets_search


    def create_lexicon(self):
        # Initialize sentiment intensity analyzer and dataframe
        sentiment_analyzer = SIA()

        # Update lexicon
        try:
            twitter_lexicon = pd.read_csv(clu).reset_index(drop=True).to_dict()
            update = zip(twitter_lexicon['word'].values(), twitter_lexicon['sentiment'].values())
        except NameError:
            return 'Could not find csv for crypto lexicon data, name error'
        except FileNotFoundError:
            return 'Could not use crypto_lexicon_update.csv, file not found'
        except KeyError:
            return 'Could not locate keys for Update Lexicon, key error'
        except:
            return '[UNKNOWN ISSUE] Problem creating lexicon, unknown error'

        sentiment_analyzer.lexicon.update(update)

        return sentiment_analyzer

class Validate:
    def validate_total_3(self, query):
        if query in ("BTC", "ETH"):
            return True
        else:
            return False

    def validate_ticker(self, query):
        cmc = API(cmc_api_key)
        try:
            r = cmc.cryptocurrency_info(symbol=query)
        except:
            return False
        else:
            return True

    def validate_search(self, input_sms):
        tweets_search = TwitterSearch().twitter_search(input_sms)
        relevancy_flag = len(tweets_search) > 0
        tweet_sum = len(tweets_search)
        
        if relevancy_flag:
            #print(len(tweets_search))
            return tweet_sum
        else:
            #print([tweet.text for tweet in tweets_search][:5][0])
            #print(tweets_search)
            return 0