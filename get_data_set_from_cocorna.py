from utils import *
import time
import ee

ee.Authenticate()
ee.Initialize(project="investigation-project-pipe")


POINTS_COCORNA = [[-75.205, 6.108],
                  [-75.160, 6.108],
                  [-75.205, 6.062],
                  [-75.160, 6.062]]

ROI_COCORNA = generate_roi_from_points(ee, POINTS_COCORNA)


def get_landsat_data_set_from_cocorna():
    dates = [(str(AAAA) + MM1, str(AAAA) + MM2) for AAAA in range(2015, 2025)
             for MM1, MM2 in zip(['-01-01', '-04-01', '-07-01', '-10-01'],
                                 ['-03-31', '-06-30', '-09-30', '-12-31'])]

    collection_landsat_path = 'LANDSAT/LC08/C02/T1_L2'
    for date in dates:

        landsat_collection_cocorna = get_satellite_collection(ee_client=ee,
                                                               collection_id=collection_landsat_path,
                                                               start=date[0],
                                                               end=date[1],
                                                               roi=ROI_COCORNA)
        image = landsat_collection_cocorna.map(mask_landsat_8sr).mean().clip(ROI_COCORNA).reproject(crs='EPSG:4326',
                                                                                                      scale=30)
        for band in image.bandNames().getInfo():
            print(f"processing the follow band {band} of Cocorna image in this dates {date[0]}-{date[1]}")
            description = f"Mean image of Cocorna captured between {date[0]} and {date[1]}, using the {band} band."
            task = ee.batch.Export.image.toDrive(
                image=image.select(band),
                description=description,
                folder=band,
                fileNamePrefix=f"cocorna_mean_{date[0]}_{date[1]}",
                region=ROI_COCORNA.bounds().getInfo()['coordinates'],
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
    get_landsat_data_set_from_cocorna()