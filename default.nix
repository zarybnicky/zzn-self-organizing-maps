{ pkgs ? import <nixpkgs> { config = { allowBroken = true; }; } }:

let graphics-py = with pkgs.python3Packages; buildPythonPackage rec {
  pname = "graphics.py";
  version = "5.0.1.post1";
  src = fetchPypi {
    inherit pname version;
    sha256 = "15qa6cp0s6g8937bpprh5fqrclv1zk0544rbzd9f8ivlaz662daq";
  };
  propagatedBuildInputs = [ tkinter ];
  doCheck = false;
};
in pkgs.python3Packages.buildPythonApplication {
  name = "zzn-self-organizing-maps";
  propagatedBuildInputs = with pkgs.python3Packages; [
    numpy
    pylint
    flake8
    matplotlib
    graphics-py
    tkinter
  ];
}
