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

    For instance 0->A, 1->B, 2->C, ... 26->AA, 27->AB, ... etc.
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
    """Generate a CSV file for Echo printing of an image.

    This function generates a CSV file for the Echo liquid
    handler to bioprint a given picture, using specified color wells.

    Parameters
    ----------
    image_filename : str
        The path to the image file. The image can be any size and format, but
        should be suitable for low resolution yeast printing. Images taller than
        they are wide will automatically be rotated 90 degrees to maximize
        resolution while preserving aspect ratio.

    output_filename : str
        The name of the CSV file for the Echo.

    bg_color : tuple
        A triplet (R,G,B) of 0-255 integers indicating the background color of the original image (no pigment).

    pigments_wells : dict
        A dictionary of well names and the corresponding pigments (
        e.g., {"A1": [0, 10, 20], "B1": [...]}). Only one well per pigment is
        supported currently.

    resolution : tuple, optional
        Resolution (width, height) of the printing plate. You must define a
        plate with these exact same characteristics using the Echo software.
        Default is (192, 128), equivalent to twice the resolution of a
        1536-well plate. The aspect ratio of the image is preserved.

    transfer_volume : float, optional
        Volume in microliters of liquid used per pixel, default is 2.5 μL.

    pigment_well_capacity : float
        Volume in microliters that each pigment well can dispense. Raises an
        error if required pigment for any color exceeds the content of the well,
        i.e. if ``transfer_volume * number_pixels > well_capacity``.

    transfer_rate : int, optional
        Average number of droplet transfers per second; used to estimate printing time.

    quantified_image_filename : str, optional
        Path to save the quantified version of the picture as an image file.

    Examples
    --------
    Print the EGF logo!

    ::

        bioprint(
            image_filename="egf_logo.jpeg",
            output_filename="egf_logo.csv",
            bg_color=[255, 255, 255],  # White background
            pigments_wells={
                "A1": [0, 0, 0],  # Black
                "A2": [250, 120, 10]  # Orange
            }
        )
    """

    pigments_wells, pigments_colors = zip(*pigments_wells.items())

    # Constants of the problem
    colors = np.vstack([np.array(bg_color), np.array(pigments_colors)]).astype(float)
    resolution_w, resolution_h = resolution
    resolution_ratio = 1.0 * resolution_w / resolution_h

    image = Image.open(image_filename)
    width, height = image.size

    # IF THE PICTURE IS HIGHER THAN WIDE, CHANGE THE ORIENTATION

    if height > width:
        image = image.rotate(90, expand=1)
        height, width = width, height

    # RESIZE THE PICTURE TO THE PROVIDED RESOLUTION (KEEP THE ASPECT RATIO)

    image_ratio = 1.0 * width / height
    if (height > resolution_h) or (width > resolution_w):
        if image_ratio > resolution_ratio:
            new_width = resolution_w
            new_height = int(np.round(resolution_w / image_ratio))
        else:
            new_width = int(np.round(resolution_h * image_ratio))
            new_height = resolution_h
        image = image.resize((new_width, new_height))
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
        writer.writerow(["Source Well", "Destination Well", "Transfer Volume"])
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
