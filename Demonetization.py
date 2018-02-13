import re
import tweepy
from tweepy import OAuthHandler
import matplotlib.pyplot as plt
from textblob import TextBlob
 
class Demonetization(object):
    overall_score=0;
    total=0;
    graph=[0]*21;
    def authentication(self):
        

        key = '*************************'
        secret = '*******************************************'
        token = '*******************************************'
        token_secret = '*******************************************'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(key, secret)
            # set access token and secret
            self.auth.set_access_token(token, token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            #print("Place")
            print("Authentication Error")
    def plot_graph(self):
        base = [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        plt.plot(base, self.graph)
        plt.ylabel('no. of tweets')
        plt.xlabel('Analysis score')
        plt.show()
    def clean_tweet(self, tweet):
   
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def sentiment_analysis(self, tweet):
 
        # create TextBlob object of passed tweet text
        score = TextBlob(self.clean_tweet(tweet))
        #calculating overall score
        
        # set sentiment
        if score.sentiment.polarity > 0:
            return 'positive'
        elif score.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    def calculate_score(self,tweet):
        polar = TextBlob(self.clean_tweet(tweet))
        #calculating overall score
        
        # set sentiment
        if polar.sentiment.polarity > 0:
            c = polar.sentiment.polarity;
            c = c*10 + 10;
            #print int(c);
            self.graph[int(c)] = self.graph[int(c)] + 100;
            return ((polar.sentiment.polarity*0.5) + 0.5 )*100 
        elif polar.sentiment.polarity == 0:
            self.graph[11]+=1;
            return 50
        else:
            c = polar.sentiment.polarity;
            c = c*10 + 10;
            #print int(c);

            self.graph[int(c)] = self.graph[int(c)] + 100;
            return ((polar.sentiment.polarity)*50)
        
    def get_tweets(self, query, count = 1000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        
        try:
            # calling twitter api to fetch tweets
            all_tweets = self.api.search(q = query, count = count)
            
            # parsing tweets one by one
            for tweet in all_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.sentiment_analysis(tweet.text)
                self.total = self.total + 1;
                self.overall_score= self.overall_score + self.calculate_score(tweet.text);
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
    
    obj = Demonetization()
    obj.authentication()
    
    tweets = obj.get_tweets(query = 'Demonetization', count = 10000)
    print ("Overall Success of Demonetization =")
    print (obj.overall_score/obj.total)
    obj.plot_graph();
    #ptweets=[]
    # picking positive tweets from tweets
    # for tweet in tweets:
       # if tweet['sentiment'] == 'positive':
        #    ptweets.extend(tweet);
    positive = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    
    print("Percentage of Positive Tweets: {} %".format(100*len(positive)/len(tweets)))
    
    negative = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Percentage of Negative tweets: {} %".format(100*len(negative)/len(tweets)))
 
    #Printing First 10 Positive Tweets
    print("\n\nPositive tweets:")
    for tweet in positive[:10]:
        print(tweet['text'])
    
    #Printing First 10 negative Tweets.
    print("\n\nNegative tweets:")
    for tweet in negative[:10]:
        print(tweet['text'])
    
if __name__ == "__main__":
    main()
