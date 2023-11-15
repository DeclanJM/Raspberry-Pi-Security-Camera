import tweepy

#Degbot Keys
api_key = "RDHyHWuv8I0yBAe2NCRfuxTr1"
api_secret = "j93hop2IwDNkINO8q4rwm2AYjoKTAmtVUfRFUbCkQGcm6ja4q5"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAFteqwEAAAAAFnq9Wjexz2ycsCZfPY9aHjlttxw%3DhS8rYyWPoQTp8BIgnP7q7wqTscHLNm2HdVG5OO5efE0cnr2zMH"
access_token = "1606067833628246017-mKbaphyUpdrdRhgXd4NGTrufzhsLVp"
access_token_secret = "aAKQtExkxfQ9MwyTA7DqfRschsBHzzZCp19Z55qAFhqUA"

#Shribot Keys
client_id = "aFZCZUlpMTB1WUVab3RiOEFtWlA6MTpjaQ"
client_secret = "mhagc2_3v8R-snUSo6xxKDgYnDZcLNnnitdcGkml5CIu1GJ4wi"
api_key = "cN4gu6OlUOfan080ShMPsRXiR"
api_secret = "0w08I5rL2375JRgXYQ0cIWj7M9PQsSvYBsiFftTHRBaeMqJGTz"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAF%2FdqwEAAAAA5gVe9UdrmlaSH6oDumUBUAJGaqk%3DmvRk8A86adWvN5WS90mwGS3T1GmtWDl2pN0zMBWPVrHmWly3qp"
access_token = "1723244241051058176-sFp9EFfZzNH9rmbKUO7rkoy8yZQvNH"
access_token_secret = "EGylv9SNrqswI5D0x3HO3Sl84jEnKz40eQ64m2BLCwcIq"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)