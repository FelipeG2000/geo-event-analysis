import ee
import time

def generate_roi_from_points(ee_client: ee, points: list):
    """
    Generates a Region of Interest (ROI) from a list of points.

    Args:
        ee_client: Google Earth Engine module.
        points (list): List of [longitude, latitude] pairs.

    Returns:
        ee.Geometry: A convex hull polygon enclosing the points.
    """
    if not points or len(points) < 3:
        raise ValueError("At least three points are required to generate a valid ROI.")

    return  ee_client.Geometry.MultiPoint(points).convexHull()


def get_satellite_collection(ee_client, collection_id: str, start: str, end: str, points: list = None, roi = None,
    bands: list = None):
    """
    Retrieves a filtered ImageCollection from Google Earth Engine, supporting both points and predefined ROI.

    Args:
        ee_client: Google Earth Engine module.
        collection_id (str): The ID of the satellite image collection (e.g., "COPERNICUS/S2").
        start (str): Start date in "YYYY-MM-DD" format.
        end (str): End date in "YYYY-MM-DD" format.
        points (list, optional): List of [longitude, latitude] pairs for spatial filtering. Default is None.
        roi (ee.Geometry, optional): Predefined region of interest. Default is None.
        bands (list, optional): List of band names to select from the collection. Default is None.

    Returns:
        ee.ImageCollection: The filtered image collection.
    """
    if points is None and roi is None:
        raise ValueError("roi or points must be provided.")

    collection = ee_client.ImageCollection(collection_id).filterDate(start, end)

    # Generate ROI if points are provided
    if points and roi is None:
        roi = generate_roi_from_points(ee_client, points)

    collection = collection.filterBounds(roi)

    if bands:
        collection = collection.select(bands)

    return collection

def reduce_collection(collection: ee.ImageCollection, method: str = "mean") -> ee.Image:
    """
    Applies statistical reduction to an ImageCollection.

    Args:
        collection (ee.ImageCollection): The image collection to reduce.
        method (str, optional): The reduction method ("mean" or "median"). Default is "mean".

    Returns:
        ee.Image: A single reduced image.
    """
    if method == "mean":
        return collection.mean()
    elif method == "median":
        return collection.median()
    else:
        raise collection.first()


def mask_landsat_8sr(image):
    """
    Applies cloud and shadow masking to a Landsat 8 Surface Reflectance (SR) image
    using the QA_PIXEL band. Also scales optical and thermal bands.

    Args:
        image (ee.Image): Landsat 8 SR image.

    Returns:
        ee.Image: Cloud-masked and scaled Landsat 8 image.
    """
    # Bitmasks for clouds and cloud shadows (from QA_PIXEL band)
    cloud_shadow_bit_mask = (1 << 4)  # Bit 4: Cloud shadow
    clouds_bit_mask = (1 << 3)       # Bit 3: Clouds

    # Select QA_PIXEL band
    qa = image.select('QA_PIXEL')

    # Create mask
    cloud_shadow_mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0)
    clouds_mask = qa.bitwiseAnd(clouds_bit_mask).eq(0)
    mask = cloud_shadow_mask.And(clouds_mask)

    # Apply the mask to the image
    image = image.updateMask(mask)

    # Scale optical bands (SR_B.*) to reflectance values
    optical_bands = image.select('SR_B.*').multiply(0.0000275).add(-0.2)

    # Scale thermal bands (ST_B.*) to temperature values in Kelvin
    thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)

    # Replace original bands with scaled versions
    return image.addBands(optical_bands, None, True).addBands(
        thermal_bands, None, True).copyProperties(image, ["system:time_start"])


def mask_sentinel2_sr(image):
    """
    Applies a cloud and shadow mask to a Sentinel-2 image
    using the Scene Classification Layer (SCL) band. It also scales reflectance values.

    Args:
        image (ee.Image): Sentinel-2 SR image.

    Returns:
        ee.Image: Cloud-free and scaled Sentinel-2 image.
    """

    # Select the Scene Classification Layer (SCL) band
    scl = image.select('SCL')

    # Create the mask by removing clouds (9, 10) and cloud shadows (3)
    cloud_mask = scl.neq(9).And(scl.neq(10)).And(scl.neq(3))

    # Apply the mask to the image
    image = image.updateMask(cloud_mask)

    # Scale all bands that start with "B" (to ensure none are lost)
    optical_bands = image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']).multiply(0.0001)

    # Replace original bands with the scaled ones
    return image.addBands(optical_bands, None, True).copyProperties(image, ["system:time_start"])


def filter_landsat8_sr_st_bands(bands):
    """Filters SR (Surface Reflectance) and ST (Surface Temperature) bands from a Landsat 8 band collection."""
    return list(filter(lambda band: band.startswith(('SR', 'ST')), bands))


def filter_sentinel2_reflected_bands(bands):
    """Filters SR (Surface Reflectance) and ST (Surface Temperature) bands from a Landsat 8 band collection."""
    return list(filter(lambda band: band.startswith('B'), bands))


def get_landsat8_visualization_params(band_name):
    """Returns visualization parameters based on the Landsat 8 band type."""
    visualization_defaults = {
        'SR': {'min': 0, 'max': 1},
        'ST': {'min': 270, 'max': 310}
    }
    return visualization_defaults.get(band_name[:2], {'min': 0, 'max': 255})  # Default for other bands


def generate_date_ranges(start_year, end_year, frequency="quarterly"):
    """
    Generates date ranges based on the selected frequency.

    :param start_year: Start year for the date range.
    :param end_year: End year for the date range.
    :param frequency: Frequency of the date ranges. Options: "monthly", "bimonthly", "quarterly", "four_months", "six_months".
    :return: List of tuples with start and end dates.
    """
    frequencies = {
        "monthly": [('-01-01', '-01-31'), ('-02-01', '-02-28'), ('-03-01', '-03-31'), ('-04-01', '-04-30'),
                    ('-05-01', '-05-31'), ('-06-01', '-06-30'), ('-07-01', '-07-31'), ('-08-01', '-08-31'),
                    ('-09-01', '-09-30'), ('-10-01', '-10-31'), ('-11-01', '-11-30'), ('-12-01', '-12-31')],
        "bimonthly": [('-01-01', '-02-28'), ('-03-01', '-04-30'), ('-05-01', '-06-30'), ('-07-01', '-08-31'),
                      ('-09-01', '-10-31'), ('-11-01', '-12-31')],
        "quarterly": [('-01-01', '-03-31'), ('-04-01', '-06-30'), ('-07-01', '-09-30'), ('-10-01', '-12-31')],
        "four_months": [('-01-01', '-04-30'), ('-05-01', '-08-31'), ('-09-01', '-12-31')],
        "six_months": [('-01-01', '-06-30'), ('-07-01', '-12-31')]
    }
    return [(str(year) + start, str(year) + end) for year in range(start_year, end_year + 1) for start, end in
            frequencies[frequency]]


def monitor_task(task):
    """
    Monitors the status of an Earth Engine export task.

    :param task: The Earth Engine task to monitor.
    """
    while task.active():
        status = task.status()
        state = status.get('state')

        if state == "FAILED":
            print(f"Error: {status.get('error_message')}")
            break
        elif state == "CANCELLED":
            print("The export task was cancelled.")
            break
        time.sleep(1)
