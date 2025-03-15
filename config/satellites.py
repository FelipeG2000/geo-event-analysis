"""
Module: satellites.py

This module defines classes representing Earth observation satellites, each with
its own unique collection ID and relevant processing methods.

Classes:
    - Satellite: Base class for all Earth observation satellites.
    - Landsat8: Represents the Landsat 8 satellite with cloud filtering capabilities.
    - Sentinel2: Represents the Sentinel-2 satellite with cloud filtering capabilities.
    - Sentinel1: Represents the Sentinel-1 satellite with radar backscatter processing.

Example usage:
    from satellites import Landsat8, Sentinel2

    # Get satellite collection ID without instantiation
    collection_id = Landsat8.get_collection()
    print(collection)  # Output: LANDSAT/LC08/C01/T1_SR
"""


class Satellite:
    """
    Base class representing an Earth observation satellite.
    Defines common attributes and methods for different satellites.
    """

    collection: str  # Collection identifier for the satellite

    def __init__(self, name: str):
        """
        Initialize a Satellite object.

        :param name: Name of the satellite.
        """
        self.name = name

    @classmethod
    def get_collection(cls) -> str:
        """
        Get the collection ID associated with the satellite.

        :return: Collection ID as a string.
        """
        return cls.collection

    def __repr__(self) -> str:
        """
        String representation of the satellite.

        :return: The satellite's name.
        """
        return f"{self.name} ({self.collection})"


class Landsat8(Satellite):
    """
    Represents the Landsat 8 satellite, which provides multi-spectral
    imagery and cloud filtering capabilities.
    """
    collection = 'LANDSAT/LC08/C02/T1_L2'

    def __init__(self):
        """Initialize the Landsat 8 satellite."""
        super().__init__("Landsat-8", self.collection)

    def filter_clouds(self, image):
        """
        Apply cloud filtering specific to Landsat-8 imagery.

        :param image: The input image to process.
        :return: Cloud-filtered image.
        """
        # Placeholder for actual cloud filtering logic
        return image


class Sentinel2(Satellite):
    """
    Represents the Sentinel-2 satellite, which captures multispectral images
    and provides cloud filtering functionality.
    """

    collection = "COPERNICUS/S2_SR"

    def __init__(self):
        """Initialize the Sentinel-2 satellite."""
        super().__init__("Sentinel-2", self.collection)

    def filter_clouds(self, image):
        """
        Applies cloud masking to Sentinel-2 images.

        :param image: Input image.
        :return: Processed image with clouds filtered out.
        """
        # Placeholder for actual cloud filtering logic
        return image


class Sentinel1(Satellite):
    """
    Represents the Sentinel-1 satellite with radar capabilities.
    """

    collection = "COPERNICUS/S1_GRD"

    def __init__(self):
        """Initialize the Sentinel-1 satellite."""
        super().__init__("Sentinel-1", self.collection)

    def process_backscatter(self, image):
        """
        Processes Sentinel-1 images to extract radar backscatter data.

        :param image: Input radar image.
        :return: Processed radar image with applied enhancements.
        """
        # Placeholder for actual backscatter processing logic
        return image