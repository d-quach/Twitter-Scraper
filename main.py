"""A Twitter Data miner using the Tweepy API"""
import keys
import tweepy  # pip install tweepy
from textblob import TextBlob  # pip install -U textblob
import pandas as pd  # pip install pandas
import numpy as np  # pip install numpy
import preprocessor as p  # pip install tweet-preprocessor


class Authenticator:
    """A class for proving credentials to access the Twitter API"""
    @staticmethod
    def authenticate_session():
        try:
            authentication = tweepy.OAuthHandler(keys.keys_dictionary['consumer_key'],
                                                 keys.keys_dictionary['consumer_secret'])
            authentication.set_access_token(keys.keys_dictionary['access_token'],
                                            keys.keys_dictionary['access_token_secret'])
            return authentication
        except Exception:
            print("There has been an issue with verification.")


class TwitterClient:
    """A class that contains functionality for searching tweets and an accounts tweets"""
    def __init__(self):
        self.authenticated = Authenticator.authenticate_session()
        self.clientAPI = tweepy.API(self.authenticated, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def display_menu(self):
        """Displays menu options and loops until exit"""
        user_input = None
        valid_inputs = np.array(['1', '2', '3', 'q'])

        while user_input != 'q':

            print('***************  Twitter Miner  ***************')
            print(
                f'{"****  Option":<16}{"Action    ****":>31}\n{"*" * 47}\n{"*" * 4:<11}1'
                f'{"Search Recent Tweets  ***":>35}\n'
                f'{"*" * 4: <11}2{"Account Analytics  ***":>35}\n'
                f'{"*" * 4: <11}3{"Search For a User  ***":>35}\n'
                f'{"*" * 4: <11}q{" Quit  ***":>35}\n'
                
                f'{"*" * 47}\n')

            user_input = input('Enter an Option: ')

            if user_input not in valid_inputs:
                print('\nPlease Enter a Valid Option\n')

            elif user_input == '1':
                search_string = input('Enter Your Search: ')
                tweets = self.search_recent_tweets(search_string)
                self.print_searched_tweets(tweets)

            elif user_input == '2':
                get_account = input('Which Account Needs to Be Analyzed? ')
                amount = int(input('Specify the Number of Tweets to Sample: '))

                df = self.get_user_tweets(get_account, amount)
                self.tweet_performance(df)

            elif user_input == '3':
                search_user = input('Which Twitter User Would You Like to Look Up? ')
                twitter_user = self.get_user(search_user)
                self.print_user(twitter_user)

            elif user_input == 'q':
                print('Thank you, Have a Good Day.\n')
                break

    def search_recent_tweets(self, line):
        """Use the Twitter api to search for recent tweets"""
        try:
            searched_tweets = np.array(self.clientAPI.search(q=line, count=20, tweet_mode='extended'))
            return searched_tweets
        except Exception:
            print("There Has Been an Error in the Search.")

    @staticmethod
    def print_searched_tweets(tweets):
        """Print information about searched tweets"""
        try:
            p.set_options(p.OPT.URL, p.OPT.RESERVED)

            for tweet in tweets:
                print(f'\nUsername: {tweet.user.screen_name}')
                print(f'Name: {tweet.user.name}')

                if 'en' in tweet.lang:
                    try:
                        tweet_text = tweet.retweeted_status.full_text
                        print(f'Tweet Body: {p.clean(tweet_text)}')
                    except AttributeError:
                        print(f'Tweet Body: {p.clean(tweet.full_text)}')
                else:
                    try:
                        tweet_text = tweet.retweeted_status.full_text
                        cleaned = p.clean(tweet_text)
                        print(f'English Translation: {TextBlob(cleaned).translate()}')
                    except AttributeError:
                        tweet_text = tweet.full_text
                        cleaned = p.clean(tweet_text)
                        print(f'English Translation: {TextBlob(cleaned).translate()}')

                print(f'Date: {tweet.created_at}')

                if tweet.user.location is not None:
                    print(f'Location: {tweet.user.location}')

                try:
                    print(f'Like Count: {tweet.retweeted_status.favorite_count}')
                    print(f'Retweet Count: {tweet.retweeted_status.retweet_count}\n')
                except AttributeError:
                    print(f'Like Count: {tweet.favorite_count}')
                    print(f'Retweet Count: {tweet.retweet_count}\n')
        except Exception:
            print("There Has Been an Error in the Search.\n")

    def get_user_tweets(self, account, amount):
        """Get the tweets from a user's timeline"""
        try:
            account_tweets = self.clientAPI.user_timeline(screen_name=account, count=amount, include_rts='false')

            tweet_dictionary = {}
            tweet_counter = 1

            for tweet in account_tweets:
                t_key = "Tweet" + str(tweet_counter)
                tweet_counter += 1

                tweet_dictionary[t_key] = [tweet.user.screen_name, tweet.text, tweet.favorite_count,
                                           tweet.retweet_count]

            tweet_df = pd.DataFrame(tweet_dictionary)
            tweet_df.index = ['Screen Name', 'Tweet', 'Like Count', 'Retweet Count']
            return tweet_df
        except Exception:
            print("There Has Been an Error in the Search.")

    @staticmethod
    def tweet_performance(df):
        """Access dataframe rows to perform statistical analysis"""
        try:
            print(f'\n--------  {df.iat[0, 0]}\'s Tweet Engagement  --------\n'
                  f'\n{"Tweets Returned: ":<32}{df.loc["Tweet"].count():>16.2f}'
                  f'\n\n{"Total Likes: ":<32}{df.loc["Like Count"].sum():>16.2f}'
                  f'\n{"Highest Number of Likes: ":<32}{df.loc["Like Count"].max():>16.2f}'
                  f'\n{"Lowest Number of Likes: ":<32}{df.loc["Like Count"].min():>16.2f}'
                  f'\n{"Average Number of Likes: ":<32}{df.loc["Like Count"].mean():>16.2f}'
                  f'\n{"Median Likes: ":<32}{df.loc["Like Count"].median():>16.2f}'
                  f'\n{"Standard Deviation of Likes: ":<32}{df.loc["Like Count"].std():>16.2f}'
                  f'\n{"Variance of Likes: ":<32}{df.loc["Like Count"].var():>16.2f}'
                  f'\n\n{"Total Retweets: ":<32}{df.loc["Retweet Count"].sum():>16.2f}'
                  f'\n{"Highest Number of Retweets: ":<32}{df.loc["Retweet Count"].max():>16.2f}'
                  f'\n{"Lowest Number of Retweets: ":<32}{df.loc["Retweet Count"].min():>16.2f}'
                  f'\n{"Average Number of Retweets: ":<32}{df.loc["Retweet Count"].mean():>16.2f}'
                  f'\n{"Median Retweets: ":<32}{df.loc["Retweet Count"].median():>16.2f}'
                  f'\n{"Standard Deviation of Retweets: ":<32}{df.loc["Retweet Count"].std():>16.2f}'
                  f'\n{"Variance of Retweets: ":<32}{df.loc["Retweet Count"].var():>16.2f}'
                  f'\n\n')
        except Exception:
            print("There has been an error in the search.")

    def get_user(self, search_user):
        """Get information about a twitter user"""
        try:
            twitter_user = self.clientAPI.get_user(search_user)
            return twitter_user
        except Exception:
            print("There Has Been an Error in the Search.")

    @staticmethod
    def print_user(found_user):
        print(f'\n'f'Screen Name: {found_user.screen_name}\n'
              f'Name: {found_user.name}\n'
              f'ID: {found_user.id}\n'
              f'Location: {found_user.location}\n'
              f'Date Created: {found_user.created_at}\n'
              f'Description: {found_user.description}\n'
              f'Is Verified? {found_user.verified}\n'
              f'Is This Account Protected? {found_user.protected}\n'
              f'URL: {found_user.url}\n\n')


if __name__ == '__main__':
    """Instantiate a TwitterClient object and call the display_menu method"""
    client = TwitterClient()
    client.display_menu()