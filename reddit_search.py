# Import user defined secrets
from config_secrets import reddit_secret, reddit_client, reddit_password, reddit_username

# Import python standard lib
from datetime import datetime as dt
import requests

class RedditSearch:
    def reddit_search(self, query):
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(reddit_client, reddit_secret)

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': reddit_username,
                'password': reddit_password}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'Social Score/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

        reddit_response = requests.get(f"https://oauth.reddit.com/r/{query}/new",
                        headers=headers,
                        params={'limit': 100})

        return reddit_response