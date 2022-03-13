# Import standard library modules
from datetime import datetime as dt

# Create required variables
current_date = dt.today().strftime('%Y%m%d')

# Twitter
twitter_access_token = '1455988050958430214-Cd4YUMAoWaFUq4eAshsFyfmV5RpINO'
twitter_access_secret = 'Tg7Y9f9N0WpOsOKos5NTHnAFHJEw5usaVIZWYrbXSLN7v'
twitter_api_key = 'eGvbr0B8hbW5QLX6YSqQ8cZIG'
twitter_api_secret = 'gle6oJh5CCQzT8sNZzbMBmhf4yIBtHABPa9h7gCB4RUDRubmkz'
twitter_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJprZAEAAAAAXEH%2FFRt05ABvpkoDSP7MzLzUdMs%3D6XiDvDZ3to3fQXwkNSVILLCMDPRWuAjggVCmk2zJskjEy7SwPj'

# Reddit
reddit_secret = 'W-mLaZolXXwhqoZ41TWYrOqV33LCGQ'
reddit_client = 'QMRFNFqcYXjWbgKczdlHJA'
reddit_username = 'swagless_monk'
reddit_password = 'spidermanN00737151'

# CoinMarketCap
cmc_api_key = '047317bb-e1a9-4b26-8fa2-975fafd80ac9'

# Save locations
ticker_excel_ouput_location = f'./output/twitter/ticker_output/results_{current_date}.csv'
ticker_backup_save_location = f'./output/backup/twitter/ticker_output/results_{current_date}.csv'
hash_excel_ouput_location = f'./output/twitter/hash_output/results_{current_date}.csv'
hash_backup_save_location = f'./output/backup/twitter/hash_output/results_{current_date}.csv'
unfound_excel_ouput_location = f'./output/twitter/unfound_output/results_{current_date}.csv'
unfound_backup_save_location = f'./output/backup/twitter/unfound_output/results_{current_date}.csv'
reddit_excel_ouput_location = f'./output/reddit/results_{current_date}.csv'
reddit_backup_save_location = f'./output/backup/reddit/results_{current_date}.csv'

# Crypto Lexicon
crypto_lexicon_update = './crypto_lexicon_update.csv'

# Data locations
twitter_ticker = './output/twitter/ticker_output/'
reddit_ticker = './output/reddit/'

# Other
