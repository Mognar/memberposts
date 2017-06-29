
# coding: utf-8

# In[49]:

get_ipython().system(u'pip install pyslet')


# In[50]:

import time


# In[51]:

get_ipython().system(u'pip install tweepy')


# In[52]:

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


# In[53]:

from pyslet.odata2.client import Client
c = Client("http://data.parliament.uk/membersdataplatform/open/OData.svc")


# In[54]:

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
            
            
            
            m=c.feeds['Members'].OpenCollection()
            ordering=core.CommonExpression.OrderByFromString("NameDisplayAs Desc")
            m.set_orderby(ordering)

            odfilter = core.CommonExpression.from_str("startswith('"+tr1+"',Forename) and startswith('"+tr2+"',Surname)")
            m.set_filter(odfilter)

            for p in m.itervalues():
                print(p.key(), p['NameDisplayAs'].value)
                mem = str(p['NameDisplayAs'].value)  
                print mem
                z = int(p.key())
                print z

                n=c.feeds['Members'].OpenCollection()
                if ("#govposts" in tweetText) and (not "#committees" in tweetText):
                    mcm=n[z]['MemberGovernmentPosts'].OpenCollection()
                    for k in mcm.keys():
                    #Get the Government Post details
                        with mcm[k]['GovernmentPost'].OpenCollection() as mcmc:
                            for k2,v2 in mcmc[mcmc.keys()[0]].data_items():
                                if k2=='Name':
                                #if k2=='HansardName' :
                                    tw = str(v2.value)
                                    print tw
                                #print(v2.value)

                                #print('------')
                                #api.update_status(repl + " " + tw + " " + tim)
                            replyText = str("@"+screenName + " " + mem + " " + tw)
                            print replyText
                            try:
                                api.update_status(status=replyText, in_reply_to_status_id = tweetId)
                            except tweepy.TweepError as e:
                                pass
                elif ("#committees" in tweetText) and (not "#govposts" in tweetText):
                    mcm=n[z]['MemberCommittees'].OpenCollection()
                    for k in mcm.keys():
                    #Get the Government Post details
                        with mcm[k]['Committee'].OpenCollection() as mcmc:
                            for k2,v2 in mcmc[mcmc.keys()[0]].data_items():
                                if k2=='Name':
                                #if k2=='HansardName' :
                                    tw = str(v2.value)
                                    print tw
                                #print(v2.value)

                                #print('------')
                                #api.update_status(repl + " " + tw + " " + tim)
                            replyText = str("@"+screenName + " " + mem + " " + tw)
                            print replyText
                            try:
                                api.update_status(status=replyText, in_reply_to_status_id = tweetId)
                            except tweepy.TweepError as e:
                                pass
                else:
                    #tv = n[z]['DateOfWrit'].value
                    #tw = str(tv)
                    replyText = str("@"+screenName + " I'll need a hashtag to tell you more about " + mem)
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