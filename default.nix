let
  pkgs = import (
    fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/heads/release-20.09.tar.gz"
  ) {};
  mach-nix = import (
    fetchTarball "https://github.com/DavHau/mach-nix/archive/refs/tags/3.3.0.tar.gz"
  ) { inherit pkgs; };
  pyEnv = mach-nix.mkPython {
    requirements = builtins.readFile ./script/requirements.txt;
  };
  jekyllEnv = pkgs.bundlerEnv {
    name = "jekyll-github-pages";
    ruby = pkgs.ruby;
    gemfile = ./Gemfile;
    lockfile = ./script/Gemfile.lock;
    gemset = ./script/gemset.nix;
  };
  update-gems = pkgs.writeScriptBin "update-gems" ''
    export PATH=${with pkgs; lib.makeBinPath [ bundler bundix coreutils ]}
    bundler package --no-install --path vendor
    rm -rf .bundle* vendor
    exec bundix --gemset=script/gemset.nix --lockfile=script/Gemfile.lock
  '';
in pkgs.stdenv.mkDerivation {
  name = "transcribe-smbc";
  buildInputs = [ pyEnv jekyllEnv update-gems ];
}
