import tweepy

api_key = "RDHyHWuv8I0yBAe2NCRfuxTr1"
api_secret = "j93hop2IwDNkINO8q4rwm2AYjoKTAmtVUfRFUbCkQGcm6ja4q5"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAFteqwEAAAAAFnq9Wjexz2ycsCZfPY9aHjlttxw%3DhS8rYyWPoQTp8BIgnP7q7wqTscHLNm2HdVG5OO5efE0cnr2zMH"
access_token = "1606067833628246017-mKbaphyUpdrdRhgXd4NGTrufzhsLVp"
access_token_secret = "aAKQtExkxfQ9MwyTA7DqfRschsBHzzZCp19Z55qAFhqUA"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client.create_tweet(text = "HELLO WORLD!?")

# client.like("1613078224539615233")

# client.retweet("1613078224539615233")

# client.create_tweet(in_reply_to_tweet_id="1613078224539615233", text = "Keep learning Simplilearners")

# for tweet in api.home_timeline():
#     print(tweet.text)

# person = client.get_user(username = "narendramodi").data.id

# for tweet in client.get_users_tweets(person).data:
#     print(tweet.text)

