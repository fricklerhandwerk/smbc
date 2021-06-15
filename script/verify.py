#!/usr/bin/env python

from pathlib import Path

import PIL
import scrape
import yaml
from PIL import Image


def main():
    """
    verify integrity of images
    """

    for p in Path('_comics').iterdir():
        if p.suffix == '.md':
            with open(p, 'r') as f:
                _, header, content = f.read().split('---', maxsplit=2)
            data = yaml.load(header, yaml.SafeLoader)
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
