import json
import os
from datetime import datetime
from pprint import pprint
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs


def main():
    url = "https://smbc-comics.com"

    result = []
    while url:
        sauce = requests.get(url)
        soup = bs(sauce.content, 'html.parser')

        values = get_values(soup)
        pprint(values)
        result.append(values)

        url = previous(soup)

    with open('result.json', 'w') as out:
        json.dump(result, out, indent='  ')


def get_values(page):
    return {
        'date': comic_date(page),
        'title': comic_title(page),
        'url': comic_url(page),
        'hovertext': hovertext(page),
        'extra_url': extra_comic_url(page),
        'permalink': permalink(page),
    }


def previous(page):
    prev = page.find(rel='prev')
    if prev:
        return prev['href']
    else:
        return None


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
