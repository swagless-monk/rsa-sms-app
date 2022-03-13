# Import user defined functions
from current_price import get_price
from twitter_search import Validate
from schema import CreateSchema
from data_save import Save

# Import third party modules
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

# Import python standard lib
import re
import locale

# Set currency to USD
locale.setlocale(locale.LC_ALL, '')

def mms_reply():
    pass

def sms_reply(input_sms):
    # Initialize search object, save object, and message object
    save = Save()
    schema = CreateSchema()
    validate = Validate()
    response = MessagingResponse()

    # Send received notification
    msg = response.message(f"Checking for {input_sms.upper()}...")
    
    volume = validate.validate_search(input_sms)
    relevancy_flag = volume > 0
    
    if relevancy_flag:

        # Check if input is a username/handle or hashtag
        if input_sms[0] == '@' or input_sms[0] == '#':
            query = input_sms
            ticker_results = schema.get_userhash_results(input_sms.upper())
            avg_sent = round(sum(ticker_results.sentiment) / len(ticker_results.sentiment), 2)
            users = set(ticker_results.user_id)
            
            #print(f'{query.upper()} Social Score: {avg_sent}', end="\n\n")
            #print(data.head(), end="\n\n")
            
            # Save file
            save.save_userhash_file(ticker_results)
            
            # Create Social Score chart
            """create_guage_chart(avg_sent, query)"""

            # Send data
            msg = response.message(f"{input_sms.upper()} \n\nSOCIAL SCORE: {avg_sent} \nTOTAL TWEETS: {len(ticker_results)} \nDISTINCT USERS: {len(users)}", action=f"https://twitter.com/{input_sms.upper()}/")
                
        # Check if input is a ticker
        elif input_sms[0] == '$':

            # Adjust input for CMC 
            query = input_sms.upper().replace('$', '')

            # Create validators for ticker and BTC/ETH
            ticker_validator = validate.validate_ticker(query)
            top_validator = validate.validate_total_3(query)
        
            # Validate that the input query is a valid ticker in coinmarketcap
            if ticker_validator == True:
                # Send failed message
                msg = response.message(f"Unfortunately, I am unable to find {query}. Please try again.")
                return str(response)
            else:
                # Check that input is not BTC or ETH
                if top_validator:
                    # Send failed message
                    msg = response.message(f"Unfortunately, I am forbidden from analyzing {query}. Please try again.")
                    return str(response)

                # Search and return results to user
                else:
                    # Create result set, Social Score, distinct user count from Twitter
                    twitter_ticker_schema = schema.get_ticker_results(query)
                    twitter_avg_sent = round(sum(twitter_ticker_schema.sentiment) / len(twitter_ticker_schema.sentiment), 2)
                    users = set(twitter_ticker_schema.user_id)
                    
                    # Create result set, Social Score, distinct post count from Reddit
                    try:
                        reddit_ticker_schema = schema.get_reddit_results(query)
                    except:
                        # Send data
                        msg = response.message(f"{query} \nhttps://coinmarketcap.com/currencies/{query}/ \n\nPRICE: {locale.currency(get_price(query))} \n\nTWITTER SOCIAL SCORE: {twitter_avg_sent} \nTOTAL TWEETS: {len(twitter_ticker_schema)} \nDISTINCT USERS: {len(users)} \n\nREDDIT SOCIAL SCORE: no data found\n\nBTC PRICE: {locale.currency(get_price('BTC'))} \nETH PRICE: {locale.currency(get_price('ETH'))}")
                        return str(response)

                    if len(reddit_ticker_schema) > 0:
                        reddit_avg_sent = round(sum(reddit_ticker_schema.average_sentiment) / len(reddit_ticker_schema.average_sentiment), 2)
                        reddit_avg_selftext_sent = round(sum(reddit_ticker_schema.selftext_sentiment) / len(reddit_ticker_schema.selftext_sentiment), 2)
                        reddit_avg_title_sent = round(sum(reddit_ticker_schema.title_sentiment) / len(reddit_ticker_schema.title_sentiment), 2)
                        posts = set(reddit_ticker_schema.title)
                        
                        # Save files
                        save.save_ticker_file(twitter_ticker_schema)
                        save.save_reddit_file(reddit_ticker_schema)
                        
                        # Send data
                        msg = response.message(f"{query} \nhttps://coinmarketcap.com/currencies/{query}/ \n\nPRICE: {locale.currency(get_price(query))} \n\nTWITTER SOCIAL SCORE: {twitter_avg_sent} \nTOTAL TWEETS: {len(twitter_ticker_schema)} \nDISTINCT USERS: {len(users)} \n\nREDDIT SOCIAL SCORE: {reddit_avg_sent} \nTITLE SENTIMENT: {reddit_avg_title_sent} \nSELF TEXT SENTIMENT: {reddit_avg_selftext_sent} \nDISTINCT POSTS: {len(posts)} \n\nBTC PRICE: {locale.currency(get_price('BTC'))} \nETH PRICE: {locale.currency(get_price('ETH'))}")
                    else:
                        # Save files
                        save.save_ticker_file(twitter_ticker_schema)
                        
                        # Send data
                        msg = response.message(f"{query} \nhttps://coinmarketcap.com/currencies/{query}/ \n\nPRICE: {locale.currency(get_price(query))} \n\nTWITTER SOCIAL SCORE: {twitter_avg_sent} \nTOTAL TWEETS: {len(twitter_ticker_schema)} \nDISTINCT USERS: {len(users)} \n\nREDDIT SOCIAL SCORE: no data found\n\nBTC PRICE: {locale.currency(get_price('BTC'))} \nETH PRICE: {locale.currency(get_price('ETH'))}")

                    # Create Social Score chart
                    """create_guage_chart(avg_sent, query)"""

                    
        else:
            # Send rejection notice
            msg = response.message(f"Unable to find {input_sms.upper()}. \n\n EXAMPLE SEARCHES: \n @username \n $crypto_ticker \n #hashtag")
    else:
        # Save unfound item to a list
        input_data = [input_sms]
        unfound_search = pd.DataFrame(columns=['word'], data=input_data)
        save.save_unfound_file(unfound_search)

        # Send rejection notice
        msg = response.message(f"Unable to find {input_sms.upper()}. \n\n EXAMPLE SEARCHES: \n @username \n $crypto_ticker \n #hashtag")

    return str(response)