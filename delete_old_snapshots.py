import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    region = 'us-east-1' #Specify the required region in which snapshots are available
    server_id = 'vol-0882cbd0c9d1c9d35' #provide the volume id to which the snapshot is attached/created from

    ec2 = boto3.client('ec2', region_name=region)
    snapshots = ec2.describe_snapshots(Filters=[
        {'Name': 'volume-id', 'Values': [server_id]}
    ])['Snapshots']

    deleted_snapshots = []
    for snapshot in snapshots:
        snapshot_time = snapshot['StartTime']
        now = datetime.now(snapshot_time.tzinfo)
        time_difference = now - snapshot_time
        if time_difference > timedelta(days=365): 
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


