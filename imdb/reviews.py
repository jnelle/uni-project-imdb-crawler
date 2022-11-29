from tqdm import tqdm
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dependency_injector.wiring import Provide, inject
from db.mongo import MongoService
from models.model import Review

import warnings
from provider.db_provider import Container

warnings.filterwarnings("ignore")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


@inject
async def get_reviews(service: MongoService = Provide[Container.service]) -> None:

    driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
    driver.get("https://www.imdb.com/title/tt1877830/reviews?ref_=tt_urv")
    sel = Selector(text=driver.page_source)
    review_counts = sel.css('.lister .header span::text').extract_first().replace(
        ',', '').split(' ')[0]
    movie_id = sel.css(
        '.article .subpage_title_block .subpage_title_block__right-column a::attr(href)').extract_first().split('/')[2]
    movie_name = sel.css(
        '.article .subpage_title_block .subpage_title_block__right-column a::text').extract_first()
    movie_year = sel.css(
        '.article .subpage_title_block .subpage_title_block__right-column span::text').extract_first().strip().replace('(', '').replace(')', '')

    more_review_pages = int(int(review_counts)/25)
    for i in tqdm(range(more_review_pages)):
        try:
            driver.find_element(By.ID, 'load-more-trigger').click()
            driver.implicitly_wait(4)
        except Exception as e:
            print(e)
            pass

    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
    for review in reviews:
        try:
            sel2 = Selector(text=review.get_attribute('innerHTML'))
            rating = sel2.css(
                '.rating-other-user-rating span::text').extract_first().strip()
            review = sel2.css(
                '.text.show-more__control').extract_first().strip()
            review = review.replace('<div class="text show-more__control">',
                                    '').replace('</div>', '').replace("<br>", "").replace('&amp;', '')
            review_date = sel2.css(
                '.review-date::text').extract_first().strip()
            author = sel2.css(
                '.display-name-link a::text').extract_first().strip()
            review_title = sel2.css('a.title::text').extract_first().strip()
            review_url = sel2.css(
                'a.title::attr(href)').extract_first().strip()
            helpfulness = sel2.css(
                '.actions.text-muted::text').extract_first().strip()
            await service.add_review(Review(review=review, review_title=review_title,
                                            rating=rating, url="https://www.imdb.com" + review_url,
                                            date=review_date, helpfulness=helpfulness, author=author,
                                            id=movie_id, year=int(
                                                movie_year),
                                            name=movie_name))
        except Exception as e:
            print(e)
