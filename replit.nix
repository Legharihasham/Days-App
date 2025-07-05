
{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.git
    pkgs.which
    pkgs.jdk11
    pkgs.android-tools
  ];
}
