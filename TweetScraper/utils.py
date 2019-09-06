import os

def mkdirs(dirs):
    ''' Create `dirs` if not exist. '''
    if not os.path.exists(dirs):
        os.makedirs(dirs)

import tweepy


def twitter_auth():
    CONSUMER_KEY = "mjuoCpYhKAyInosFQbVdHMjrG"
    CONSUMER_SECRET = "Yq7PfP8Vy48JehXXjLNcNqekjVVDnpGTQStx7jTB89aHH7tGWN"
    OAUTH_TOKEN = "2354306079-sDY74vrY2tIsO5B4lIgbGKni1y3UFYPuE7kGW3E"
    OAUTH_TOKEN_SECRET = "xJQGZipFJRU7yi0wAGsfo1TvrUaTp1TQklwveOqUDd6EY"

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return auth


def create_api():
    auth = twitter_auth()
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True,
                     )
    return api