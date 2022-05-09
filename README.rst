.. raw:: html

    <p align="center">
    <img alt="Bioprinter logo" title="Bioprinter" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/bioprinter/master/docs/_static/images/title.png" width="550">
    <br /><br />
    </p>


BioPrinter
==========

.. image:: https://github.com/Edinburgh-Genome-Foundry/bioprinter/actions/workflows/build.yml/badge.svg
    :target: https://github.com/Edinburgh-Genome-Foundry/bioprinter/actions/workflows/build.yml
    :alt: GitHub CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/bioprinter/badge.svg?branch=master
   :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/bioprinter?branch=master


Bioprinter (webpage here_) is a Python package for producing living art. It transforms an image into files that a liquid dispenser can use to *print* the image to a plate using pigmented yeast or bacteria.

Here are two examples of bio-art:

.. figure:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/bioprinter/master/docs/_static/images/bioprint_dolly.jpeg
    :align: center

    Dolly drawn with baker yeast (white), violacein-producing yeast (black), and carotene-producing yeast (orange).


.. figure:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/bioprinter/master/docs/_static/images/bioprint_england.jpeg
    :align: center

    British flag drawn with 3 different strains of the bacterium *E. coli*.

These bio-prints (and many others!) were presented at the University of Edinburgh's SynthSys Open days 2016 (strain selection and acoustic printing by Paulina Kanigowska).

Bioprinter is released on Github_ under the MIT licence (Copyright 2015 Edinburgh Genome Foundry), everyone is welcome to contribute!

Bioprinter was written at the Edinburgh Genome Foundry by Zulko_ after an original idea and Matlab code by Mike Shen (`project on Github <https://github.com/mshen5/BioPointillism>`_).

Installation
------------

If you have PIP installed: ::

    pip install ez_setup bioprinter

Or unzip the source code in a directory and type in a terminal: ::

    python setup.py install


Usage
-----

The image file to be printed can have any resolution, but note that the width/height ratio of the plate the image is printed on is 1.5. Ensure that a specific color is used to mark the un-pigmented background of the image, here we use blue:

.. figure:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/bioprinter/master/docs/_static/images/dolly.jpeg
    :align: center

Run the following code in Python or save in ``dolly.py``:

.. code:: python

    from bioprinter import bioprint

    bioprint(
        image_filename="/path/to/image/dolly.jpeg",
        output_filename="dolly.csv",
        bg_color=[0, 0, 255],  # blue background represents empty wells
        pigments_wells={"A1": [0, 0, 0],        # black yeast in source well A1
                        "A2": [250, 120, 10],   # orange yeast in well A2
                        "A3": [255, 255, 255]}, # white yeast in well A3
        quantified_image_filename="dolly_preview.jpeg"
    )

The saved script can be executed in a terminal with ``python dolly.py``. This will produce a ``dolly.csv`` file as well as a preview image of the final printing (so that you can check if the image looks good at this low resolution).

Prepare a source plate with the right pigmented yeasts in wells A1, A2, A3, use an agar plate as the destination plate, and feed ``dolly.csv`` to the `Labcyte Echo Acoustic Liquid Handler <https://www.labcyte.com/products/liquid-handling/echo-liquid-handlers>`_ (tested with Labcyte Echo 555 Series). Once the printing is finished, incubate 2 days at 30C (it would be one day at 37C for bacteria). Enjoy the result!


.. _here: http://edinburgh-genome-foundry.github.io/bioprinter/
.. _Zulko: https://github.com/Zulko/
.. _Github: https://github.com/Edinburgh-Genome-Foundry/bioprinter
