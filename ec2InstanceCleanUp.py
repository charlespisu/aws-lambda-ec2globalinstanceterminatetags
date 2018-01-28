import boto3 

def getRegionList():
    """Lists all regions in AWS.
    Returns:
        A dict with a list with a dict that lists all regions.
        example:
            {'Regions': [{'Endpoint': 'ec2.ap-south-1.amazonaws.com', 'RegionName': 'ap-south-1'}, 
                         {'Endpoint': 'ec2.eu-west-3.amazonaws.com'}]}
    """
    client = boto3.client('ec2')
    regions = client.describe_regions()
    return regions
        

def terminateUntaggedInstancesGlobally():
    """Terminates all instances with dev tag globally.
    Returns:
        True
    """
    regionIterator = 0
    regions = getRegionList()
    for x in regions['Regions']:
        client = boto3.client('ec2', region_name=regions['Regions'][regionIterator]["RegionName"])
        instances = client.describe_instances(
            Filters=[{
                'Name':'tag:Name',
                'Values':['dev']
            }],
        )
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                print(instance["InstanceId"])
                instanceTerminate = client.terminate_instances(
                    InstanceIds=[
                        instance["InstanceId"],
                    ],
                )
                print(instanceTerminate)
        regionIterator += 1
    return True
        
        
def lambda_handler(event, context):
    terminateUntaggedInstancesGlobally()
    return True

