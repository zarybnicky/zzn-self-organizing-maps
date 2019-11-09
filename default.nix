{ pkgs ? import <nixpkgs> { config = { allowBroken = true; }; } }:

pkgs.python3Packages.buildPythonApplication {
  name = "zzn-self-organizing-maps";
  propagatedBuildInputs = with pkgs.python3Packages; [
    numpy
    pylint
    flake8
  ];
}
