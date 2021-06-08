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

    # start scraping at home page, which shows the latest comic
    values = scrape("https://www.smbc-comics.com")
    current = values['comic']
    _next = None

    while current:
        path = Path(f'source/comics/{current}.md')

        if path.exists():
            log.debug(f"File exists: {current}")
            with open(path, 'r') as f:
                # split out YAML header
                _, header, content = f.read().split('---', maxsplit=2)
            data = yaml.load(header, yaml.SafeLoader)
            # update pointer to next comic if none exists
            if not data['next']:
                log.info(f"Update: {current} -> {_next}")
                data['next'] = _next
                with open(path, 'w') as f:
                    f.write(markdown(content, data))
            _next = current
            current = data['prev']
            continue

        values = scrape(base + current)

        _next = values['comic']
        del values['comic']
        with open(path, 'w') as f:
            log.info("New: %s\n%s", _next, pformat(values))
            f.write(markdown("", values))
        current = values['prev']


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


def markdown(content, data=None):
    """
    write markdown file contents with optional YAML header
    """
    if data:
        # `width=` sets maximum line length
        # https://stackoverflow.com/questions/18514205/how-to-prevent-yaml-to-dump-long-line-without-new-line/18526119#18526119
        header = yaml.dump(data, width=float("inf"))
        return f"---\n{header}---\n\n{content}"
    return content


if __name__ == "__main__":
    main()
