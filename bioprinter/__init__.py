"""Bioprinter: print images with colored bacteria and yeast.

This implements the `bioprint` function, which takes an image and writes a CSV
file that the Labcyte Echo dispenser can use to print the pictures on a plate
using yeast, coli, ...

Written by Valentin for the Edinburgh Genome Foundry.
Original idea and Matlab code by Mike Shen:

https://github.com/mshen5/BioPointillism
"""
# __all__ = []

from .bioprinter import bioprint

from .version import __version__
