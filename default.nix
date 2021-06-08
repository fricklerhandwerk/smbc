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
  default = pkgs.stdenv.mkDerivation {
    name = "transcribe-smbc";
    buildInputs = [ pyEnv jekyllEnv ];
  };
  override = attrs: default.overrideAttrs (old: attrs);
in
{
  inherit default pyEnv;
  update-gems = override {
    nativeBuildInputs = with pkgs; [ bundler bundix ];
    shellHook = ''
      bundler package --no-install --path vendor
      rm -rf .bundle* vendor
      exec bundix
    '';
  };
}
