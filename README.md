# Transcribe SMBC

This is an effort to transcribe [Saturday Morning Breakfast Cereal comics](https://www.smbc-comics.com) to make them searchable.

Using the strips for this purpose with Zach's permission:

> Feel free! Sounds cool.
> -- Zach Weinersmith, 2021-05-25

## Why?

You're about to make a point in an argument, and that one SMBC strip you read five years ago totally nailed it? But you can't find it anywhere... Fear not! From now on you can finally search for SMBC content on the web. With luck, the comic in question is already transcribed by volunteers and indexed by search engines.

# Development

## Environment

Install [nix](https://nixos.org/) package manager to use the scripts.

```sh
sh <(curl -L https://nixos.org/nix/install) --daemon
```

## Wrangling Data

### Scrape metadata

Go through all strips on smbc-comics.com and extract meta data to YAML headers of markdown files.

```sh
nix-shell --run "script/scrape.py"
```

### Download image files

Using locally available meta data, download image files. This will take a lot
of time initially, as it runs sequentially. Check out an earlier revision for
parallel downloads.

```sh
nix-shell --run "script/download.py"
```

### Verify image files

This will delete broken images, which may be left over if downloading is cancelled mid-way.

```sh
nix-shell --run "script/verify.py"
```

## Working with Jekyll/GitHub pages

### Serve pages locally

```sh
nix-shell --run "jekyll serve --incremental"
```

### Update dependencies

```sh
nix-shell -A update-gems
```
