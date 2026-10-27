{ pkgs ? import <nixpkgs> {} }:

let
  devDependencies = {
    python = pkgs.python3;
  };
in
pkgs.mkShell {
  name = "Mastermind";

  buildInputs = builtins.attrValues devDependencies;

  shellHook = ''
    echo "Dev-Environment for Klotski"

    ${builtins.concatStringsSep "\n" (
      map (name: ''
        echo "${name}: ${devDependencies.${name}.version}"
      '') (builtins.attrNames devDependencies)
    )}

    source env/bin/activate
  '';
}
