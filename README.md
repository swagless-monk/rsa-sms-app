RSA or Relative Sentiment Analysis is a project designed to generate both csv files and text message outputs based on given inputs.

#messaging.py
allows a user to text a provided phone number with a given crypto ticker symbol and receive a sentiment analysis score based on the most recent 100 to 1000 tweets and reddit posts

#twitter_search.py 
will generate a csv file based on the most recent 100 twitter posts run every 5 minutes (done via task scheduler on a windows pc) and uploads that csv to a database

#reddit_search.py 
does the same as twitter_search.py except for reddit data
