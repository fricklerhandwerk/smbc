# Development

## Requirements

Install [nix](https://nixos.org/) package manager to use the scripts.

```sh
sh <(curl -L https://nixos.org/nix/install) --daemon
```

## Wrangling Data

### Scrape metadata

Go through all strips on [smbc-comics.com](https://www.smbc-comics.com) and extract meta data to YAML headers of markdown files.

```sh
nix-shell --run scrape
```

### Download image files

Using locally available meta data, download image files. This will take a lot of time initially, as it runs sequentially. Check out an earlier revision for parallel downloads.

```sh
nix-shell --run download
```

### Verify image files

This will delete broken images, which may be left over if downloading is cancelled mid-way.

```sh
nix-shell --run verify
```

## Working with Jekyll/GitHub pages

### Serve pages locally

```sh
nix-shell --run "jekyll serve"
```

### Update dependencies

```sh
nix-shell --run update-gems
```
