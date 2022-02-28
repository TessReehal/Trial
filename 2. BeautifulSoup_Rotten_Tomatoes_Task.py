Is it working?


#!/usr/bin/env python
# coding: utf-8

# #  Web scraping a Rotten Tomatoes page

# ## Import the relevant libraries

# This exercise is going to use web scraping techniques to extract data and store in a data frame using Pandas. The data that will needed to be included in the data frame will be as follows:
# - Title
# - Year
# - Score
# - Adjusted score
# - Director
# - Cast
# 
# As an exension task, then the following can be added also:
# 
#  - consensus
#  - synopsis
#  
# There will be placeholder headers and some notes to assist you but feel free to delete any of that and work in your own way on this. The completed data frame should be exported as a CSV at the end of the activity. You will need to use the pandas documentation to help with this.
# https://pandas.pydata.org/docs/
# 

# In[1]:


# load packages
import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[2]:


# Define the URL of the site
base_site = 'https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now'


# ## Check to see if the request was successful

# In[3]:


# sending a request to the webpage
response = requests.get(base_site)
response.status_code


# In[7]:


# get the HTML from the webpage
html = response.content


# ## Choosing a parser

# In[8]:


# convert the HTML to a BeatifulSoup object
html_soup = BeautifulSoup(html, 'lxml')


# In[9]:


# Exporting the HTML to a file
with open('Rotten_tomatoes_page2LXML_Parser.html', 'wb') as file:
    file.write(html_soup.prettify('utf-8'))


# ### Re: Parser choice

# In[11]:


# Beautiful Soup ranks the lxml parser as the best one.

# If a parser is not explicitly stated in the Beautiful Soup constructor,
# the best one available on the current machine is chosen.

# This means that the same piece of code can give different results on different computers.


# ## Finding an element containing all the data

# In[36]:


# Right click on the webpage and choose INSPECT to find out the divs of the part of the page that you would like to scrape.
# 
#Find all div tags on the webpage containing the information we want to scrape
divs = html_soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
divs


# # Extracting the title, year and score of each movie

# In[13]:


# The title, year and score of each movie are contained in the 'h2' tags


# In[11]:


# choose the first film to get a better idea of how the data is structured - use list indexing to achieve this.
divs[0].find('h2')


# In[12]:


# Extracting all 'h2' tags
headings = [div.find('h2') for div in divs]
headings


# In[13]:


[heading.text for heading in headings]
# The movie title is in the 'a' tag
# The year is in a 'span' with class 'start-year'
# The score is in a 'span' with class 'tMeterScore'


# ## Title

# In[14]:


[heading.find('a') for heading in headings]


# In[15]:


# Obtaining the movie titles from the links
movie_names = [heading.find('a').string for heading in headings]
movie_names


# ## Year

# In[17]:


# Filtering only the spans containing the year
[heading.find('span', class_ = 'start-year') for heading in headings]


# In[18]:


# Extracting the year string
years = [heading.find('span', class_ = 'start-year').string for heading in headings]
years


# ### Removing the brackets

# In[26]:


# Use the strip method to remove the parantheses


# In[20]:


# code for removing parantheses - use the strip method 
years[0].strip('()')


# In[22]:


# Updating years with stripped values
# Create a list of all the years 
years = [year.strip('()') for year in years]
years


# In[23]:


# Converting all the strings to integers - use list comprehension to achieve this
years = [int(year) for year in years]
years


# ## Score

# In[27]:


# Extracting the score string
scores = [heading.find('span', class_ = 'tMeterScore').string for heading in headings]
scores


# In[28]:


# Converting all the strings to integers
scores = [score.strip('%') for score in scores]
scores


# In[29]:


# Converting each score to an integer
scores = [int(score) for score in scores]
scores


# # Extracting the rest of the information

# ## Critics Consensus

# In[30]:


# The critics consensus is located inside a 'div' tag with the class 'info critics-consensus'
# This can be found inside the original 'div's we scraped
divs


# In[37]:


consensus = [div.find("div", {"class": "info critics-consensus"}) for div in divs]
consensus


# In[39]:


consensus[0].contents


# In[42]:


consensus_text = [c.contents[1].strip() for c in consensus]
consensus_text


# ### Way #2: Inspecting the HTML

# In[50]:


# When inspecting the HTML we see that the common phrase ("Critics Consensus: ")
# is located inside a span element
# The string we want to obtain follows that


# In[19]:


# We can use .contents to obtain a list of all children of the tag


# In[20]:


# The second element of that list is the text we want


# In[21]:


# We can remove the extra whitespace (space at the beginning) with the .strip() method


# ## Directors

# In[55]:


# Extracting all director divs
director = [div.find("div", {"class": "info director"}) for div in divs]
director


# In[56]:


director[0]


# In[59]:


[d.find('a').string for d in directors]


# In[61]:


final_directors = [None if d.find("a") is None else d.find("a").string for d in director]
final_directors


# ## Cast info

# In[76]:


# Each cast member's name is the string of a link
# There are multiple cast members for a movie
cast = [div.find("div", {"class": "info cast"}) for div in divs]
cast


# In[77]:


cast[0]


# In[79]:


list_1 = cast[0].find_all('a')
list_1


# In[80]:


list_1 = [l.string for l in list_1]
list_1


# In[ ]:





# In[72]:


[c.find('a') for c in cast]

# Obtain all the links to different cast members


# In[68]:


# Extract the names from the links
[c.find('a').string for c in cast]


# In[24]:


# OPTIONALLY: We can stitch all names together as one string

# This can be done using the join method
# To use join, pick a string to use as a separator (in our case a comma, followed with a space) and
# pass the list of strings you want to merge to the join method

#cast = ", ".join(cast_names)
#cast


# In[68]:


# Now we need to do the above operations for every movie


# ### Using a for loop

# In[81]:


# Initialize the list of all cast memners
casting = []



# Just put all previous operations inside a for loop
for c in cast:
    cast_links = c.find_all('a')
    cast_names = [link.string for link in cast_links]

    casting.append(", ".join(cast_names)) # Joining is optional



casting


# ## Synopsis

# In[82]:


divs


# In[83]:


synopsis = [div.find("div", {"class": "info synopsis"}) for div in divs]
synopsis


# In[84]:


synopsis[0]


# In[85]:


synopsis_text = [s.contents[1] for s in synopsis]
synopsis_text


# In[ ]:





# In[ ]:





# # Representing the data in structured form

# ## Creating a Data Frame

# In[86]:


movie_review = pd.DataFrame()
movie_review


# ## Populating the dataframe

# In[87]:


# Populating the dataframe

movie_review['Movie Title'] = movie_names
movie_review['Year'] = years
movie_review['Scores'] = scores
movie_review['Critics'] = consensus_text
movie_review['Directors'] = final_directors
movie_review['Cast'] = casting
movie_review['Synopsis'] = synopsis_text

movie_review


# In[88]:


pd.set_option('display.max_colwidth', -1)
movie_review


# ## Exporting the data to CSV (comma-separated values) and excel files

# In[89]:


# Write data to excel file
movie_review.to_excel('movie_review.xlsx', index = False, header = True)


# In[90]:


# or write data to CSV file
movie_review.to_csv('movie_review.csv', index = False, header = True)


# In[87]:


# Index is set to False so that the index (0,1,2...) of each movie is not saved to the file (the index is purely internal)
# The header is set to True, so that the names of the columns are saved


Hi Tess 
