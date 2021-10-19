#!/usr/bin/env python
# coding: utf-8

# In[24]:


# Import tweepy to work with the twitter API
import tweepy as tw

# Import numpy and pandas to work with dataframes
import numpy as np
import pandas as pd

# Import seaborn and matplotlib for viz
from matplotlib import pyplot as plt


# In[25]:


consumer_key = 'AUJgJP4AUOSQ2kxEn0fGJJVtQ'
consumer_secret = 'quLdAlGihzGRfI69eUztsEBdJg2pFl3OYM7xpsvQixEOamtSDh'
access_token = '2261179994-PCS6zNCGrnoz4qq3vcne4nU0gUNv3s8DgleeSfT'
access_token_secret = 'FnSB6L5IkTPrv24XbUhysSQCmPvHWoRZt7zTSBpA8ZweP'


# In[26]:



# Authenticate
auth = tw.OAuthHandler(consumer_key, consumer_secret)
# Set Tokens
auth.set_access_token(access_token, access_token_secret)
# Instantiate API
api = tw.API(auth, wait_on_rate_limit=True)


# In[27]:


hashtag = "#MUNLIV"
query = tw.Cursor(api.search_tweets, q=hashtag).items(1000)
tweets = [{'Tweet':tweet.text, 'Timestamp':tweet.created_at} for tweet in query]
print(tweets)


# In[28]:


df = pd.DataFrame.from_dict(tweets)
df.head()


# In[29]:


MUN_handle = ['ManchesterUnited', 'Manchester United', 'Manchester United FC' 'Manchester', 'United']
LIV_handle = ['Liverpool', 'Pool', 'Liverpool FC']


# In[30]:


def identify_subject(tweet, refs):
    flag = 0 
    for ref in refs:
        if tweet.find(ref) != -1:
            flag = 1
    return flag

df['MUN'] = df['Tweet'].apply(lambda x: identify_subject(x, MUN_handle)) 
df['LIV'] = df['Tweet'].apply(lambda x: identify_subject(x, LIV_handle))
df.head(10)


# In[31]:


# Import stopwords
import nltk
from nltk.corpus import stopwords

# Import textblob
from textblob import Word, TextBlob


# In[33]:


nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')
custom_stopwords = ['RT', '#MUNLIV']


# In[34]:


def preprocess_tweets(tweet, custom_stopwords):
    processed_tweet = tweet
    processed_tweet.replace('[^\w\s]', '')
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in stop_words)
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in custom_stopwords)
    processed_tweet = " ".join(Word(word).lemmatize() for word in processed_tweet.split())
    return(processed_tweet)

df['Processed Tweet'] = df['Tweet'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
df.head()


# In[35]:


print('Base review\n', df['Tweet'][0])
print('\n------------------------------------\n')
print('Cleaned and lemmatized review\n', df['Processed Tweet'][0])


# In[36]:


# Calculate polarity
df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])
df[['Processed Tweet', 'MUN', 'LIV', 'polarity', 'subjectivity']].head()


# In[37]:


display(df[df['MUN']==1][['MUN','polarity','subjectivity']].groupby('MUN').agg([np.mean, np.max, np.min, np.median]))
df[df['LIV']==1][['LIV','polarity','subjectivity']].groupby('LIV').agg([np.mean, np.max, np.min, np.median])


# In[42]:


LIV = df[df['LIV']==1][['Timestamp', 'polarity']]
LIV = LIV.sort_values(by='Timestamp', ascending=True)
LIV ['MA Polarity'] = LIV.polarity.rolling(10, min_periods=3).mean()

MUN = df[df['MUN']==1][['Timestamp', 'polarity']]
MUN = MUN.sort_values(by='Timestamp', ascending=True)
MUN['MA Polarity'] = MUN.polarity.rolling(10, min_periods=3).mean()


# In[43]:


MUN.head()


# In[45]:


repub = 'red'
demo = 'blue'
fig, axes = plt.subplots(2, 1, figsize=(13, 10))

axes[0].plot(LIV['Timestamp'], LIV['MA Polarity'])
axes[0].set_title("\n".join(["LIV Polarity"]))
axes[1].plot(MUN['Timestamp'], MUN['MA Polarity'], color='red')
axes[1].set_title("\n".join(["MUN Polarity"]))

fig.suptitle("\n".join(["United VS Liverpool"]), y=0.98)

plt.show()


# In[ ]:




