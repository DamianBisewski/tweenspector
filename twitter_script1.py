import tweepy
import os

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

userID = input("Podaj nazwę użytkownika: ")

tweets = api.user_timeline(screen_name=userID,
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )
num = input("Podaj liczbę tweetów: ")
for info in tweets[:int(num)]:
    print("ID: {}".format(info.id))
    print(info.created_at)
    print(info.full_text)
    print("\n")
