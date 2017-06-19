
# coding: utf-8

# In[1]:

get_ipython().system(u'pip install pyslet')


# In[2]:

import time


# In[3]:

get_ipython().system(u'pip install tweepy')


# In[4]:

import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
consumer_key = 'X1VdJN3XZE0qaoBjrAWTf0zBC'
consumer_secret = 'NMTltKlA2Rd0926YRNLII5bAHVExm9s1ZGLAqsfrLEphcHvCQM'
access_token = '854276747096973313-sKvvt5r0vPbFdpDmH6c81bxxvlULNcM'
access_token_secret = 'fvWM3NCtIiq0ox3qyFRqEyKdYtE1LlYFCYRY45wF16cQ6'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[5]:

from pyslet.odata2.client import Client
c = Client("http://data.parliament.uk/membersdataplatform/open/OData.svc")


# In[6]:

import pyslet.odata2.core as core


# In[ ]:

#m=c.feeds['Members'].OpenCollection()


# In[ ]:

class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == 854276747096973313

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            
            y = str(tweetText[17:])
            print y
            m=c.feeds['Members'].OpenCollection()
            ordering=core.CommonExpression.OrderByFromString("NameDisplayAs Desc")
            m.set_orderby(ordering)

            #Add in a filter "+y+"
            odfilter = core.CommonExpression.from_str("substringof('"+y+"',NameDisplayAs)")
            m.set_filter(odfilter)

            #View the response
            for p in m.itervalues():
                print(p.key(), p['NameDisplayAs'].value)
                mem = str(p['NameDisplayAs'].value)  
                print mem
                z = int(p.key())
                print z

                n=c.feeds['Members'].OpenCollection()
                mcm=n[z]['MemberGovernmentPosts'].OpenCollection()
                for k in mcm.keys():
                #Get the Government Post details
                    with mcm[k]['GovernmentPost'].OpenCollection() as mcmc:
                        for k2,v2 in mcmc[mcmc.keys()[0]].data_items():
                            #if k2=='NameDisplayAs' or k2=='HansardName' or k2=='StartDate':
                            if k2=='HansardName'or k2=='StartDate':
                                tw = str(v2.value)
                                print tw
                            #else: 
                                #tw = "No posts held"
                            #print(v2.value)

                    #print('------')
                    #api.update_status(repl + " " + tw + " " + tim)
                    replyText = str("@"+screenName + " " + mem + " " + tw)
                    print replyText
                    api.update_status(status=replyText, in_reply_to_status_id = tweetId)
                #api.update_status(repl + " " + tw)
                #print(repl + " " + tw)

if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')


# 
#     #for tweet in tweepy.Cursor(api.search,
#                                #q='@parldivisionbot').items(1):
#     #for tweet in tweepy.StreamListener():
#         #x = str(tweet.text)
#         #repl = str("@"+tweet.user.screen_name)
#         #tim = str(tweet.id)
#         #print x
#             y = str(tweetText[17:])
#             print y
#             ordering=core.CommonExpression.OrderByFromString("NameDisplayAs Desc")
#             m.set_orderby(ordering)
# 
#             #Add in a filter "+y+"
#             odfilter = core.CommonExpression.from_str("substringof('"+y+"',NameDisplayAs)")
#             m.set_filter(odfilter)
# 
#             #View the response
#             for p in m.itervalues():
#                 print(p.key(), p['NameDisplayAs'].value)
#                 z = int(p.key())
#                 print z
# 
#             n=c.feeds['Members'].OpenCollection()
#             mcm=n[z]['MemberGovernmentPosts'].OpenCollection()
#             for k in mcm.keys():
#                 #Get the Committee details
#                 with mcm[k]['GovernmentPost'].OpenCollection() as mcmc:
#                     for k2,v2 in mcmc[mcmc.keys()[0]].data_items():
#                         #if k2=='NameDisplayAs' or k2=='HansardName' or k2=='StartDate':
#                         if k2=='HansardName':
#                             #or v2.value is None:
#                             tw = str(v2.value)
#                         else: 
#                             tw = "No posts held"
#                         print(v2.value)
#                 #print('------')
#             try:
#                 #api.update_status(repl + " " + tw + " " + tim)
#                 api.update_status(repl + " " + tw, in_reply_to_status_id = tim)
#             except tweepy.error.TweepError:
#                 pass
#             #api.update_status(repl + " " + tw)
#             #print(repl + " " + tw)
# 
# if __name__ == '__main__':
#     streamListener = ReplyToTweet()
#     twitterStream = Stream(auth, streamListener)
#     twitterStream.userstream(_with='user')
#         

#     y = str(x[17:])
#     print y
#     ordering=core.CommonExpression.OrderByFromString("NameDisplayAs Desc")
#     m.set_orderby(ordering)
# 
#     #Add in a filter "+y+"
#     odfilter = core.CommonExpression.from_str("substringof('"+y+"',NameDisplayAs)")
#     m.set_filter(odfilter)
# 
#     #View the response
#     for p in m.itervalues():
#         print(p.key(), p['NameDisplayAs'].value)
#         z = int(p.key())
#         print z

#     n=c.feeds['Members'].OpenCollection()
#     mcm=n[z]['MemberGovernmentPosts'].OpenCollection()
#     for k in mcm.keys():
#         #Get the Committee details
#         with mcm[k]['GovernmentPost'].OpenCollection() as mcmc:
#             for k2,v2 in mcmc[mcmc.keys()[0]].data_items():
#                 #if k2=='NameDisplayAs' or k2=='HansardName' or k2=='StartDate':
#                 if k2=='HansardName':
#                     #or v2.value is None:
#                     tw = str(v2.value)
#                     print(v2.value)
#         #print('------')

# #api.update_status(repl + " " + tw)
# print(repl + " " + tw)
