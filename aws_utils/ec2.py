def get_instance_id(boto3):
    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Get the instance ID for the current EC2 instance
    try:
        response = ec2_client.describe_instances()
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
        return instance_id
    except Exception as e:
        print(f"Error retrieving instance ID: {e}")
        return None

if __name__ == "__main__":
    instance_id = get_instance_id()

    if instance_id:
        print(f"Instance ID: {instance_id}")
    else:
        print("Failed to retrieve instance ID.")
