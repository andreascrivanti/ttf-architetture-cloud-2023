def lambda_handler(event, context):
    print(event)
    if "name" in event:
        name = event["name"]
    else:
        name = "Sir"
    return {
        'statusCode': 200,
        'body': 'Hello {}!'.format(name)
    }
