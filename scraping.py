
# import Spliter and BeautifulSoup
from splinter import Browser
#from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    print('****  browser created  *****')
    news_title , news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    print("************  DATA ********")
    print(data)
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    print('****  getting mars news  *****')
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    print('****  got  mars news  *****')
    return news_title, news_p

# ## Featured Images

def featured_image(browser):
    print('****  getting mars image  *****')
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img',class_='fancybox-image').get('src')
    except AttributeError:
        return None    

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    print('****  got mars image  *****')
    return img_url


# ## Scrape table of information
def mars_facts():
    print('****  getting mars facts  *****')
    try:    
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['description','Mars','Earth']
    df.set_index('description', inplace=True)
    print('****  got mars facts  *****')
    return df.to_html()


# ## Scrape Mars Hemisphere Full Images and Title
# ## by visiting each link
def mars_hemispheres(browser):
    
    print('****  getting mars hemis  *****')
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
    
    print('****  got mars hemis  *****')
    return hemisphere_image_urls

if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())