import json
import os
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs


def main():
    url = "https://smbc-comics.com"

    while url:
        sauce = requests.get(url)
        soup = bs(sauce.content, 'html.parser')

        values = get_values(soup)

        name = basename(values['permalink'])
        path = Path(f'comics/{name}')

        if not path.exists():
            path.mkdir()
            with open(path/'data.json', 'w') as out:
                pprint(values)
                json.dump(values, out, indent='  ')

        url = previous(soup)


def get_values(page):
    return {
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
