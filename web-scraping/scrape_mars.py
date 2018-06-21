# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo


# create instance of Flask app
app = Flask(__name__)

# dictionary to hold all scraped data
data = { } 

# mongo 
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.scrape


@app.route("/scrape")
def scrape():

    # coding: utf-8

    # # Step 1 

    # ## NASA Mars News

    # dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    import time



    # In[17]:


    url = 'https://mars.nasa.gov/news/'


    # In[18]:


    # initialize chrome driver
    executable_path = { 'executable_path': "C:\\Windows\\chromedriver" }
    browser = Browser('chrome', **executable_path, headless=True )


    # In[21]:


    # make request to page
    browser.visit(url)


    # In[22]:


    # wait for page to finish loading, sleep for 5 seconds
    time.sleep(5)


    # In[23]:


    # get page html
    html = browser.html


    # In[24]:


    # create BeautifulSoup object
    soup = BeautifulSoup( html, 'html.parser')


    # In[25]:


    news_title = soup.find(class_='content_title').text
    data['news_title'] = news_title


    # In[26]:


    news_p = soup.find(class_='article_teaser_body').text
    data['news_p'] = news_p


    # ## JPL Mars Space Images - Featured Image

    # In[29]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # In[31]:


    # visit page
    browser.visit(url)


    # In[32]:
    time.sleep(5)

    # click on button with text `FULL IMAGE`
    browser.click_link_by_partial_text('FULL IMAGE')


    # In[33]:
    time.sleep(5)

    # click on button with text `more info`
    browser.click_link_by_partial_text('more info')


    # In[34]:
    time.sleep(5)

    # get page html and create BeautifulSoup object
    html = browser.html
    soup = BeautifulSoup( html, "html.parser")


    # In[35]:


    # get featured image link
    image = soup.find(class_='lede').find('img')['src']
    image


    # In[36]:


    # add url to get full image url 
    featured_image_url = 'https://www.jpl.nasa.gov/' + image
    data['featured_image_url'] = featured_image_url



    # ## Mars Weather

    # In[18]:


    # dependencies
    import tweepy
    import os
    from config import (consumer_key, 
                        consumer_secret, 
                        access_token, 
                        access_token_secret)


    # In[19]:


    twitter_url = 'http://space-facts.com/mars/'


    # In[21]:


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = api.user_timeline('marswxreport')
    mars_weather = tweets[0].text
    data['mars_weather'] = mars_weather 

    # ## Mars Facts

    # In[22]:


    # dependency
    import pandas as pd


    # In[23]:


    url = 'https://space-facts.com/mars/'


    # In[35]:


    table = pd.read_html(url)
    table


    # In[40]:


    df = table[0]
    df


    # In[42]:


    df.columns = ['description', 'value']
    df


    # In[43]:


    # drop first row and set index to `description`

    df.set_index('description', inplace=True)
    df.head()


    # In[46]:


    # convert to html string
    table_html = df.to_html()
    data['table_html'] = table_html



    # ## Mars Hemispheres

    # In[122]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[70]:


    # initialize chrome driver
    executable_path = { 'executable_path': "C:\\Windows\\chromedriver" }
    browser = Browser('chrome', **executable_path, headless=True )


    # In[123]:


    # visit url 
    browser.visit(url)


    # In[107]:


    # wait for page to load
    time.sleep(5)


    # In[124]:


    # get page html and create BeautifulSoup object
    html = browser.html
    soup = BeautifulSoup( html, "html.parser")


    # In[127]:


    # get link and title for each hemisphere
    links = soup.find_all(class_='description')

    hemisphere_image_urls = []

    for i in links:
        
        # get url 
        href = i.find('a')['href']
        
        # visit page 
        browser.visit('https://astrogeology.usgs.gov' + href )
        
        # get html 
        page_html = browser.html
        
        # create BeautifulSoup object
        page_soup = BeautifulSoup( page_html, "html.parser")
        
        # get title and image url 
        title = page_soup.find(class_='title').text
        
        img_url = page_soup.find(class_='downloads').find('a')['href']
        
        hemisphere_image_urls.append( { "title": title, "img_url": img_url  } )
        
        
    data['hemisphere_image_urls'] = hemisphere_image_urls
    print( data )

    # store data in mongo 
    db.scrape.insert({ "data": data })

    # loading..
    return '<h1>Scraping done! Now go <a href="/">Home</a> to see the data</h1>'


@app.route("/")
def home():
   data = db.scrape.find().limit(1)
   print( type(data) )
   return render_template("index.html", data=data)

if __name__ == "__main__":
   app.run(debug=True)
