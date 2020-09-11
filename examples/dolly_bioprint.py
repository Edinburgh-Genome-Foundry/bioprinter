from bioprinter import bioprint

bioprint(
    image_filename="../tests/assets/dolly.jpeg",
    output_filename="dolly.csv",
    bg_color=[0, 0, 255],  # blue background represents empty wells
    pigments_wells={
        "A1": [0, 0, 0],  # black yeast in source well A1
        "A2": [250, 120, 10],  # orange yeast in well A2
        "A3": [255, 255, 255],  # white yeast in well A3
    },
    quantified_image_filename="dolly_preview.png",
)
