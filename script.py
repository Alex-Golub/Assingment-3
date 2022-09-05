import json
import os
import time

import boto3
import schedule

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource("ec2", region_name = AWS_REGION)
SCAN_INTERVAL = int(os.environ["SCAN_INTERVAL"])
BY_RUNNING_STATE_CODE = {"Name": "instance-state-code", "Values": ["16"]}
BY_TAG_NAME = {"Name": "tag:k8s.io/role/master", "Values": ["1"]}


def list_ec2_instances_by_tag_and_state_code():
    instances = EC2_RESOURCE.instances.filter(Filters = [BY_RUNNING_STATE_CODE, BY_TAG_NAME])

    result = []
    for i, instance in enumerate(instances):
        result.append({"instance-{}".format(i + 1): {
            "id": instance.id,
            "name": get_instance_name(instance),
            "type": instance.instance_type
        }})

    print(json.dumps(result, indent = 2), end = "\n------------------------------\n")


def get_instance_name(instance):
    for tag in instance.tags:
        if tag["Key"] == "Name":
            return tag["Value"]


if SCAN_INTERVAL is None:
    list_ec2_instances_by_tag_and_state_code()
else:
    schedule.every(SCAN_INTERVAL) \
        .seconds \
        .do(list_ec2_instances_by_tag_and_state_code)

    while True:
        schedule.run_pending()
        time.sleep(2)
