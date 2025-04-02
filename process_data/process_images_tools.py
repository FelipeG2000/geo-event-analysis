import rasterio
import numpy as np

class GeoImageProcessor:
    """
    Handles georeferenced image processing efficiently.
    - Loads an image with rasterio.
    - Applies processing functions while preserving metadata.
    - Saves the processed image with its original georeferencing.
    """

    def __init__(self, image_path):
        """
        Initializes the processor with an image.

        Args:
            image_path (str): Path to the georeferenced image.
        """
        self.image_path = image_path
        self.data, self.profile = self._load_image()


    def _load_image(self):
        """Loads the image and stores its metadata."""
        with rasterio.open(self.image_path) as src:
            profile = src.profile
            data = src.read(1).astype(np.float32)  # Load first band as float32
            self.meta = src.meta
        return data, profile

    def apply(self, processing_function, *args, **kwargs):
        """
        Applies a function to process the image.

        Args:
            processing_function (function): A function that modifies the image.
        """
        self.data = processing_function(self.data, *args, **kwargs)

    def save(self, output_path):
        """
        Saves the processed image with the original georeferencing.

        Args:
            output_path (str): Path to save the new image.
        """
        self.meta.update(dtype=np.uint8, count=1)

        with rasterio.open(output_path, 'w', **self.meta) as dst:
            dst.write(self.data, 1)
            dst.close()

