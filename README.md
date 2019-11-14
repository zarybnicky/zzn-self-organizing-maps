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

Tasks:
- CLI [JH]
  - learn
  - [OPTIONAL] classify (k-means - https://codereview.stackexchange.com/questions/205097/k-means-using-numpy)
  - visualize
- learning algorithm [JZ]
  - SOM
  - [OPTIONAL] GSOM
- visualization [JH]
  - animation (https://gist.github.com/Seanny123/2c7efd90bebbe9c7bea6a1bd30a2133c)
  - image export
- dataset testing
  - Iris [JZ]
  - Digit recognizer [JH]
