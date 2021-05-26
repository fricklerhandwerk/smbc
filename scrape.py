import json
import os
from pathlib import Path
from pprint import pprint
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs


# the first comic
start = "https://www.smbc-comics.com/comic/2002-09-05"


def main():
    url = start

    while url:
        name = basename(url)
        path = Path(f'comics/{name}')

        if path.exists():
            print(f"Skipping {name}...")
            with open(path/'data.json', 'r') as out:
                url = json.load(out)['next']
            continue

        sauce = requests.get(url)
        soup = bs(sauce.content, 'html.parser')
        values = get_values(soup)

        path.mkdir(parents=True)
        with open(path/'data.json', 'w') as out:
            pprint(values)
            json.dump(values, out, indent='  ')
        url = next_comic(soup)


def get_values(page):
    return {
        'title': comic_title(page),
        'image': comic_url(page),
        'hovertext': hovertext(page),
        'extra_image': extra_comic_url(page),
        'url': permalink(page),
        'prev': prev_comic(page),
        'next': next_comic(page),
    }


def prev_comic(page):
    prev = page.find(rel='prev')
    if prev:
        return prev['href']
    else:
        return None


def next_comic(page):
    # `next` is a keyword in Python
    _next = page.find(rel='next')
    if _next:
        return _next['href']
    else:
        return None


def comic_title(page):
    title = page.title.string
    prefix = "Saturday Morning Breakfast Cereal - "
    return title[len(prefix):].strip()


def comic_url(page):
    img = page.find(id='cc-comic')
    return img['src'].strip()


def hovertext(page):
    img = page.find(id='cc-comic')
    return img['title'].strip()


def extra_comic_url(page):
    after = page.find(id='aftercomic').img
    return after['src'].strip()


def permalink(page):
    permalink = page.find(id='permalinktext')
    return permalink['value'].strip()


def basename(url):
    return os.path.basename(urlparse(url).path).strip()


if __name__ == "__main__":
    main()
