let
  pkgs = import (
    fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/heads/release-20.09.tar.gz"
  ) {};
  mach-nix = import (
    fetchTarball "https://github.com/DavHau/mach-nix/archive/refs/tags/3.3.0.tar.gz"
  ) { inherit pkgs; };
  pyEnv = mach-nix.mkPython {
    requirements = builtins.readFile ./requirements.txt;
  };
  jekyllEnv = pkgs.bundlerEnv {
    name = "jekyll-github-pages";
    ruby = pkgs.ruby;
    gemfile = ./Gemfile;
    lockfile = ./Gemfile.lock;
    gemset = ./gemset.nix;
  };
  updateGems = pkgs.writeShellScriptBin "update-gems" ''
    PATH=${with pkgs; lib.makeBinPath [ bundler bundix ]}:$PATH
    bundler package --no-install --path vendor
    rm -rf .bundle* vendor
    exec bundix
  '';
in pkgs.mkShell {
  buildInputs = with pkgs; [
    pyEnv
    jekyllEnv
    updateGems
  ];
}
