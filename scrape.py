from selenium import webdriver
import os
from urllib.parse import urlparse
from datetime import datetime
from pprint import pprint


def main():
    url = "https://smbc-comics.com"

    profile = webdriver.FirefoxProfile()
    profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get(url)
    pprint(get_values(browser))


def get_values(browser):
    return {
        'date': comic_date(browser),
        'title': comic_title(browser),
        'url': comic_url(browser),
        'hovertext': hovertext(browser),
        'extra_url': extra_comic_url(browser),
        'permalink': permalink(browser),
    }


def comic_date(browser):
    url = comic_url(browser)
    filename = os.path.splitext(basename(url))[0]
    date = filename[len(filename)-8:]
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')


def comic_title(browser):
    return browser.title[len("Saturday Morning Breakfast Cereal - "):]


def comic_url(browser):
    img = browser.find_element_by_id('cc-comic')
    return img.get_attribute('src')


def hovertext(browser):
    img = browser.find_element_by_id('cc-comic')
    return img.get_attribute('title')


def extra_comic_url(browser):
    after = browser.find_element_by_css_selector('#aftercomic img')
    return after.get_attribute('src')


def permalink(browser):
    permalink = browser.find_element_by_id('permalinktext')
    return permalink.get_attribute('value')


def basename(url):
    return os.path.basename(urlparse(url).path)


if __name__ == "__main__":
    main()
