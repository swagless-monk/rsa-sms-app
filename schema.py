# Import user defined functions
from twitter_search import TwitterSearch, Validate
from reddit_search import RedditSearch
from current_price import get_price

# Import third party modules
import pandas as pd

# Import python standard lib
from datetime import datetime as dt

# Create schema
class CreateSchema(TwitterSearch, RedditSearch, Validate):

    # Create schema for ticker searches
    def get_ticker_results(self, query):
        
        # Inhereit twitter search, user defined lexicon, and validation object 
        tweets_search = TwitterSearch().twitter_search(query)
        sentiment_analyzer = TwitterSearch().create_lexicon()
        validation = Validate().validate_search(query)
    
        # Initialize volume class
        volume_class = ''
        
        # Adjust volume class
        if validation >= 90:
            volume_class = "GOOD "
        elif validation >= 60:
            volume_class = "NEUTRAL"
        else:
            volume_class = "LOW"

        # Initialize dataframe
        results = pd.DataFrame()

        # Create root phrase for unique id and insert_date (current date)
        id_root = str(dt.today().strftime('%Y%m%d%H%M%S')).replace(':', '')

        # Store results in lists
        try:
            tweet_id, tweet_text, create_timestamps, create_dates, user_ids, retweets = [id_root + str(tweet.user.id)[-5:] for tweet in tweets_search], [tweet.text for tweet in tweets_search], [tweet.created_at for tweet in tweets_search], [str(tweet.created_at)[:11] for tweet in tweets_search], [tweet.user.id for tweet in tweets_search], [tweet.retweeted for tweet in tweets_search]
            insert_date = [dt.today().strftime('%Y-%m-%d %X') for i in range(len(tweet_id))]
            tweet_query = [query for i in range(len(tweet_id))]
            price = get_price(query)
            btc_price = get_price('BTC')
            eth_price = get_price('ETH')
            current_price = [price for i in range(len(tweet_id))]
            current_btc_price = [btc_price for i in range(len(tweet_id))]
            current_eth_price = [eth_price for i in range(len(tweet_id))]
            vol_class = [volume_class for i in range(len(tweet_id))]

            # Add lists to dataframe
            results['tweet_id'], results['query'], results['current_price'], results['btc_price'], results['eth_price'], results['text'], results['create_timestamp'], results['create_date'], results['user_id'], results['retweet'], results['sentiment'], results['volume_class'], results['insert_date'] = tweet_id, tweet_query, current_price, current_btc_price, current_eth_price, tweet_text, create_timestamps, create_dates, user_ids, retweets, [sentiment_analyzer.polarity_scores(str(text))['compound']*100 for text in tweet_text], vol_class, insert_date
        except TypeError:
            print('Unable to create data for dataframe, type error')
        except UnboundLocalError:
            print('Unable to create insert_date, unbound local error')
        except:
            print('[UNKNOWN ISSUE] Problem creating data for dataframe')

        # Return dataframe
        return results
    
    # Create schema for username/hashtag searches
    def get_userhash_results(self, query):
        # Inhereit twitter search and user defined lexicon
        tweets_search = TwitterSearch().twitter_search(query)
        sentiment_analyzer = TwitterSearch().create_lexicon()
        validation = Validate().validate_search(query)
    
        # Initialize volume class
        volume_class = ''
        
        # Adjust volume class
        if validation >= 90:
            volume_class = "GOOD "
        elif validation >= 60:
            volume_class = "NEUTRAL"
        else:
            volume_class = "LOW"

        # Initialize dataframe
        results = pd.DataFrame()

        # Create root phrase for unique id and insert_date (current date)
        id_root = str(dt.today().strftime('%Y%m%d%H%M%S')).replace(':', '')

        # Store results in lists
        try:
            tweet_id, tweet_text, create_timestamps, create_dates, user_ids, retweets = [id_root + str(tweet.user.id)[-5:] for tweet in tweets_search], [tweet.text for tweet in tweets_search], [tweet.created_at for tweet in tweets_search], [str(tweet.created_at)[:11] for tweet in tweets_search], [tweet.user.id for tweet in tweets_search], [tweet.retweeted for tweet in tweets_search]
            insert_date = [dt.today().strftime('%Y-%m-%d %X') for i in range(len(tweet_id))]
            tweet_query = [query for i in range(len(tweet_id))]
            vol_class = [volume_class for i in range(len(tweet_id))]
            vol_score = [validation for i in range(len(tweet_id))]

            # Add lists to dataframe
            results['tweet_id'], results['query'], results['text'], results['create_timestamp'], results['create_date'], results['user_id'], results['retweet'], results['sentiment'], results['volume_class'], results['vol_score'], results['insert_date'] = tweet_id, tweet_query, tweet_text, create_timestamps, create_dates, user_ids, retweets, [sentiment_analyzer.polarity_scores(str(text))['compound']*100 for text in tweet_text], vol_class, vol_score, insert_date
        except TypeError:
            print('Unable to create data for dataframe, type error')
        except UnboundLocalError:
            print('Unable to create insert_date, unbound local error')
        except:
            print('[UNKNOWN ISSUE] Problem creating data for dataframe')

        # Return dataframe
        return results
    
    # Create schema for reddit results
    def get_reddit_results(self, query):
        # Create sentiment analyzer and Reddit search results object
        sentiment_analyzer = TwitterSearch().create_lexicon()
        reddit_response = RedditSearch().reddit_search(query)

        # Create empty data structures to store data
        results = pd.DataFrame()
        subreddit = []
        titles = []
        selftext = []
        ups = []
        downs = []
        score = []

        for post in reddit_response.json()['data']['children']:
            subreddit.append(post['data']['subreddit'])
            titles.append(post['data']['title'])
            selftext.append(post['data']['selftext'])
            ups.append(post['data']['ups'])
            downs.append(post['data']['downs'])
            score.append(post['data']['score'])

        try:
            reddit_query = [query for i in range(len(score))]
            title_sentiment = [sentiment_analyzer.polarity_scores(title)['compound']*100 for title in titles]
            selftext_sentiment = [sentiment_analyzer.polarity_scores(text)['compound']*100 for text in selftext]
            insert_date = [dt.today().strftime('%Y-%m-%d %X') for i in range(len(titles))]
            price = get_price(query)
            btc_price = get_price('BTC')
            eth_price = get_price('ETH')
            current_price = [price for i in range(len(titles))]
            current_btc_price = [btc_price for i in range(len(titles))]
            current_eth_price = [eth_price for i in range(len(titles))]

            results['query'], results['current_price'], results['btc_price'], results['eth_price'], results['subreddit'], results['title'], results['title_sentiment'], results['selftext'], results['selftext_sentiment'], results['ups'], results['downs'], results['score'] = reddit_query, current_price, current_btc_price, current_eth_price, subreddit, titles, title_sentiment, selftext, selftext_sentiment, ups, downs, score

            results['average_sentiment'] = round((results['title_sentiment'] + results['selftext_sentiment']) / 2, 2)
            results['insert_date'] = insert_date
        except:
            print('[UNKNOWN ISSUE] Problem creating data for dataframe')

        # Return dataframe
        return results