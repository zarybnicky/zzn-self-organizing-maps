# Self Organizing Maps (ZZN, winter 2019, VUT)

The only required dependency is numpy - you can install it either via your
system's package manager, or if you use Nix, you can enter the provided Nix
shell by typing `nix-shell`on the command line.

To run:
```
./som.py -i <input> -o live|<file> -s 265x128
```

Available parameters:
- `-s AxB` - size of the map, X dimension `x` Y dimension
- `-i <file>` - input file as a CSV file (all rows must have the same width)
- `-o <type>` - output type, either live visualization via matplotlib, or a
  filename to write the resulting map into
