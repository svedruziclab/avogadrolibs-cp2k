# CP2K input generator for Avogadro 2

**Note:** This software is **DISCONTINUED** since we switched to the C++/Qt interface and should be used for
experimentation only. There is absolutely no guarantee of correctness of
generated input files; they might produce unrealistic results, crash randomly,
or scare your cat. Or any combination of those.

## Description

[CP2K](http://cp2k.org/) is a program to perform atomistic and molecular
simulations of solid state, liquid, molecular, and biological systems.

[Avogadro 2](http://www.openchemistry.org/projects/avogadro2/) is a chemical
editor and visualization application, and also a set of reusable software
libraries written in C++.

Avogadro 2 already provides input generators for various quantum chemistry
software such as [GAMESS](http://www.msg.ameslab.gov/gamess/) and
[NWChem](http://www.nwchem-sw.org/). Our goal is to provide support for
generating CP2K input files.

## Installation

Copy the file `cp2k.py` into

* `Avogadro2/lib/avogadro2/scripts/inputGenerator` (Windows)
* `<prefix>/lib/avogadro2/scripts/inputGenerator` (Debian)
* `<prefix>/lib64/avogadro2/scripts/inputGenerator` (Fedora)

and restart Avogadro 2. If you get `CP2K` entry in `Quantum\Input Generators`
menu, the installation was successful.

## Usage

Load the molecule you want to work with and then use Avogadro 2 menu to
`Quantum\Input Generators` and select `CP2K`. This opens a window where input
file parameters can be configured.

**Note:** Generated input file requires you to manually change
`BASIS_SET_FILE_NAME` (default `BASIS_SET`) and `POTENTIAL_FILE_NAME` (default
`GTH_POTENTIALS`) to correct file paths for your system. We aim to eventually
remove this requirement.

## Bug reports

There are probably lots of bugs. If you find one, report it using GitHub issue
tracker. Feature requests are also welcome.

## Contributing code

As Linus Torvalds said

> ... the Linux philosophy is "laugh in the face of danger". Oops. Wrong one.
> "Do it yourself". That's it.

If you desire to contribute a patch, please fork the repo, commit your changes
and send a pull request.

## Contact

[Tomislav Šubić](https://github.com/tsubic)
[Vedran Miletić](https://github.com/rivanvx)
