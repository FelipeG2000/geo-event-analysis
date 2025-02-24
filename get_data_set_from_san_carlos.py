from utils import *
import time
import ee

ee.Authenticate()
ee.Initialize(project="investigation-project-pipe")


def get_landsat_data_set_from_san_carlos():
    dates = [(str(AAAA) + MM1, str(AAAA) + MM2) for AAAA in range(2015, 2025)
             for MM1, MM2 in zip(['-01-01', '-04-01', '-07-01', '-10-01'],
                                 ['-03-31', '-06-30', '-09-30', '-12-31'])]

    points_san_carlos = [[-75.0174891, 6.2002711],
                         [-74.9691066, 6.2007604],
                         [-74.9686103, 6.1675056],
                         [-75.0172356, 6.1670877]]

    roi_san_carlos = generate_roi_from_points(ee, points_san_carlos)

    collection_landsta_path = 'LANDSAT/LC08/C02/T1_L2'
    for date in dates:

        landsat_collection_san_carlos = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsta_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=roi_san_carlos)
        image = landsat_collection_san_carlos.map(mask_landsat_8sr).mean().clip(roi_san_carlos).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of san carlos image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of San carlos captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"San_carlos_mean_{date[0]}_{date[1]}",
                region=roi_san_carlos.bounds().getInfo()['coordinates'],
                scale=30,
                crs='EPSG:4326',
                maxPixels=1e13
            )
            task.start()
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


if __name__ == '__main__':
    get_landsat_data_set_from_san_carlos()