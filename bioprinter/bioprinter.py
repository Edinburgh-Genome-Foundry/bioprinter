"""Bioprinter: print images with colored bacteria and yeast.

This implements the `bioprint` function, which takes an image and writes a CSV
file that the Labcyte Echo dispenser can use to print the pictures on a plate
using yeast, coli, ...

Written by Zulko at the Edinburgh Genome Foundry.

Original idea and Matlab code by Mike Shen:
https://github.com/mshen5/BioPointillism
"""

from collections import Counter
import csv

import numpy as np
from PIL import Image


def _rownumber_to_rowname(num):
    """Return the row name corresponding to the row number.

    For instance 0-> A, 1->B, 2->C, ... 26->AA, 27->AB, ... etc.
    """
    if num < 26:
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[num]
    else:
        return "".join(
            [_rownumber_to_rowname(int(num / 26) - 1), _rownumber_to_rowname(num % 26)]
        )


def bioprint(
    image_filename,
    output_filename,
    bg_color,
    pigments_wells,
    resolution=(192, 128),
    transfer_volume=2.5,
    pigment_well_capacity=25000,
    transfer_rate=150,
    quantified_image_filename=None,
):
    """Generate a CSV that can be used in the Echo to print the given picture.

    Example
    =======

        # Let's print the EGF logo !
        bioprint(
             image_filename = "egf_logo.jpeg",
             output_filename = "egf_logo.csv",
             bg_color=[255,255,255], # The background of the image is white
             pigments_wells= { "A1": [0,0,0],  # black
                               "A2": [250,120, 10] }  # orange
        )

    Parameters
    ==========

    image_filename
      The path the image file to be printed. Can be virtually any size
      and file format, but make sure the image is well adapted to low
      resolution yeast printing. If the picture is higher than wide it will
      be automatically rotated 90 degrees so as to maximize its resolution on
      the plate (the image aspect ratio is conserved).

    output_filename
      The name of the CSV file written by the function, that will then
      be fed to the Echo.

    bg_color
       A triplet (R,G,B) of 0-255 integers indicating which color
       of the original image represents the background (no pigment)

    pigments_wells
      A dictionary of well names and the corresponding pigments. For
      instance {"A1": [0,10,20], "B1":...}. Only one well per pigment
      is currently supported.

    resolution
      Resolution (width, height) of the printing plate. You must define a
      plate with these exact same characteristics using the Echo
      software. Default is (192, 128) (twice the resolution of a
      1536-well plate). The aspect ratio of the original image is always
      automatically conserved.

    transfer_volume
      How many microliters of liquid should be used for each pixel.
      The default, 2.5, works very well and is also the lowest possible
      value on our Echo.

    pigment_well_capacity
      Volume in microliters that one pigment well can dispense. The
      function raises an error if the total number of pixels for one
      color exceeds the content of one pigment well, i.e. if
          transfer_volume * number_pixels > well_capacity

    transfer_rate
      Average number of droplet transfers per second, used only to
      give an estimate of the time required for printing.

    quantified_image_filename
      If a path is provided, the quantified picture will be saved as an
      image file under this name.
    """
    pigments_wells, pigments_colors = zip(*pigments_wells.items())

    # Constants of the problem
    colors = np.vstack([np.array(bg_color), np.array(pigments_colors)]).astype(float)
    resolution_w, resolution_h = resolution
    resolution_ratio = 1.0 * resolution_w / resolution_h

    image = Image.open(image_filename)
    height, width = image.size

    # IF THE PICTURE IS HIGHER THAN WIDE, CHANGE THE ORIENTATION

    if height > width:
        image = image.rotate(90, expand=1)
        height, width = width, height

    # RESIZE THE PICTURE TO THE PROVIDED RESOLUTION (KEEP THE ASPECT RATIO)

    image_ratio = 1.0 * width / height
    if (height > resolution_h) or (width > resolution_w):
        if image_ratio > resolution_ratio:
            new_size = (int(resolution_w / image_ratio), resolution_w)
            image = image.resize(new_size)
        else:
            new_size = (resolution_h, int(resolution_h * image_ratio))
            image = image.resize(image, new_size)
    image = np.array(image)

    # QUANTIFY THE ORIGINAL IMAGE WITH THE PROVIDED PIGMENTS COLORS

    image_color_distances = np.dstack(
        [
            ((1.0 * image - color.reshape((1, 1, 3))) ** 2).sum(axis=2)
            for color in colors
        ]
    )
    # now image_color_distances[x,y,i] represents the distance between color
    # i and the color of the image pixel at [x,y].
    image_quantnumbers = image_color_distances.argmin(axis=2)

    # CHECK THAT WE WILL HAVE ENOUGH COLORANT

    max_pixels_per_color = pigment_well_capacity / transfer_volume
    counter = Counter(image_quantnumbers.flatten())
    for color, count in counter.items():
        if (color != 0) and (count > max_pixels_per_color):
            err_message = "Too much pixels of color #%d. " % (
                color
            ) + "Counted %d, max authorized %d" % (count, max_pixels_per_color)
            raise ValueError(err_message)

    # WRITE THE CSV
    # TO DO: write the wells in an order that miminizes the Echo's travels.
    with open(output_filename, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([u"Source Well", u"Destination Well", u"Transfer Volume"])
        for i, row in enumerate(image_quantnumbers):
            for j, color in enumerate(row):
                if color != 0:
                    writer.writerow(
                        [
                            pigments_wells[color - 1],  # source well
                            _rownumber_to_rowname(i) + str(j + 1),  # target "well"
                            transfer_volume,
                        ]
                    )

    # ESTIMATE THE PRINTING TIME

    total_pixels = sum([count for (color, count) in counter.items() if color > 0])
    print(
        "%d pixels will be printed in appr. %.1f minutes"
        % (total_pixels, total_pixels / transfer_rate)
    )

    # SAVE THE QUANTIFIED VERSION OF THE IMAGE IF A FILENAME IS PROVIDED

    if quantified_image_filename is not None:
        image_quantified = np.array([colors[y] for y in image_quantnumbers])
        pil_image = Image.fromarray(image_quantified.astype("uint8"))
        pil_image.save(quantified_image_filename)
