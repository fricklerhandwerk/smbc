let
  pkgs = import (
    fetchTarball {
      url = "https://github.com/NixOS/nixpkgs/archive/59b8d9cf24e9fcf10341a0923c9bdca088dca8c8.tar.gz";
      sha256 = "08f38v4b2kcxnbapdwrb54bglka92cxj9qlnqlk5px206jyq9v4c";
    }) {};
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
  pyEnv = import ./script { inherit pkgs; };
in pkgs.stdenv.mkDerivation {
  name = "transcribe-smbc";
  src = ./.;
  buildInputs = [ jekyllEnv update-gems pyEnv ];
  dontConfigure = true;
  buildPhase = ''
    # work around https://github.com/mmistakes/jekyll-theme-hpstr/issues/185
    export LC_ALL="en_US.UTF-8"
    mkdir $out
    jekyll build --destination $out
  '';
  dontInstall = true;
}
