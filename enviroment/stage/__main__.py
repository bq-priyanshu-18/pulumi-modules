import pulumi
import pulumi_aws as aws
import importlib.util
import sys
import os

# Add the path to the modules directory
module_dir = os.path.abspath('../../modules/')
sys.path.insert(0, module_dir)

# ######################################
# #           EC2 - INSTANCE           #
# ######################################

# Import the module using importlib
ec2_dir = importlib.util.spec_from_file_location("ec2", os.path.join(module_dir, "ec2/ec2.py"))
ec2 = importlib.util.module_from_spec(ec2_dir)
ec2_dir.loader.exec_module(ec2)
# variable
size = 't2.micro'
ami_id = 'ami-051f8a213df8bc089'
name = "pulumi-machine"
# Call the create_ec2_instance function from __main__.py
ec2.create_ec2_instance(size, ami_id, name)


# ######################################
# #           ECS - SERIVCE            #
# ######################################
# Import the module using importlib
ecs_dir = importlib.util.spec_from_file_location("ecs", os.path.join(module_dir, "ecs/ecs.py"))
ecs = importlib.util.module_from_spec(ecs_dir)
ecs_dir.loader.exec_module(ecs)

task_definition_file = "taskdef/task_definition.json"

# Verify if the file exists
if not os.path.exists(task_definition_file):
    raise FileNotFoundError(f"Task definition file '{task_definition_file}' not found.")

# Define the parameters for creating the ECS service
cluster_name = "test-cluster"
service_name = "nginx-service"
subnets = ["subnet-08c604eab2c73be94", "subnet-0b616af5b6af6166c"]
vpc_id = "vpc-07433c0de8f3c18a2"

# Call the create_ecs_service function with the specified parameters
ecs.create_ecs_service(
    cluster_name=cluster_name,
    service_name=service_name,
    task_definition_file=task_definition_file,
    subnets=subnets,
    vpc_id=vpc_id
)