# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Setting an executable path for Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Defining variables as return from mars_news function
    news_title, news_p = mars_news(browser)

    # Creating a dictionary that will hold the scraped data
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemi_images(browser)
    }

    # Ending session
    browser.quit()

    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Creating html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Adding try/except block for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Using parent element to find th first 'a' tag and save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Using parent element to find summary text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

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

# ### Mars Facts

def mars_facts():
    try:
        # Converting table found on the web to a pandas df
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Converting dataframe back to html
    return df.to_html() 

## Hemisphere images
def hemi_images(browser):
    # visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Creating list to hold data
    hemi_image_and_titles = []
    for x in range(4):
        # Creating dictionary to hold imag url and title
        hemispheres = {}

        # Navigating to the page with the full-res image
        full_hemi = browser.find_by_tag('h3')[x]
        full_hemi.click()
        
        # Parsing the html
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # Extracting the image-url and title and holding as variables
        full_image = img_soup.find('img', class_='wide-image').get('src')
        img_url = f'{url}{full_image}'
        title = img_soup.find('h2', class_='title').get_text()
        
        # Adding those variables to dictionary
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title
        
        # Adding dictionary to list
        hemi_image_and_titles.append(hemispheres)
        browser.back()

    return hemi_image_and_titles

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

    