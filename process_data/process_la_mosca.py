from utils import preserve_georef
import rasterio
import matplotlib.pyplot as plt
BASEPATH = "/home/felipe/MiDrive/GEE_Exports/la_mosca"


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

if __name__ == "__main__":
    create_ndvi_from_la_mosca()










