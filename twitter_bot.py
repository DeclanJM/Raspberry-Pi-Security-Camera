from oauth2 import client, api

def tweet_text(text):
    client.create_tweet(text = text)
    print("Tweeted Text!")

def upload_image(img_name):     ##Loads image into the api, does NOT post to twitter
    img_path = "images/" + img_name
    print(img_path)
    media_id = api.media_upload(filename = img_path).media_id_string
    print("Media ID: " + media_id)
    return media_id

def tweet(text, media):         ##Tweets out the text along with the image/s uploaded
    media_id = upload_image(media)
    client.create_tweet(text = text, media_ids = [media_id])
    print("Tweet Successfully Tweeted!")

def test(text, media_addr):
    tweet(text, media_addr)
    print("Test Successful!")

if __name__ == "__main__":
    text = input("Enter text to tweet:  ")
    media = input("Enter the name of the image you would like to upload:  ")

    tweet(text, media)

