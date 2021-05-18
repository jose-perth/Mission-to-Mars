# Import Spliter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

### Visit the Red Planet Science news site

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

### Featured Images from Spaceimages-Mars

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

### Scrape Mars Facts table

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['Description','Mars','Earth']
df.set_index('Description', inplace=True)

df.to_html()

### Deliverable 1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

#### Hemispheres and titles

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

thumb_images = browser.find_by_tag("h3")

# Visit each site and scrape .jpg image
for i in range(4):
    thumb_images[i].click()
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    download_box = img_soup.find("div", class_="downloads")
    img_url_rel = download_box.find("a", target="_blank")['href']
    img_url = f"{url}{img_url_rel}"
    title = img_soup.find("h2", class_="title").text
    hemisphere_image_urls.append({'img_url':img_url, 'title':title})
    
    # return to previous page
    browser.back()
    # Delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #need to reevaluate thumb_images before the next visit
    thumb_images = browser.find_by_tag("h3")

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




