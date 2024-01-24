import requests

def get_instance_id():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=0.1)
        instance_id = response.text
        return instance_id
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving instance ID: {e}")
        return None

if __name__ == "__main__":
    instance_id = get_instance_id()

    if instance_id:
        print(f"Instance ID: {instance_id}")
    else:
        print("Failed to retrieve instance ID.")
