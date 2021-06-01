import json
import sys
from pathlib import Path

import yaml


def main():
    """
    convert JSON to markdown YAML headers
    """

    p = Path(sys.argv[1])
    with open(p/'data.json', 'r') as f:
        data = json.load(f)
    # `width=` sets maximum line length
    # https://stackoverflow.com/questions/18514205/how-to-prevent-yaml-to-dump-long-line-without-new-line/18526119#18526119
    with open(str(p.resolve()) + '.md', 'w') as f:
        f.write(markdown(yaml.dump(cleanup(data), width=float("inf"))))


def markdown(data):
    """
    write markdown YAML header
    """
    return f"""
---
{data}---
"""

def cleanup(data):
    """
    remove URL prefixes for easier reuse
    """
    comic = len("https://www.smbc-comics.com/comic/")
    permalink = len("http://smbc-comics.com/comic/")
    image = len("https://www.smbc-comics.com/comics/")

    return {
        'title': data['title'],
        'image': data['image'][image:],
        'hovertext': data['hovertext'],
        'extra_image': data['extra_image'][image:],
        'id': data['url'][permalink:],
        'prev': data['prev'][comic:],
        'next': data['next'][comic:],
    }

if __name__ == "__main__":
    main()
