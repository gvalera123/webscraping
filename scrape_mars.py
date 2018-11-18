from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(20)

    articles = soup.find_all('li',class_='slide')

    news_title = articles[0].find('div',class_='content_title').find('a').contents[0]

    news_p = articles[0].find('div',class_='article_teaser_body').contents[0]

    base_url = 'https://www.jpl.nasa.gov'
    jpl_url = base_url + '/spaceimages/?search=&category=Mars'

    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    img_url = soup.find('a',class_='button fancybox').get('data-fancybox-href')
    featured_image_url = base_url + img_url

    base_url = 'https://twitter.com'
    twitter_url = base_url + '/marswxreport?lang=en'

    browser.visit(twitter_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    mars_weather = soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').contents[0]

    mars_url = 'https://space-facts.com/mars/'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    table = pd.read_html(mars_url)

    df= table[0]
    df.columns = ['key','value']
    df = df.set_index(['key'])
    html_table = df.to_html()
    html_table = html_table.replace('\n','')


    base_url = 'https://astrogeology.usgs.gov'
    usgs_url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(usgs_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(5)

    linklist = []
    usgslinks = soup.find_all('a',class_='itemLink product-item')

    for link in usgslinks:
        linklist.append(base_url + link.get('href'))

    linklist = list(set(linklist))

    hemisphere_image_urls = []
    for link in linklist:
        browser.visit(link)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h2').contents[0]
        img_url = soup.find_all('a',target="_blank")[0].get('href')

        img_dict = {'title':title,
                    'img_url':img_url}

        hemisphere_image_urls.append(img_dict)

    mars_data = {'news_title':news_title,
                       'news_p':news_p,
                       'featured_image_url':featured_image_url,
                       'mars_weather':mars_weather,
                       'html_table':html_table,
                       'hemisphere_image_urls':hemisphere_image_urls}
    return mars_data
