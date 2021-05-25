let
  pkgs = import (
    fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/heads/release-20.09.tar.gz"
  ) {};
  mach-nix = import (
    fetchTarball "https://github.com/DavHau/mach-nix/archive/refs/tags/3.3.0.tar.gz"
  ) { inherit pkgs; };
in
mach-nix.mkPythonShell {
  requirements = builtins.readFile ./requirements.txt;
}
