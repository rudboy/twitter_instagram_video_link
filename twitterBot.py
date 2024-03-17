import tweepy

# Clés d'API Twitter
client_id = 'JvUiErvmZmaptWYLE75JNlZar'
client_secret = 'MmFiaRVuFwo8oCu9rtFonrGIhuP8kMZC6NsAhBFrZu94XutQMS'
access_token = '822495369460412416-I997Z0eyiVqa0J5wEgxmYlU6SbkqQzf'
access_token_secret = 'L7cK69yRjjGUeB41wiLJozp6CRgzMvVdClqy4QaIbHyeX'

# Fonction pour lancer l'écoute des tweets mentionnant votre compte
def ecouter_tweets_mentionnant():
    # Authentification avec Tweepy
    streaming_client = tweepy.StreamingClient("AAAAAAAAAAAAAAAAAAAAAI5NswEAAAAAfuVp4pe%2F2cY%2BcPSWIrJNlTBQfQ4%3DNA61YvcqnDogCOasvED5LNpt0uoUiFOLK1LiDrx5bnWdrgFG2m")
    streaming_client.add_rules(tweepy.StreamRule("ruddy"))
    streaming_client.filter()

    # streaming_client.filter(track=["Tweepy"])



if __name__ == "__main__":
    ecouter_tweets_mentionnant()
