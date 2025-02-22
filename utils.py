import ee


def generate_roi_from_points(ee_client, points: list):
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

    return  ee_client.Geometry.MultiPoint(points)


def get_satellite_collection(
    ee_client,
    collection_id: str,
    start: str,
    end: str,
    points: list = None,
    roi = None,
    bands: list = None
):
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
    if not points and not roi:
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

