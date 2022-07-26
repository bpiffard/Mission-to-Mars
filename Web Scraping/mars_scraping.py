# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setting an executable path for Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Article titles and summaries

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Creating html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Using parent element to find th first 'a' tag and save it as news_title
news_title = slide_elem.find('div', class_='content_title').get_text()

# Using parent element to find summary text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse html of the new page w/ beautiful soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Adding base url to code 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# ### Mars Facts

# Converting table found on the web to a pandas df
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

# Converting dataframe back to html
df.to_html()

# Ending session
browser.quit()




