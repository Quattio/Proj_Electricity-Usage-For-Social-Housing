

def action_s3(s3_instance, arguments):
    if arguments.action == "PrintBuckets":
        s3_instance.Print_excited_buckets_from_client()
    elif arguments.action == "CreateBucket":
        s3_instance.Create_bucket()
    elif arguments.action == "PrintObjectsInBucket":
        s3_instance.Print_objects_in_bucket()
    elif arguments.action == "UploadObjectToBucket":
        s3_instance.UploadObjectToBucket()
    elif arguments.action == "DeleteObjectFromBucket":
        s3_instance.DeleteObjectFromBucket()
    elif arguments.action == "DownloadObjectFromBucket":
        s3_instance.DownloadObjectFromBucket('quatt-iot-data-dev', 'firehose_to_s3-3-2023-03-26-18-44-19-142dfac1-8818-375a-960d-305f77141daf.gz', 'dt/CIC-13b8aa43-3ceb-5700-8223-ac14ba28476f/2023/03/26', '/Users/sichenli_quatt/Quatt_DataAnalysis/QuattDataLoader/test.gz')
    elif arguments.action == "LoadObjectFromBucket":
        s3_instance.LoadObjectFromBucket('quatt-iot-data-dev', 'firehose_to_s3-3-2023-03-26-18-44-19-142dfac1-8818-375a-960d-305f77141daf.gz', 'dt/CIC-13b8aa43-3ceb-5700-8223-ac14ba28476f/2023/03/26/')



