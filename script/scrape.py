#!/usr/bin/env python

import logging as log
import os
from pathlib import Path
from pprint import pformat
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup as bs

base = "https://www.smbc-comics.com/comic/"

log.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())


def main():
    """
    scrape comic metadata
    """

    comic = scrape("https://www.smbc-comics.com")['comic']

    while comic:
        path = Path(f'source/comics/{comic}.md')

        if path.exists():
            log.info(f"Skipping {comic}")
            with open(path, 'r') as f:
                # split out YAML header
                _, header, content = f.read().split('---', maxsplit=2)
                comic = yaml.load(header, yaml.SafeLoader)['prev']
            continue

        values = scrape(base + comic)

        with open(path, 'w') as f:
            del values['comic']
            log.info(pformat(values))
            # `width=` sets maximum line length
            # https://stackoverflow.com/questions/18514205/how-to-prevent-yaml-to-dump-long-line-without-new-line/18526119#18526119
            f.write(markdown(yaml.dump(values, width=float("inf"))))
        comic = values['prev']


def scrape(url):
    sauce = requests.get(url)
    soup = bs(sauce.content, 'html.parser')
    return get_values(soup)


def get_values(page):
    return {
        'title': comic_title(page),
        'image': comic_url(page),
        'hovertext': hovertext(page),
        'extra_image': extra_comic_url(page),
        'comic': permalink(page),
        'prev': prev_comic(page),
        'next': next_comic(page),
    }


def prev_comic(page):
    prev = page.find(rel='prev')
    if prev:
        return prev['href'][len(base):]
    else:
        return None


def next_comic(page):
    # `next` is a keyword in Python
    _next = page.find(rel='next')
    if _next:
        return _next['href'][len(base):]
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
    prefix = "http://smbc-comics.com/comic/"
    return permalink['value'].strip()[len(prefix):]


def basename(url):
    return os.path.basename(urlparse(url).path).strip()


def markdown(data):
    """
    write markdown YAML header
    """
    return f"---\n{data}---\n"


if __name__ == "__main__":
    main()
