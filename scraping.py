#!/usr/bin/env python
# coding: utf-8

#10.3.3
# Scrape Mars data:  The News
# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd 
import datetime as dt
import requests
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    # Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Call mars_news function to start browser and pull data
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": mars_hemi(browser),
      "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

    # Setup Splinter
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p        
    except AttributeError:
        return None, None
    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button  (button 1)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #print(img_url_rel)

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}' 
    print(img_url)

    return img_url
# ## Mars Facts

#10.3.5 - Send to Pandas
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        #df.head()
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemi(browser):
    # Visit the mars nasa news site
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    response = requests.get(url)
    hemi_soup = soup(response.text, 'html.parser')
    results = hemi_soup.find_all('div', class_='item')
    #print(len(results))

    # Iterate through each article
    for article in results:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        h3 = article.find('h3').text
        link = article.find('img')
        href = link['src']
        # Print the title and the full URL
        print('-----------')
        print(h3)
        full_url = f'{url}{href}'
        print(full_url)
        hemisphere_image_urls.append({'imge_url':full_url,'title':h3})
        #browser.back()

    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
