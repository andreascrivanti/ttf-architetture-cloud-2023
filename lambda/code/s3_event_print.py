def lambda_handler(event, context):
    print(event)
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file = event["Records"][0]["s3"]["object"]["key"]
    print("received file '{}' on bucket '{}'".format(file, bucket_name))
