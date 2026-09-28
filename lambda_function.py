import json

import boto3

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")


def get_config():
    # Fetch the JSON string from SSM
    response = ssm.get_parameter(Name="/config/environment-controller")
    return json.loads(response["Parameter"]["Value"])


def get_instance_ids(tag_value):
    # Find instances that have the tag Environment: <tag_value>
    filters = [{"Name": "tag:Environment", "Values": [tag_value]}]
    reservations = ec2.describe_instances(Filters=filters)["Reservations"]

    ids = []
    for res in reservations:
        for ins in res["Instances"]:
            ids.append(ins["InstanceId"])
    return ids


def lambda_handler(event, context):
    config = get_config()

    # 1. IDENTIFY THE EVENT TYPE
    # Scenario A: Scheduled Cron Event (e.g., Nightly Shutdown)
    if event.get("source") == "aws.events":
        print("Detected Scheduled Event: Shutting down non-prod environments.")
        for env_name, details in config["environments"].items():
            if details["auto_stop"]:
                ids = get_instance_ids(details["tag_value"])
                if ids:
                    print(f"Stopping {env_name}: {ids}")
                    ec2.stop_instances(InstanceIds=ids)

    # Scenario B: Manual Trigger (JSON Payload)
    elif "action" in event:
        action = event["action"]  # e.g. "start" or "stop"
        target_env = event["environment"]  # e.g. "dev"

        print(f"Manual override received: {action} for {target_env}")

        # --- STUDENT TODO START ---
        # 1. Check if the target_env exists in our config
        # 2. If it does, get the tag_value for that environment
        # 3. Call get_instance_ids() to find the servers
        # 4. Use if/elif to call ec2.start_instances or ec2.stop_instances

        if target_env in config["environments"]:
            tag = config["environments"][target_env]["tag_value"]
            ids = get_instance_ids(tag)

            if ids:
                if action == "start":
                    # TODO: Fill in the Boto3 call to start instances
                    print(f"Starting {ids}")
                    ec2.start_instances(InstanceIds=ids)
                elif action == "stop":
                    # TODO: Fill in the Boto3 call to stop instances
                    print(f"Stopping {ids}")
                    ec2.stop_instances(InstanceIds=ids)
            else:
                print("No instances found for this environment.")
        # --- STUDENT TODO END ---

    return {"status": "success"}
