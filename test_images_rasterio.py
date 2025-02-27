import rasterio
import matplotlib.pyplot as plt


def test_image(image_path: str, band: int = 1):
    """Displays a specific band of a raster image and prints its metadata."""
    try:
        with rasterio.open(image_path) as src:
            data = src.read(band)
            meta = src.meta
            width, height = src.width, src.height
            raster_crs = src.crs
            transform = src.transform

        # Print relevant raster information
        print("\n--- Raster Information ---")
        print(f"📂 File: {image_path}")
        print(f"📏 Dimensions: {width} x {height} (Width x Height)")
        print(f"🛰️ CRS (Coordinate Reference System): {raster_crs}")
        print(f"🗺️ Transform: {transform}")

        # Visualization
        plt.figure(figsize=(8, 6))
        plt.imshow(data, cmap="gray")
        plt.colorbar(label="Intensity")
        plt.title(f"Image: {image_path}\nBand: {band}")
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.show()

    except rasterio.errors.RasterioIOError:
        print(f"❌ Error: Could not open file '{image_path}'.")
    except IndexError:
        print(f"❌ Error: The image does not have band {band}.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_image("imagen_name.tif", band=1)
