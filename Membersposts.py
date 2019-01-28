
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
user = api.me()
print (user.name)

# In[ ]:


class ReplyToTweet(StreamListener):
    #@app.route("/")
    def on_status(self, status):
        tweet = status.text
        print(tweet)
        id_str = status.id_str
        name = status.user.screen_name

        if "#" in tweet:
            firstname = ""
            surname = ""
            try:
                str2="#"
                y = str(tweet[10:])
                print(y)
                z = y.rindex(str2)
                print(z)
                tm = str(y[:z])
                print(tm)
                tr = tm.strip(' ')
                words = tr.split()
                print(words)
                firstname = words[0]
                surname = words[1]
                print(firstname)
                print(surname)
            except IndexError as i:
                pass
                
        else:
            firstname = ""
            surname = ""
            try:
                tm = str(tweet[10:])
                print(tm)
                tr = tm.strip(' ')
                words = tr.split()
                print(words)
                firstname = words[0]
                surname = words[1]
                print(firstname)
                print(surname)
            except IndexError as i:
                pass


# In[ ]:


        if ("#committees" in tweet) and (not "#govposts" in tweet):
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
            print(result)

            # In[85]:


            result = result.fillna('Present')


            # In[97]:




            # In[101]:



            for index, row in result.iterrows():
                replyText = str("@"+name + " " + firstname + " " + surname +": Member of "+row["committeename"]+" from "+str(row["startdate"])+" to "+str(row["enddate"]))
                try:
                    api.update_status(status=replyText, in_reply_to_status_id = id_str)
                except tweepy.TweepError as e:
                    pass


        # In[ ]:


        elif ("#govposts" in tweet) and (not "#committees" in tweet):


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


            resultgov = resultgov.fillna('Present')


            # In[ ]:



            for index, row in resultgov.iterrows():
                replyText = str("@"+name + " " + firstname + " " + surname +": "+row["postitionName"]+" from "+str(row["startdate"])+" to "+str(row["enddate"]))
                try:
                    api.update_status(status=replyText, in_reply_to_status_id = id_str)
                except tweepy.TweepError as e:
                    pass


        # In[ ]:


        else:
            #tv = n[z]['DateOfWrit'].value
            #tw = str(tv)
            replyText = str("@"+name + " I'll need a hashtag to tell you more about " + mem + " . #committees or #govposts")
            print(replyText)
            try:
                api.update_status(status=replyText, in_reply_to_status_id = id_str)
            except tweepy.TweepError as e:
                pass
    def on_error(self, status_code):
        if status_code == 420:
            return False

# In[ ]:


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener)
    stream.filter(track=["@parlibot", "@Parlibot"])
    #app.run()

