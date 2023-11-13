from oauth2 import client, api

def tweet_text(text):
    client.create_tweet(text = text)
    print("Tweeted Text!")

def upload_image(img_name):     ##Loads image into the api, does NOT post to twitter
    img_path = img_name
    print("Media Path: " + img_path)
    media_id = api.media_upload(filename = img_path).media_id_string
    print("Media ID: " + media_id)
    return media_id

def tweet(text, media):
    media_id = upload_image(media)
    client.create_tweet(text = text, media_ids = [media_id])
    print("Successfully Tweeted!")

def start_thread(text):    ##Tweets initial thread tweet and returns the ID
    tweet_text = "Starting Thread!"
    tweet = api.update_status(status = tweet_text)
    print("Thread Successfully Started!")
    return tweet.id

def tweet_to_thread(thread_id, text, media): ##Tweets out the text along with the image/s uploaded to the thread
    media_id = upload_image(media)
    client.create_tweet(text = text, media_ids = [media_id], in_reply_to_tweet_id = thread_id)


if __name__ == "__main__":
    text = input("Enter text to tweet:  ")
    media = input("Enter the name of the image you would like to upload:  ")

    tweet(text, media)