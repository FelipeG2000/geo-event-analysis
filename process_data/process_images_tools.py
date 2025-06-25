import rasterio
import numpy as np

from keras.models import load_model

BASEPATH ="/home/felipe/MiDrive/GEE_Exports/"
NDWI_DIR = "ndwi"
NDVI_DIR = "ndvi"
NDBI_DIR = "ndbi"
TILE_SIZE = 512
OVERLAP = 0

OUTPUT_VV_DESPECKLED = "VV_despeckled"
OUTPUT_VH_DESPECKLED = "VH_despeckled"
MODEL_PATH = 'Autoencoder_despeckling.h5'
model = load_model(MODEL_PATH, compile=False)


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
        #self.meta.update(dtype=np.uint8, count=1)

        with rasterio.open(output_path, 'w', **self.meta) as dst:
            dst.write(self.data, 1)
            dst.close()


def preprocess(tile):
    tile = tile.astype(np.float32) / 255.0
    return np.reshape(tile, (1, TILE_SIZE, TILE_SIZE, 1))


def embed_in_center(image):
    """
    Puts a small image in the center of a TILE_SIZE x TILE_SIZE black canvas.
    """
    canvas = np.zeros((TILE_SIZE, TILE_SIZE), dtype=image.dtype)
    h, w = image.shape
    y_offset = (TILE_SIZE - h) // 2
    x_offset = (TILE_SIZE - w) // 2
    canvas[y_offset:y_offset+h, x_offset:x_offset+w] = image
    return canvas, y_offset, x_offset, h, w


def filter_large_image(image):
    """
    Tiles a large image, denoises each tile with model, stitches them back.
    Handles edges robustly: tiles larger or smaller than image size.
    """
    h, w = image.shape
    result = np.zeros_like(image, dtype=np.float32)

    step = TILE_SIZE - OVERLAP

    for i in range(0, h, step):
        for j in range(0, w, step):

            # Determine actual tile region
            height = min(TILE_SIZE, h - i)
            width = min(TILE_SIZE, w - j)

            tile = image[i:i+height, j:j+width]

            # Always predict on 512x512 padded tile
            padded_tile = np.zeros((TILE_SIZE, TILE_SIZE), dtype=tile.dtype)
            padded_tile[:height, :width] = tile

            pred = model.predict(preprocess(padded_tile), verbose=0)
            filtered = pred.reshape(TILE_SIZE, TILE_SIZE) * 255.0

            # Paste back only the valid region
            result[i:i+height, j:j+width] = filtered[:height, :width]

    return np.clip(result, 0, 255).astype(np.uint8)



def scale_to_8bit(image):
    """
    Converts an image with values in range [-1, 1] to [0, 255] for visualization.
    """
    image = np.nan_to_num(image, nan=0, posinf=1, neginf=0)  # Remove NaNs again just in case
    image = (image + 1) / 2  # Scale from [-1, 1] to [0, 1]
    image = np.clip(image * 255, 0, 255).astype(np.uint8)  # Scale to [0, 255] safely
    return image


def calculate_index(band1, band2):
    """Computes a normalized difference index like NDVI or NDWI."""
    return (band1 - band2) / (band1 + band2 + 1e-6)  # Avoid division by zero