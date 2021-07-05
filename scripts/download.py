#!/usr/bin/env python

import logging as log
import os
from pathlib import Path
from urllib.request import urlretrieve

import scrape
from requests.utils import requote_uri

log.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())


def main():
    """
    download images based on local metadata
    """

    for p in Path('_comics').iterdir():
        if p.suffix == '.md':
            with open(p, 'r') as f:
                content, data = scrape.from_markdown(f.read())
            path = p.with_suffix('')
            path.mkdir(parents=True, exist_ok=True)
            fetch(path, data['image'])
            fetch(path, data['extra_image'])


def fetch(path, url):
    target = path/scrape.basename(url)
    if not target.exists():
        urlretrieve(requote_uri(url), target)
        log.info(target)


if __name__ == "__main__":
    main()
