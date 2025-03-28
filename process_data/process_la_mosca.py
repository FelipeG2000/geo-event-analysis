import rasterio
import matplotlib.pyplot as plt
import numpy as np

from process_data.process_images_tools import GeoImageProcessor

BASEPATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca/landsat8/bands"


def create_ndvi_from_la_mosca():
    with rasterio.open(BASEPATH + '/sentinel1/descending/VH/la_mosca_first_find_2017-05-01_2017-05-31.tif') as src:
        data = src.read(1)
        imagenir_profile = src.profile
        imagenir_meta = src.meta
    plt.figure(figsize=(8, 6))
    plt.imshow(data, cmap="gray")
    plt.colorbar(label="Intensity")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.show()


def calculate_index(band1, band2):
    """Computes a normalized difference index like NDVI or NDWI."""
    return (band1 - band2) / (band1 + band2 + 1e-6)  # Avoid division by zero


if __name__ == "__main__":
    image1_la_mosca = "/home/felipe/MiDrive/GEE_Exports/la_mosca/landsat8/bands/SR_B5/la_mosca_mean_2021-10-01_2021-12-31.tif"
    image2_la_mosca = "/home/felipe/MiDrive/GEE_Exports/la_mosca/landsat8/bands/SR_B4/la_mosca_mean_2021-10-01_2021-12-31.tif"
    geo_image = GeoImageProcessor(image1_la_mosca)
    geo_red = GeoImageProcessor(image2_la_mosca)

    ndvi = calculate_index(geo_image.data, geo_red.data)
    geo_image.data = ndvi
    plt.figure(figsize=(8, 6))
    plt.imshow(ndvi, cmap="Reds")
    plt.colorbar(label="Intensity")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.show()










