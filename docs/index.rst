


Bioprinter Documentation
=========================

.. image:: _static/images/title.png
   :width: 550px
   :align: center

Bioprinter is a Python package for producing living art. It transforms an image into files that a liquid dispenser can use to *print* the image to a plate using pigmented yeast or bacteria.

Here are two examples of bio-art:

.. figure:: _static/images/bioprint_dolly.jpeg
    :align: center

    Dolly drawn with baker yeast (white), violacein-producing yeast (black), and carotene-producing yeast (orange).


.. figure:: _static/images/bioprint_england.jpeg
    :align: center

    England flag drawn with 3 different strains of the bacterium *E. coli*.


Bioprinter is released on Github_ under the MIT licence (Copyright 2015 Edinburgh Genome Foundry), everyone is welcome to contribute!

Bioprinter was written at the Edinburgh Genome Foundry by Zulko_ after an original idea
and Matlab code by Mike Shen at the Boeke Lab (`project on Github <https://github.com/mshen5/BioPointillism>`_).


Installation
------------

If you have PIP installed: ::

    (sudo) pip install ez_setup bioprinter

Or unzip the source code in a directory and type in a terminal: ::

    sudo python setup.py install


Usage
-----

The image file to be printed can have any resolution, but note that the width/height ratio of the plate the image is printed on is 1.5. Ensure that a specific color is used to mark the un-pigmented background of the image, here we use blue:

.. figure:: _static/images/dolly.jpeg
    :align: center

Run the following code in Python or save in ``dolly.py``:
::
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

.. figure:: _static/images/dolly_preview.png
    :align: center

Prepare a source plate with the right pigmented yeasts in wells A1, A2, A3, use an agar plate as the destination plate, and feed ``dolly.csv`` to the `Labcyte Echo <http://www.labcyte.com/products/liquidhandling/echo-555-liquid-handler>`_. Once the printing is finished, incubate 2 days at 30C (it would be one day at 37C for bacteria). Enjoy the result!

Reference manual
----------------

.. autofunction:: bioprinter.bioprint

.. toctree::
    :maxdepth: 1
    self

.. raw:: html

    <a href="https://twitter.com/share" class="twitter-share-button"
    data-text="BioPrinter - A Python module for printing with living matter" data-size="large" data-hashtags="Bioprinting">Tweet
    </a>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
    if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';
    fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
    </script>
    <iframe src="http://ghbtns.com/github-btn.html?user=Edinburgh-Genome-Foundry&repo=bioprinter&type=watch&count=true&size=large"
    allowtransparency="true" frameborder="0" scrolling="0" width="152px" height="30px" margin-bottom="30px"></iframe>

.. _Zulko: https://github.com/Zulko/
.. _Github: https://github.com/Edinburgh-Genome-Foundry/bioprinter
