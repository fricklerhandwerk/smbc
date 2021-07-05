let
  pkgs = import (
    fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/59b8d9cf24e9fcf10341a0923c9bdca088dca8c8.tar.gz";
      sha256 = "08f38v4b2kcxnbapdwrb54bglka92cxj9qlnqlk5px206jyq9v4c";
    }) {};
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
