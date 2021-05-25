from bs4 import BeautifulSoup as bs
import requests
import os
from urllib.parse import urlparse
from datetime import datetime
from pprint import pprint


def main():
    url = "https://smbc-comics.com"

    sauce = requests.get(url)
    soup = bs(sauce.content, 'html.parser')

    pprint(get_values(soup))


def get_values(page):
    return {
        'date': comic_date(page),
        'title': comic_title(page),
        'url': comic_url(page),
        'hovertext': hovertext(page),
        'extra_url': extra_comic_url(page),
        'permalink': permalink(page),
    }


def comic_date(page):
    url = comic_url(page)
    filename = os.path.splitext(basename(url))[0]
    date = filename[len(filename)-8:]
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')


def comic_title(page):
    title = page.title.string
    prefix = "Saturday Morning Breakfast Cereal - "
    return title[len(prefix):]


def comic_url(page):
    img = page.find(id='cc-comic')
    return img['src']


def hovertext(page):
    img = page.find(id='cc-comic')
    return img['title']


def extra_comic_url(page):
    after = page.find(id='aftercomic').img
    return after['src']


def permalink(page):
    permalink = page.find(id='permalinktext')
    return permalink['value']


def basename(url):
    return os.path.basename(urlparse(url).path)


if __name__ == "__main__":
    main()
