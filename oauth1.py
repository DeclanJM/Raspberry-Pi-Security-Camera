import tweepy

#Input your API Keys
api_key = ''
api_secret = ''
bearer_token = r''
access_token = ''
access_token_secret = ''

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)