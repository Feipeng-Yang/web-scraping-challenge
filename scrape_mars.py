
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.perser'
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results = soup.find_all('div', class_='list_text')

    # Identify and return title 
    news_title = results[0].find('div', class_='content_title').text
    # Identify and return paragraph
    news_p = results[0].find('div', class_='article_teaser_body').text
    # Print results
    print(news_title)
    print(news_p)

    # ## JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    html = browser.html
    # Create BeautifulSoup object; parse with 'html.perser'
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    # click the eatured Mars Image botton
    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    # Create BeautifulSoup object; parse with 'html.perser'
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results = soup.find_all('img', class_='fancybox-image')

    # find the url for the featured image
    link = results[0]['src']
    featured_image_url = url + '/' + link
    featured_image_url

    # ## Mars Facts
    import pandas as pd
    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)
    df = tables[0]

    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    df = df.rename(columns={'Mars - Earth Comparison': 'Description'}) 
    df = df.set_index('Description')

    # convert the data to a HTML table
    html_table = df.to_html()
    html_table

    # strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')

    # save the table directly to a html file
    df.to_html('table.html')

    # ## Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    # Create BeautifulSoup object; parse with 'html.perser'
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    # Retrieve the parent divs for all Hemispheres
    results = soup.find_all('div', class_='description')


    # define a list to store hemisphere title and url
    hemisphere_image_urls = []
    # loop over results to get hemisphere data
    for result in results:
        browser.visit(url)
        # scrape the hemisphere title
        title = result.find('h3').text
        
        # click on one hemisphere and go to the link
        browser.links.find_by_partial_text(title).click()
        
        # get the html for each hemisphere
        html = browser.html
        
        # Create BeautifulSoup object; parse with 'html.perser'
        soup = BeautifulSoup(html, 'html.parser')
        img_results = soup.find_all('a', text='Original')
        image_url = img_results[0]['href']
        img_url = url + image_url
        
        # print hemisphere and image url
        print('-----------------')
        print(title)
        print(img_url)
        
        # Dictionary to be inserted into MongoDB
        hemisphere = {
            'title': title,
            'img_url': img_url,
        }
        hemisphere_image_urls.append(hemisphere)

    # display hemisphere_image_urls
    hemisphere_image_urls

    # quit browser
    browser.quit()

    # return the data
    return news_title, news_p, featured_image_url, html_table, hemisphere_image_urls