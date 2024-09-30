# nix/default.nix

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.virtualenv
    redis
    git
    docker
    # Add other dependencies if necessary
  ];

  shellHook = ''
    export FLASK_APP=main.py
    export FLASK_ENV=development
    echo "Welcome to the Chat App development environment!"
  '';
}