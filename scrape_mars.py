from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


#NASA Mars News
def scrape_info():
    
    mars_data={}
    
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit https:mars.nasa.gov
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # results are returned as an iterable list
    latest_results = soup.find_all('li', class_='slide')
    
    # Retrieve the latest news title and paragraph
    first = latest_results[0]
    
    # Scraping for the first title name
    news_title = first.find('div', class_='content_title').text
    
    # Scraping for the first article paragraph verbiage
    news_p = first.find('div', class_='article_teaser_body').text

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
    }


#JPL Mars Space Images -Featured Mars Image
    
    # Visit https://data-class site
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    img_soup = bs(html, 'html.parser')
    
    # Use Splinter to click on the view 
    browser.links.find_by_partial_text('FULL IMAGE').click()
    
    html = browser.html
    img_soup = bs(html, "html.parser")
    
    # Retrieve the parent divs for all articles
    img_src = img_soup.find(class_='headerimage fade-in').get("src")
    
    # Drilldown into the url needed
    crop_img_url = url[:-10]
    
    featured_image_url = (f'{crop_img_url}{img_src}')
    
    mars_data["featured_image_url"] = featured_image_url


# # Mars Facts
#     df = pd.read_html("https://space-facts.com/mars/")[0]
#     df.columns=["Description", "Value"]
#     df.set_index("Description", inplace=True)
    
#     mars_data["facts"] = df
#     return mars_data


# Mars Hemispheres
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    html = browser.html
    time.sleep(5)
    soup = bs(html, 'html.parser')

    # Gather description to parse for title
    group_list = soup.find_all(class_= 'description')

    # Drilldown into the titles
    title_list = []
    for name in group_list:
        title_list.append(name.a.h3.text)

    # Create loop to group the titles
    browser.visit(mars_hemi_url)
    hemisphere_image_urls=[]

    for x in range(len(title_list)):
        browser.click_link_by_partial_text(title_list[x])
        html = browser.html
        soup = bs(html, 'html.parser')
        title = title_list[x]
        img_url = soup.find(class_='downloads')

    #Store in dictionary
        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['img_url'] = img_url.a['href']
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

        mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    return mars_data


    # Close the browser after scraping
    browser.quit()

