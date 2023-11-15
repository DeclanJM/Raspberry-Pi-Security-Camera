from oauth2 import client, api

##Loads image into the api but does not post
def load_image(img_path):
    media_id = api.media_upload(filename = img_path).media_id_string
    return media_id

#Tweets text only
def tweet_text(text):
    client.create_tweet(text = text)
    print("Tweeted: " + text)

##Tweets text and an image
def tweet_text_and_media(text, media):
    media_id = load_image(media)
    client.create_tweet(text = text, media_ids = [media_id])
    print(f"Successfully Tweeted:\n\n{text}\n\nMedia ID:  {media_id}\n")

##Requires Basic API Account. Does not work with free version
##Tweets initial thread tweet and returns the ID
def start_thread(text): 
    tweet = api.update_status(status = text)
    print("Thread Successfully Started!")
    return tweet.id

##Requires Basic API Account. Does not work with free version
##Tweets out the text along with the image/s uploaded to the thread
def tweet_to_thread(thread_id, text, media): 
    media_id = load_image(media)
    client.create_tweet(text = text, media_ids = [media_id], in_reply_to_tweet_id = thread_id)