#!/usr/bin/env python

import logging as log
import os
import sys
from pathlib import Path
from urllib.request import urlretrieve

import scrape
import yaml
from requests.utils import requote_uri

log.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())


def main():
    """
    download images based on local metadata
    """

    for p in Path('_comics').iterdir():
        if p.suffix == '.md':
            with open(p, 'r') as f:
                _, header, content = f.read().split('---', maxsplit=2)
            data = yaml.load(header, yaml.SafeLoader)
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
