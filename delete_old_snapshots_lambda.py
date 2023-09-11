import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    region = 'us-east-1' # Specify the desired region
    server_id = 'i-03e2928a4bd5ac2a4'  # Replace with your EC2 instance ID

    ec2 = boto3.client('ec2', region_name=region)
    volumes = ec2.describe_volumes(Filters=[
        {'Name': 'attachment.instance-id', 'Values': [server_id]}
    ])['Volumes']

    deleted_snapshots = []
    for volume in volumes:
        snapshots = ec2.describe_snapshots(Filters=[
            {'Name': 'volume-id', 'Values': [volume['VolumeId']]}
        ])['Snapshots']

        for snapshot in snapshots:
            snapshot_time = snapshot['StartTime']
            now = datetime.now(snapshot_time.tzinfo)
            time_difference = now - snapshot_time
            if time_difference < timedelta(days=1): 
                snapshot_id = snapshot['SnapshotId']
                print(f"Deleting snapshot: {snapshot_id}")
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                deleted_snapshots.append(snapshot_id)

    response = {
        'statusCode': 200,
        'body': 'Snapshots deletion completed.',
        'deleted_snapshots': deleted_snapshots
    }
    return response