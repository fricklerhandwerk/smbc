{ pkgs }:
let
  mach-nix = import (
    fetchTarball "https://github.com/DavHau/mach-nix/archive/refs/tags/3.3.0.tar.gz"
  ) { inherit pkgs; };
  scripts = mach-nix.buildPythonApplication {
    src = ./.;
    requirements = builtins.readFile ./requirements.txt;
  };
  push-update = pkgs.writeShellScriptBin "push-update" ''
    # update comics archive. run from the root of this repository with `git`
    # credentials in place.
    export PATH=${with pkgs; lib.makeBinPath [ scripts git openssh coreutils ]}:$PATH
    set -e
    today=$(date --rfc-3339 date)
    git checkout master
    git pull origin master
    scrape
    git add _comics
    git commit -m "automatic update"
    git push origin master
    verify
    download
  '';
  update-gems = pkgs.writeScriptBin "update-gems" ''
    export PATH=${with pkgs; lib.makeBinPath [ bundler bundix coreutils ]}
    bundler package --no-install --path vendor
    rm -rf .bundle* vendor
    exec bundix --gemset=scripts/gemset.nix --lockfile=scripts/Gemfile.lock
  '';
in pkgs.symlinkJoin {
  name = "scripts";
  paths = [ scripts push-update update-gems ];
}
