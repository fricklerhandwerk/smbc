#!/usr/bin/env python

from pathlib import Path

import scrape
from PIL import Image


def main():
    """
    verify integrity of images
    """

    for p in Path('_comics').iterdir():
        if p.suffix == '.md':
            with open(p, 'r') as f:
                content, data = scrape.from_markdown(f.read())
            path = p.with_suffix('')
            verify(path, data['image'])
            verify(path, data['extra_image'])


def verify(path, url):
    target = path/scrape.basename(url)
    if target.exists() and target.is_file():
        try:
            im = Image.open(target)
            im.verify()
        except:
            print(f"deleting {target}")
            target.unlink()


if __name__ == "__main__":
    main()
