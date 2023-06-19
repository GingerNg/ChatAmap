import tweepy

# Sample code for the Twitter API v2 endpoints
# https://github.com/twitterdev/Twitter-API-v2-sample-code

# Set up authentication credentials
# consumer_key = '*'
# consumer_secret = '*'
# access_token = '*-*'
# access_token_secret = '*'

# import requests

# bearer_token = "*"

# response = requests.get(
#     f"https://api.twitter.com/2/users/by/JourneymanChina/twitter",
#     headers={"Authorization": f"Bearer {bearer_token}"}
# )

# if response.status_code != 200:
#     raise Exception(f"Failed to retrieve user information: {response.status_code}")

# print(response.json())


import tweepy
import os

class Main:
    def fetch_tweets(self):
        # consumer_key = os.environ.get('API_KEY')
        # consumer_secret = os.environ.get('API_SECRET')
        # access_token = os.environ.get('ACCESS_TOKEN')
        # access_token_secret = os.environ.get('SECRET_ACCESS_TOKEN')

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        print('Successfully Authenticated')


        # Fetch Tweets
        public_tweets = api.get_favorites()

        # Print Tweets
        for tweet in public_tweets:
            print(tweet.text)
            print("")
            print('##########################')
            print("")

main = Main()
main.fetch_tweets()