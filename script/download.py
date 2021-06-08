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

    p = Path(sys.argv[1])
    with open(p, 'r') as f:
        _, header, content = f.read().split('---', maxsplit=2)
    data = yaml.load(header, yaml.SafeLoader)
    fetch(p, data['image'])
    fetch(p, data['extra_image'])


def fetch(p, url):
    path = p.with_suffix('')
    path.mkdir(parents=True, exist_ok=True)
    target = path/scrape.basename(url)
    if not target.exists():
        urlretrieve(requote_uri(url), target)
        log.info(target)


if __name__ == "__main__":
    main()
