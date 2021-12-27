import twint
import os

search_terms = input("Podaj nazwę użytkownika: ")
file = search_terms + '_tweets.csv'
if(os.path.exists(file) and os.path.isfile(file)):
    os.remove(file)
c = twint.Config()
c.Username = search_terms
c.Store_csv = True
c.Retweets = True
c.Profile_full = True
c.Output = search_terms + '_tweets.csv'

# Run
twint.run.Profile(c)
