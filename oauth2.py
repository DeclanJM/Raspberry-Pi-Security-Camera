import tweepy

# Enter API tokens below

#Degbot
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAFteqwEAAAAAFnq9Wjexz2ycsCZfPY9aHjlttxw%3DhS8rYyWPoQTp8BIgnP7q7wqTscHLNm2HdVG5OO5efE0cnr2zMH"
consumer_key = 'RDHyHWuv8I0yBAe2NCRfuxTr1'
consumer_secret = 'j93hop2IwDNkINO8q4rwm2AYjoKTAmtVUfRFUbCkQGcm6ja4q5'
access_token = '1606067833628246017-mKbaphyUpdrdRhgXd4NGTrufzhsLVp'
access_token_secret = 'aAKQtExkxfQ9MwyTA7DqfRschsBHzzZCp19Z55qAFhqUA'

#Shribot
#consumer_key = "aFZCZUlpMTB1WUVab3RiOEFtWlA6MTpjaQ"
#consumer_secret = "mhagc2_3v8R-snUSo6xxKDgYnDZcLNnnitdcGkml5CIu1GJ4wi"
#bearer_token = r"AAAAAAAAAAAAAAAAAAAAAF%2FdqwEAAAAA5gVe9UdrmlaSH6oDumUBUAJGaqk%3DmvRk8A86adWvN5WS90mwGS3T1GmtWDl2pN0zMBWPVrHmWly3qp"
#access_token = "1723244241051058176-sFp9EFfZzNH9rmbKUO7rkoy8yZQvNH"
#access_token_secret = "EGylv9SNrqswI5D0x3HO3Sl84jEnKz40eQ64m2BLCwcIq"

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)