from tqdm import tqdm
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import warnings

from model import Review

warnings.filterwarnings("ignore")


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
driver.get("https://www.imdb.com/title/tt1877830/reviews?ref_=tt_urv")
sel = Selector(text=driver.page_source)
review_counts = sel.css('.lister .header span::text').extract_first().replace(
    ',', '').split(' ')[0]

more_review_pages = int(int(float(review_counts))/25)
print(more_review_pages)
for i in tqdm(range(more_review_pages)):
    try:
        css_selector = 'load-more-trigger'
        driver.find_element(By.ID, css_selector).click()
        driver.implicitly_wait(2.5)
    except Exception as e:
        print(e)
        pass

reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
counter = 0
for review in reviews:
    if (counter > 10):
        break
    try:
        sel2 = Selector(text=review.get_attribute('innerHTML'))
        rating = sel2.css(
            '.rating-other-user-rating span::text').extract_first().strip()
        review = sel2.css(
            '.text.show-more__control').extract_first().strip()
        review = review.replace('<div class="text show-more__control">',
                                '').replace('</div>', '').replace("<br>", "").replace('&amp;', '')
        review_date = sel2.css('.review-date::text').extract_first().strip()
        author = sel2.css('.display-name-link a::text').extract_first().strip()
        review_title = sel2.css('a.title::text').extract_first().strip()
        review_url = sel2.css('a.title::attr(href)').extract_first().strip()
        helpfulness = sel2.css(
            '.actions.text-muted::text').extract_first().strip()
        current_review = Review(review=review, review_title=review_title,
                                rating=rating, url=review_url, date=review_date)

    except Exception:
        pass
