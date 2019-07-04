from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 


def init_browser(): 
    
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)


query_mars = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        
        browser = init_browser()

       
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

       
        html = browser.html

       
        soup = BeautifulSoup(html, 'html.parser')


        
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

       
        query_mars['news_title'] = news_title
        query_mars['news_paragraph'] = news_p

        return query_mars

    finally:

        browser.quit()


def scrape_mars_image():

    try: 

        
        browser = init_browser()

        
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

    
        html_image = browser.html

        
        soup = BeautifulSoup(html_image, 'html.parser')

       
        image_urlft  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        
        mars_link = 'https://www.jpl.nasa.gov'

        
        image_urlft = mars_link + image_urlft

       
        image_urlft 

        # Dictionary entry from FEATURED IMAGE
        query_mars['image_urlft'] = image_urlft 
        
        return query_mars
    finally:

        browser.quit()

        
def scrape_mars_weather():

    try: 

        browser = init_browser()

    
        weather_link = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_link)

        html_weather = browser.html


        soup = BeautifulSoup(html_weather, 'html.parser')

       
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

    
        query_mars['weather_tweet'] = weather_tweet
        
        return query_mars
    finally:

        browser.quit()



def scrape_mars_facts():

    
    link_facts = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(link_facts)

   
    dfmars = mars_facts[0]

    dfmars.columns = ['Description','Value']

    dfmars.set_index('Description', inplace=True)

    data = dfmars.to_html()

    query_mars['mars_facts'] = data

    return query_mars

def scrape_mars_hemispheres():

    try: 

        
        browser = init_browser()

        
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html

        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        items = soup.find_all('div', class_='item')

         
        hemi_url= []

        hemispheres_mars_link = 'https://astrogeology.usgs.gov' 

        
        for i in items: 
            
            title = i.find('h3').text
            
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            browser.visit(hemispheres_mars_link + partial_img_url)
            
            partial_img_html = browser.html
             
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            img_url = hemispheres_mars_link + soup.find('img', class_='wide-image')['src']
            
            
            hemi_url.append({"title" : title, "img_url" : img_url})

        query_mars['hemi_url'] = hemi_url

        

        return query_mars
    finally:

        browser.quit()
