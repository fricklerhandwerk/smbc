#!/usr/bin/env python

import json
from pathlib import Path

import PIL
import scrape
from PIL import Image


def main():
    """
    verify integrity of images
    """

    for p in Path('comics').iterdir():
        if p.is_dir():
            with open(p/'data.json', 'r') as f:
                data = json.load(f)
            verify(p, data['image'])
            verify(p, data['extra_image'])


def verify(p, url):
    target = p/scrape.basename(url)
    if target.exists():
        try:
            im = Image.open(target)
            im.verify()
        except:
            print(f"deleting {target}")
            target.unlink()


if __name__ == "__main__":
    main()
