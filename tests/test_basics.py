import os
import tempfile
import unittest

from bioprinter import bioprint

def test_basics():
    quantified_image_filename = tempfile.mktemp(".jpeg")
    output_filename = tempfile.mktemp(".csv")

    bioprint(
        image_filename="../docs/_static/images/dolly.jpeg",
        output_filename=output_filename,
        bg_color=[0, 0, 255], # blue background represents empty wells
        pigments_wells={"A1": [0, 0, 0],  # black yeast in source well A1
                        "A2": [250, 120, 10],  # orange yeast in well A2
                        "A3": [255, 255, 255]},  # white yeast in well A3
        quantified_image_filename=quantified_image_filename
    )
    assert os.path.exists(quantified_image_filename)
    assert os.path.exists(output_filename)
