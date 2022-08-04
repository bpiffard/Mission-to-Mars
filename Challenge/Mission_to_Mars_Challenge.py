#!/usr/bin/env python
# coding: utf-8

# In[17]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[18]:


# Setting an executable path for Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Article titles and summaries

# In[ ]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[ ]:


# Creating html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[ ]:


slide_elem.find('div', class_='content_title')


# In[ ]:


# Using parent element to find th first 'a' tag and save it as news_title
news_title = slide_elem.find('div', class_='content_title').get_text()

news_title


# In[ ]:


# Using parent element to find summary text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

news_p


# ### Featured Images

# In[ ]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[ ]:


# Parse html of the new page w/ beautiful soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[ ]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[ ]:


# Adding base url to code 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[ ]:


df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

df


# In[ ]:


df.to_html()


# In[ ]:


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse html of the new page w/ beautiful soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Adding try/except block for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Adding base url to code 
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    except AttributeError:
        return None
    
    return img_url


# In[ ]:





# In[ ]:


def scrape_all():
    # Setting an executable path for Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Creating a dictionary that will hold the scraped data
    data = {
        "featured_image": featured_image(browser),
    }

    # Ending session
    browser.quit()

    return data

print(scrape_all())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# In[19]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[20]:


# 2. Create a list to hold the images and titles.
hemi_image_and_titles = []

# 3. Write code to retrieve the image urls and titles for each hemispheres
for x in range(4):
    hemispheres = {}
    full_hemi = browser.find_by_tag('h3')[x]
    full_hemi.click()
    
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    full_image = img_soup.find('img', class_='wide-image').get('src')
    img_url = f'{url}{full_image}'
    title = img_soup.find('h2', class_='title').get_text()
    
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    hemi_image_and_titles.append(hemispheres)
    browser.back()


# In[21]:


# 4. Print the list that holds the dictionary of each image url and title.
hemi_image_and_titles


# In[22]:


# 5. Quit the browser
browser.quit()

