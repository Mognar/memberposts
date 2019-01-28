
# coding: utf-8

# !pip install pdpy

# In[ ]:


import time,os


# In[23]:


import pdpy


# In[ ]:


import json
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
                firstname = words[0]
                surname = words[1]
                print firstname
                print surname
            else:
                tm = str(tweetText[10:])
                print tm
                tr = tm.strip(' ')
                words = tr.split()
                print words
                firstname = words[0]
                surname = words[1]
                print firstname
                print surname


# In[ ]:


if ("#govposts" in tweetText) and (not "#committees" in tweetText):


# In[83]:


querycom = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <https://id.parliament.uk/schema/>
SELECT ?committeename ?startdate ?enddate WHERE {
  ?member a :Member;
     :personGivenName '"""+firstname+"""';
     :personFamilyName '"""+surname+"""'.

  ?member
  :personHasFormalBodyMembership ?formalBody .

  ?formalBody
  :formalBodyMembershipHasFormalBody ?committee;
  :formalBodyMembershipStartDate ?startdate . 
  OPTIONAL { ?formalBody
  :formalBodyMembershipEndDate ?enddate } .

  ?committee 
  rdfs:label ?committeename .
} 
ORDER BY DESC(?startdate)
"""


# In[84]:


result = pdpy.sparql_select(querycom)
result


# In[85]:


result = result.fillna('Present')


# In[97]:


screenName = "gorman"


# In[101]:


replyText = str("@"+screenName + " " + firstname + " " + surname +": Member of "+row["committeename"]+" from "+str(row["startdate"])+" to "+str(row["enddate"]))
for index, row in result.iterrows():
    try:
        api.update_status(status=replyText, in_reply_to_status_id = tweetId)
    except tweepy.TweepError as e:
        pass


# In[ ]:


elif ("#committees" in tweetText) and (not "#govposts" in tweetText):


# In[93]:


querygov = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <https://id.parliament.uk/schema/>
SELECT DISTINCT ?positionName ?startdate ?enddate WHERE {
  ?member a :Member;
     :personGivenName '"""+firstname+"""';
     :personFamilyName '"""+surname+"""'.

  ?member 
    :memberHasParliamentaryIncumbency ?parlIncumbency
    .  

  ?member
    :governmentPersonHasGovernmentIncumbency ?govIncumbency
.

  ?govIncumbency :governmentIncumbencyHasGovernmentPosition/:name ?positionName;
  :incumbencyStartDate ?startdate . 
  OPTIONAL { ?govIncumbency
  :incumbencyEndDate ?enddate } .

} 
ORDER BY DESC(?startdate)
"""


# In[94]:


resultgov = pdpy.sparql_select(querygov)
resultgov


# In[ ]:


result = result.fillna('Present')


# In[ ]:


replyText = str("@"+screenName + " " + firstname + " " + surname +": "+row["postitionName"]+" from "+str(row["startdate"])+" to "+str(row["enddate"]))
for index, row in result.iterrows():
    try:
        api.update_status(status=replyText, in_reply_to_status_id = tweetId)
    except tweepy.TweepError as e:
        pass


# In[ ]:


else:
    #tv = n[z]['DateOfWrit'].value
    #tw = str(tv)
    replyText = str("@"+screenName + " I'll need a hashtag to tell you more about " + mem + " . #committees or #govposts")
    print replyText
    try:
        api.update_status(status=replyText, in_reply_to_status_id = tweetId)
    except tweepy.TweepError as e:
        pass


# In[ ]:


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
    #app.run()

