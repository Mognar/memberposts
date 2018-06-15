# coding: utf-8

# In[10]:


# In[11]:

#from flask import Flask
#app = Flask(__name__)


# In[12]:

import time,os


# In[13]:


# In[14]:

import json
import requests
from datetime import datetime
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
consumer_key = os.environ['CONKEY']
consumer_secret = os.environ['CONSEC']
access_token = os.environ['ACCKEY']
access_token_secret = os.environ['ACCSEC']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[15]:

#from pyslet.odata2.client import Client
#c = Client("http://data.parliament.uk/membersdataplatform/open/OData.svc")


# In[16]:

#import pyslet.odata2.core as core


# In[ ]:

#m=c.feeds['Members'].OpenCollection()


# In[ ]:

class ReplyToTweet(StreamListener):
    #@app.route("/")
    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == 854276747096973313
        #tweetText = tweet.get('text')
        not_reply = tweet.get('in_reply_to_status_id_str')
        
        
        if retweeted is not None and not retweeted and not from_self and not_reply is None:
            #tweet.text.encode('utf8')
            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            print tweetText 
            
            if "#" in tweetText:
                str2="#"
                y = str(tweetText[10:])
                print y
                z = y.rindex(str2)
                print z
                tm = str(y[:z])
                print tm
                tr = tm.strip(' ')
                words = tr.split()
                print words
                tr1 = words[0]
                tr2 = words[1]
                print tr1
                print tr2
            else:
                tm = str(tweetText[10:])
                print tm
                tr = tm.strip(' ')
                words = tr.split()
                print words
                tr1 = words[0]
                tr2 = words[1]
                print tr1
                print tr2
            
            
            
            stub='https://api.parliament.uk'.strip('/')
        

        
            if ("#govposts" in tweetText) and (not "#committees" in tweetText):
                url1='{}/odata/Person?$filter=endswith(PersonFamilyName,%27{}%27)%20and%20startswith(PersonGivenName,%27{}%27)'.format(stub,tr2,tr1)
                r=requests.get(url1)
                r1=r.json()
                r2=r1['value'][0]['LocalId']
                url2='https://api.parliament.uk/odata/Person(%27{}%27)/PersonHasIncumbency?$expand=IncumbencyHasPosition'.format(r2)
                r3=requests.get(url2)
                r4=r3.json()
                for i in r4['value']:
                    try:
                        d = datetime.strptime(i['IncumbencyStartDate'], "%Y-%m-%dT%H:%M:%SZ")
                        datum = d.strftime("%d/%m/%Y")
                        tw = i['IncumbencyHasPosition']['PositionName'] + ", started:" + datum

                    except TypeError:
                        pass

                                    #print('------')
                                    #api.update_status(repl + " " + tw + " " + tim)
                    replyText = str("@"+screenName + " " + tw)
                    print replyText
                    try:
                        api.update_status(status=replyText, in_reply_to_status_id = tweetId)
                    except tweepy.TweepError as e:
                        pass
            else:
                #tv = n[z]['DateOfWrit'].value
                #tw = str(tv)
                replyText = str("@"+screenName + " I'll need a hashtag to tell you more about " + tr1 + " #committees or #govposts")
                print replyText
                try:
                    api.update_status(status=replyText, in_reply_to_status_id = tweetId)
                except tweepy.TweepError as e:
                    pass
            #api.update_status(repl + " " + tw)
            #print(repl + " " + tw)

if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
