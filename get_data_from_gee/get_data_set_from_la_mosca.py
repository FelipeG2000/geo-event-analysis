from config.satellites import Landsat8, Sentinel2, Sentinel1
from utils import *
import ee
from config.ee_init import ee



POINTS_LA_MOSCA = [[-75.3845077, 6.2052735],
                  [-75.3363690, 6.2052617],
                  [-75.3359859, 6.1513562],
                  [-75.3847079, 6.1515247]]
ROI_LA_MOSCA = generate_roi_from_points(ee, POINTS_LA_MOSCA)


def get_landsat_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts Landsat 8 imagery for each date range from 2015 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2015, 2025)

    for date in dates:

        landsat_collection_la_mosca = get_satellite_collection(ee_client=ee,
                                                               collection_id=Landsat8.get_collection(),
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_LA_MOSCA)
        image = landsat_collection_la_mosca.map(mask_landsat_8sr).mean().clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of La Mosca image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of La Mosca captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"la_mosca_mean_{date[0]}_{date[1]}",
                region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_landsat_visualisation_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts Landsat 8 imagery for each date range from 2015 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2015, 2025)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'

    for date in dates:

        landsat_collection_la_mosca = get_satellite_collection(ee_client=ee,
                                                               collection_id=Landsat8.get_collection(),
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_LA_MOSCA)
        image = landsat_collection_la_mosca.map(mask_landsat_8sr).mean().clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in filter_landsat8_sr_st_bands(image.bandNames().getInfo()):
            print(f"processing the follow band {band} of La Mosca image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of La Mosca captured between {date[0]} and {date[1]}, using the {band} band."
            visualization = get_landsat8_visualization_params(band)
            task = ee.batch.Export.image.toDrive(
                image=image.select(band).visualize(**visualization),
                description=description,
                folder=f'{band}',
                fileNamePrefix=f"la_mosca_mean_{date[0]}_{date[1]}",
                region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_sentinel2_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 2 imagery for each date range from 2018 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2018, 2025)

    for date in dates:

        sentinel2_collection_la_mosca = get_satellite_collection(ee_client=ee, collection_id=Sentinel2.get_collection(),
                                                                 start=date[0], end=date[1], roi=ROI_LA_MOSCA)
        image = sentinel2_collection_la_mosca.map(mask_sentinel2_sr).mean().clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326',
                                                                                                         scale=10)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of La Mosca image in this dates {date[0]}-{date[1]}")
            description = f"Mean image La Mosca {date[0]} to {date[1]} using {band} band"
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"la_mosca_mean_{date[0]}_{date[1]}",
                region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                scale=10,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_sentinel2_visualized_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 2 imagery for each date range from 2018 to 2024.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2018, 2025)

    collection_sentinel2_path = "COPERNICUS/S2_SR_HARMONIZED"

    for date in dates:

        sentinel2_collection_la_mosca = get_satellite_collection(ee_client=ee, collection_id=Sentinel2.get_collection(),
                                                                 start=date[0], end=date[1], roi=ROI_LA_MOSCA)
        image = sentinel2_collection_la_mosca.map(mask_sentinel2_sr).mean().clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326',
                                                                                                         scale=10)
        for band in filter_sentinel2_reflected_bands(image.bandNames().getInfo()):
            print(f"processing the follow band {band} of La Mosca image in this dates {date[0]}-{date[1]}")
            description = f"Mean image La Mosca {date[0]} to {date[1]} using {band} band"
            task = ee.batch.Export.image.toDrive(
                image=image.select(band).visualize(**{'min': 0, 'max': 1}),
                description=description,
                folder=band,
                fileNamePrefix=f"la_mosca_mean_{date[0]}_{date[1]}",
                region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                scale=10,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


def get_sentinel1_descending_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 1 imagery for each date range from 2017 to 2024.
    - Filters imagery for descending orbit mode.
    - Computes the mean image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2023, 2023, 'monthly')

    for date in dates:
        sentinel1_collection_la_mosca = (
            get_satellite_collection(ee_client=ee, collection_id=Sentinel1.get_collection(),
                                     start=date[0], end=date[1], roi=ROI_LA_MOSCA)
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
        )

        first_image = sentinel1_collection_la_mosca.first()

        if first_image.getInfo():
            image = first_image.clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326', scale=10)
            bands = image.bandNames().getInfo()
            filtered_bands = filter_sentinel1_bands(bands) if has_sentinel1_vv_vh_bands(bands) else []

            for band in filtered_bands:
                print(f"Processing band {band} for La Mosca image ({date[0]} - {date[1]})")
                description = f"First image La Mosca {date[0]} to {date[1]} using {band} band"
                task = ee.batch.Export.image.toDrive(
                    image=image.select(band).visualize(**{'min': -25, 'max': 5}),
                    description=description,
                    folder=band,
                    fileNamePrefix=f"la_mosca_first_find_{date[0]}_{date[1]}",
                    region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                    scale=10,
                    crs='EPSG:4326',
                    maxPixels=1e13
                )
                task.start()
                monitor_task(task)
        else:
            print(f"No Sentinel-1 images found for La Mosca in date range {date[0]} - {date[1]}")


def get_sentinel1_ascending_data_set_from_la_mosca():
    """
    Retrieves and exports mean Landsat images of the La Mosca region for multiple date ranges.

    - Defines a region of interest (ROI) based on predefined coordinates.
    - Extracts sentinel 1 imagery for each date range from 2017 to 2024.
    - Filters imagery for ascending orbit mode.
    - Computes the first image for each period.
    - Exports each band separately to Google Drive (organized by filename).

    The exported files follow this naming convention:
    - File name: `la_mosca_mean_{start_date}_{end_date}`
    """

    dates = generate_date_ranges(2017, 2025, 'monthly')

    for date in dates:

        sentinel1_collection_la_mosca = (get_satellite_collection(ee_client=ee, collection_id=Sentinel1.get_collection(),
                                                                 start=date[0], end=date[1], roi=ROI_LA_MOSCA)
                                         .filter(ee.Filter.eq('instrumentMode', 'IW'))
                                         .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING')))
        image = sentinel1_collection_la_mosca.mean().clip(ROI_LA_MOSCA).reproject(crs='EPSG:4326', scale=10)
        bands = image.bandNames().getInfo()
        filtered_bands = filter_sentinel1_bands(bands) if has_sentinel1_vv_vh_bands(bands) else []
        for band in filtered_bands:
            print(f"processing the follow band {band} of La Mosca image in this dates {date[0]}-{date[1]}")
            description = f"Mean image La Mosca {date[0]} to {date[1]} using {band} band"
            task = ee.batch.Export.image.toDrive(
                image=image.select(band).visualize(**{'min': -25, 'max': 5}),
                description=description,
                folder=band,
                fileNamePrefix=f"la_mosca_first_find_{date[0]}_{date[1]}",
                region=ROI_LA_MOSCA.bounds().getInfo()['coordinates'],
                scale=10,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
            monitor_task(task)


if __name__ == '__main__':
    get_sentinel1_descending_data_set_from_la_mosca()