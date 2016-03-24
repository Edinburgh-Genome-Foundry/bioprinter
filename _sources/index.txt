Bioprinter
========

Print images with colored bacteria and yeast.

This implements the `bioprint` function, which takes an image and writes a CSV
file that the Labcyte Echo dispenser can use to print the pictures on a plate
using yeast, coli, ...

Written by Valentin for the Edinburgh Genome Foundry. The code is released on Github_ under the MIT licence. Everyone is welcome to contribute.

Original idea and Matlab code by Mike Shen:
https://github.com/mshen5/BioPointillism


Installation
--------------

If you have PIP installed: ::

    (sudo) pip install ez_setup bioprinter

Or unzip the source code in a directory and type in a terminal: ::

    sudo python setup.py install


Example of code
------------------


Reference manual
-----------------

.. autoclass:: bioprinter.bioprinter

.. _Zulko: https://github.com/Zulko/
.. _Github: https://github.com/Edinburgh-Genome-Foundry/bioprinter
