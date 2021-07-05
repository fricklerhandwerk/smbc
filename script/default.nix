{ pkgs }:
let
  mach-nix = import (
    fetchTarball "https://github.com/DavHau/mach-nix/archive/refs/tags/3.3.0.tar.gz"
  ) { inherit pkgs; };
in mach-nix.mkPython {
  requirements = builtins.readFile ./requirements.txt;
}
