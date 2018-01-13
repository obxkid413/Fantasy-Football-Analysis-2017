
# coding: utf-8

# In[31]:


import pandas as pd
import bs4 as BeautifulSoup
import html5lib
import numpy as np


#append the data frames together into a single file





# In[ ]:

lst=[]
#only using top 300 players from each week*
for i in range(1,18):
    for j in range(0,300,50):
        url='http://games.espn.com/ffl/leaders?&scoringPeriodId=%s&seasonId=2017&startIndex=%d' % (i, j)
        lst.append(pd.read_html(url))


# In[21]:

frames=[]
for i in lst:
    i=(i[1])
    i=pd.DataFrame(i)
    frames.append(i)
    
df=pd.concat(frames)    


# In[22]:

df=df.rename(columns={df.columns[0]:'player', df.columns[6]: 'pass_yds', df.columns[7]: 'pass_td', df.columns[16]:'receiving_td', df.columns[23]:'points'})
df=df[['player', 'pass_yds', 'pass_td', 'receiving_td', 'points']]

#remove un-neeeded rows
clean_df=df.player!='PLAYER, TEAM POS'
clean_df=df.player!='OFFENSIVE PLAYERS'
df=df[clean_df]

#Now we have a clean data set.  Just need to add in the week identifier so we can look at stats by week.  The week changes every 300 rows.
df=df.reset_index(drop=True)

df.head(5)



# In[23]:

#We see we can drop the first row at index 0 because we have the appropriate headers now.
df.drop(0, inplace=True)
df.head(5)


# In[24]:

len(df)


# In[26]:

#Now I need to remove un-necessary rows
clean_df=df.player!='PLAYER, TEAM POS'
df=df[clean_df]


# In[27]:

clean_df=df.player!='OFFENSIVE PLAYERS'
df=df[clean_df]


# In[28]:

len(df)


# In[29]:

#Create the week index to do week by week analysis
df['week'] = df.index / 300 + 1
df.head(5)


# In[34]:

#Get every player's summary stats over the season
df.dtypes


# In[35]:

# In order to be able to aggregate and do what we want, we need to convert other columns to int64 data type
df[['pass_yds','pass_td', 'receiving_td', 'points', 'week']] = df[['pass_yds','pass_td', 'receiving_td', 'points', 'week']].apply(pd.to_numeric)


# In[36]:

df.dtypes


# In[37]:

#Get some summary stats for all players
summary=pd.pivot_table(df, index= 'player', values= "points", aggfunc=[np.sum, np.mean, np.median, min, max, np.std])
summary.head(5)


# In[41]:

#We can graph these results in Bokeh.  Here, I'm graphing a player's total against their median.  Suggestions on how to layout the graph are appreciated!  I couldn't figure out
# how to keep the other tools like wheel_zoom which would be really nice to have and the hover point tool the way it is implemented here.

from bokeh.models import *
from bokeh.plotting import figure, ColumnDataSource, output_notebook, show

source = ColumnDataSource(summary)

TOOLS="pan,wheel_zoom,box_zoom,reset,hover,previewsave"

#p = figure(title="Fantasy Football 2017 Performances", tools=TOOLS)

hover = HoverTool(tooltips=[('Name', '@player1')])

tools = [hover, WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool()]

p = figure(tools=[HoverTool(tooltips=[('Player', '@player'),
                                      ('Total', '@sum'),
                                      ('Average', '@median')])])

#p = figure(title="Fantasy Football 2017 Performances", tools=TOOLS)


#p = figure(title="Fantasy Football 2017 Performances", tools=TOOLS)

p.scatter(x='median', y='sum', size=8, source=source)

output_notebook()

show(p)




# In[ ]:



