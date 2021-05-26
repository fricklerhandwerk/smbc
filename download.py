import json
from pathlib import Path
from urllib.request import urlretrieve

import scrape
from requests.utils import requote_uri


def main():
    """
    download images based on local metadata
    """

    for p in Path('comics').iterdir():
        if p.is_dir():
            with open(p/'data.json', 'r') as f:
                data = json.load(f)
            fetch(p, data['image'])
            fetch(p, data['extra_image'])


def fetch(p, url):
    target = p/scrape.basename(url)
    if not target.exists():
        urlretrieve(requote_uri(url), target)
        print(target)


if __name__ == "__main__":
    main()
