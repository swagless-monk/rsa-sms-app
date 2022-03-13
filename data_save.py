# Import user defined functions
from config_secrets import ticker_excel_ouput_location, ticker_backup_save_location, hash_backup_save_location, hash_excel_ouput_location, unfound_excel_ouput_location, unfound_backup_save_location, reddit_excel_ouput_location, reddit_backup_save_location

# Store results to local (ADJUST TO STORE IN DB)
class Save:
    # Save ticker data
    def save_ticker_file(self, df):
        try:
            # Save to normal location
            df.to_csv(ticker_excel_ouput_location, mode='a')
            # Save to backup location
            df.to_csv(ticker_backup_save_location, mode='a')
        except Exception as e:
            print(f'Error ! {e}')

    # Save reddit data
    def save_reddit_file(self, df):
        try:
            # Save to normal location
            df.to_csv(reddit_excel_ouput_location, mode='a')
            # Save to backup location
            df.to_csv(reddit_backup_save_location, mode='a')
        except Exception as e:
            print(f'Error ! {e}')

    # Save hashtag/@ data
    def save_userhash_file(self, df):
        try:
            # Save to normal location
            df.to_csv(hash_excel_ouput_location, mode='a')
            # Save to backup location
            df.to_csv(hash_backup_save_location, mode='a')
        except Exception as e:
            print(f'Error ! {e}')

    # Save unfound search data
    def save_unfound_file(self, df):
        try:
            # Save to normal location
            df.to_csv(unfound_excel_ouput_location, mode='a')
            # Save to backup location
            df.to_csv(unfound_backup_save_location, mode='a')
        except Exception as e:
            print(f'Error ! {e}')