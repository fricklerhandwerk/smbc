import json
from pathlib import Path

import yaml


def main():
    """
    convert JSON to markdown YAML headers
    """

    for p in Path('comics').iterdir():
        if p.is_dir():
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
    return f"---\n{data}---\n"


def cleanup(data):
    """
    remove URL prefixes for easier reuse
    """
    comic = len("https://www.smbc-comics.com/comic/")

    return {
        'title': data['title'],
        'image': data['image'],
        'hovertext': data['hovertext'],
        'extra_image': data['extra_image'],
        'prev': data['prev'][comic:] if data.get('prev') else None,
        'next': data['next'][comic:] if data.get('next') else None,
    }


if __name__ == "__main__":
    main()
