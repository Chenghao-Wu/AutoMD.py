[![Build Status](https://travis-ci.org/jewettaij/moltemplate.svg?branch=master)](./.travis.yml)
[![GitHub](https://img.shields.io/github/license/jewettaij/moltemplate)](./LICENSE.md)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/moltemplate)](https://pypistats.org/packages/moltemplate)
[![PyPI - Version](https://img.shields.io/pypi/v/moltemplate)](https://pypi.org/project/moltemplate/)
[![Website](https://img.shields.io/website?down_color=orange&down_message=moltemplate.org%20offline&up_color=green&up_message=online&url=https%3A%2F%2Fmoltemplate.org)](http://moltemplate.org)
[![GitHub repo size](https://img.shields.io/github/repo-size/jewettaij/moltemplate)]()



Moltemplate
===========

##  Description

[Moltemplate](http://moltemplate.org)
is a *general* cross-platform text-based molecule builder for
[**LAMMPS**](https://lammps.sandia.gov) and *(the TCL version of)*
[**ESPResSo**](http://espressomd.org).
Moltemplate was intended for building custom coarse-grained molecular models,
but it can be used to prepare realistic all-atom simulations as well.
It currently supports the
[**OPLSAA**](./examples/all_atom/force_field_OPLSAA),
[**OPLSUA**](./examples/all_atom/force_field_OPLSUA_united_atom),
[**LOPLSAA**(2015)](./examples/all_atom/force_field_OPLSAA/hexadecane),
[**AMBER**(GAFF,GAFF2)](./examples/all_atom/force_field_AMBER),
[**DREIDING**](./examples/all_atom/force_field_DREIDING),
[**COMPASS**](./examples/all_atom/force_field_COMPASS),
[**TraPPE**(1998)](./examples/coarse_grained/solvent_models/manybodywaterMW+hydrocarbonsTraPPE)
force fields,
the
[**ATB**](https://atb.uq.edu.au) molecule database,
and the
[**MOLC**](https://pubs.rsc.org/en/content/articlelanding/2019/cp/c9cp04120f),
[**mW**](https://doi.org/10.1021/jp805227c),
[**ELBA**(water)](./examples/coarse_grained/solvent_models/ELBAwater%2Bmethanol),
[**oxDNA2**](https://dna.physics.ox.ac.uk/index.php/DNA_model_introduction),
and
[**EFF**](./examples/misc_examples/explicit_electrons/eff_CH4)
molecular models (and others).
Moltemplate is interoperable with
[**ATB**](https://atb.uq.edu.au),
[**VMD/topotools**](https://www.ks.uiuc.edu/Research/vmd),
[**PACKMOL**](http://m3g.iqm.unicamp.br/packmol/home.shtml),
[**Open Babel**](https://open-babel.readthedocs.io/en/latest/FileFormats/The_LAMMPS_data_format.html),
[**EMC**](http://montecarlo.sourceforge.net/),
[**CellPACK**](http://www.cellpack.org),
[**LigParGen**](http://moltemplate.org/doc/moltemplate_talk_2019-8-15.pdf#page=190),
[**Vipster**](https://sgsaenger.github.io/vipster),
[**struc2lammpsdf**](https://nanohub.org/resources/struc2lammpsdf),
and any other program that reads or generates LAMMPS data (.lmpdat) files.
This repository includes approximately 50 [examples](./examples).
(New force fields and examples are added continually by users.)

### Documentation

The best way to learn how to use moltemplate is to find an example
which is similar to the system that you wish to simulate and modify it.
Some of the moltemplate examples are also demonstrated (with pictures)
[here](http://moltemplate.org/visual_examples.html).

All moltemplate users should probably read chapter 4 of the
[reference manual](./doc/moltemplate_manual.pdf)
*(It's only a few pages long.  The first 3 chapters are optional.)*
In addition, there are also several
[talks/tutorials](http://moltemplate.org/doc/talks.html)
online.


### Limitations for preparing all-atom simulations

Moltemplate [does *not* choose atom types automatically ("atom typing")](http://moltemplate.org/force_field_recommendations.html),
and currently cannot be used to build all-atom proteins from scratch.
3rd-party tools may be needed to calculate atomic partial charges accurately.
(For non-trivial molecules, users are encouraged to use the
[ATB](https://atb.uq.edu.au) database,
or use the DREIDING force field which has simple [atom type rules](./doc/DREIDING_Label_Manual.pdf),
or use a 3rd-party molecule-builder
and convert the resulting files to LAMMPS format using
[OpenBabel](https://open-babel.readthedocs.io/en/latest/FileFormats/The_LAMMPS_data_format.html "Convert 3rd party sim files to LAMMPS DATA format")
followed by [ltemplify.py](./doc/doc_ltemplify.md "Convert LAMMPS DATA to Moltemplate format").)



## Typical usage

    moltemplate.sh [-atomstyle style] [-pdb/-xyz coord_file] [-vmd] system.lt


## Web page

Additional suggestions and supporting code can be found at:

http://www.moltemplate.org


## Requirements

Moltemplate requires the Bourne-shell, and a recent version of python
(2.7, 3.0 or higher), and can run on OS X, linux, or windows.
(...if a suitable shell environment has been installed.  See below.)

The *numpy* python module is also required.


## INSTALLATION INSTRUCTIONS

This directory should contain 3 folders:

    moltemplate/                  <-- source code and force fields
    doc/                          <-- the moltemplate reference manual
    examples/                     <-- examples built with moltemplate

There are two ways to install moltemplate:


## Installation using pip
If you are familiar with pip, then run the following command from within the directory where this README file is located:

    pip install . --user

This will install moltemplate for a single user.  On a shared computer, to install moltemplate system-wide, use:

    sudo pip install .

Make sure that your default pip install bin directory is in your PATH.  (This is usually something like ~/.local/bin/ or ~/anaconda3/bin/.  If you have installed anaconda, this will be done for you automatically.)  Later, you can uninstall moltemplate using:

    pip uninstall moltemplate

If you continue to run into difficulty, try installing moltemplate into a temporary virtual environment by installing "*virtualenv*", downloading moltemplate (to "~/moltemplate" in the example below), and running these commands:

    cd ~/moltemplate
    python -m venv venv     #(or "virtualenv venv" if using python2)
    source venv/bin/activate
    pip install .
    #(now do something useful with moltemplate...)

(You will have to enter "source ~/moltemplate/venv/bin/activate"
 into a terminal beforehand every time you want to run moltemplate.
Virtual environments are
[explained here](https://docs.python.org/3/tutorial/venv.html)
If all this fails, then try installing moltemplate by manually updating your
\$PATH environment variable.  Instructions for doing that are included below.


## Manual installation:

Alternatively, you can edit your $PATH environment variable manually to 
include the subdirectory where the "moltemplate.sh" script is located,
as well as the subdirectory where most of the python scripts are located.
Suppose the directory with this README file is named "moltemplate"
and is located in your home directory:

If you use the *BASH* shell, typically you would edit your
`~/.bashrc` file (or `~/.profile`, `~/.bash_profile` files)
to contain the following lines:

    export PATH="$PATH:$HOME/moltemplate/moltemplate"
    export PATH="$PATH:$HOME/moltemplate/moltemplate/scripts"

If you use the *TCSH* shell, typically you would edit your
`~/.cshrc`, `~/.tcshrc` or `~/.login` files to contain the following lines:

    setenv PATH "$PATH:$HOME/moltemplate/moltemplate"
    setenv PATH "$PATH:$HOME/moltemplate/moltemplate/scripts"

After making these changes, you may need to start a new terminal (shell) for the changes to take effect.  If you do not know what a `PATH` environment variable is and are curious, read:
    http://www.linfo.org/path_env_var.html
(I receive this question often.)

*(Warning:
Do not install moltemplate this way if you are using "vipster",
"cellpack2moltemplate", or other software that has a moltemplate python
dependency.  In order to be able to be able to run "import moltemplate"
within python, as these programs do, moltemplate must be installed using
pip or setuptools.)*


### WINDOWS installation suggestions

You can install both moltemplate and LAMMPS in windows, but you will first need to install the BASH shell environment on your computer.  I recommend installing [virtualbox](https://www.virtualbox.org) in windows together with a (debian-based) linux distribution with a lightweight desktop such as [xubuntu](https://xubuntu.org).  Alternatively, if you are using Windows 10 or later, you can try installing the
[Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl)
*(which is text only)*
or
[Hyper-V](https://www.nakivo.com/blog/run-linux-hyper-v/).
Otherwise, if you are using an older version of windows, try installing
[CYGWIN](https://www.cygwin.com/) instead.

To use LAMMPS and moltemplate, you will also need to install (and learn
how to use) a text editor.  (Word, Wordpad, and Notepad will not work.)
If you are **NOT using WSL**, then you can use popular graphical text editors
such as Atom, Sublime, Notepad++, VSCode,
and the graphical versione of emacs and vim.
([Don't use these editors to edit files within the WSL environment.](https://www.reddit.com/r/bashonubuntuonwindows/comments/6bu1d1/since_we_shouldnt_edit_files_stored_in_wsl_with/))
If you **ARE using WSL** then you are restricted to using non-graphical text
editors which you can safely install and run from within the WSL terminal.
These include: **nano**, **ne**, **emacs** (the text version),
**vim** (the text version), and **jove**.


## License

With the exception of one file
([ttree_lex.py](./moltemplate/ttree_lex.py)),
moltemplate is available under the terms of the [MIT license](LICENSE.md).

The remaining file, ([ttree_lex.py](./moltemplate/ttree_lex.py)),
is a modified version of the 
[shlex.py](https://docs.python.org/3/library/shlex.html) library,
which was released using the
[PSF license](https://docs.python.org/3/license.html).
Hence [ttree_lex.py](./moltemplate/ttree_lex.py) must also use this license.
(*The PSF is not a copyleft license.
It is similar to the BSD and MIT licenses and
[is compatible with the the GPL license](https://docs.python.org/3/license.html).)*


## Funding

Moltemplate is currently funded by NIH grant T32-AI007354-29
(and previously by HSFP grant RGP0014/2014 and NSF grant NSF-MCB-1158577).
