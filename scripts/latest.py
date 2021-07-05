#!/usr/bin/env python

from pathlib import Path

import scrape


def main():
    """
    get latest comic
    """

    for p in Path('_comics').iterdir():
        # this is somewhat inefficient, as one could pick an arbitrary strip
        # and follow the linked list from there, but easiest to read and write
        if p.suffix == '.md':
            with open(p, 'r') as f:
                content, data = scrape.from_markdown(f.read())
            if data['next_comic'] is None:
                print(p.with_suffix('').name, end='')
                return


if __name__ == "__main__":
    main()
