import json
import pulumi
import pulumi_aws as aws

def create_ecs_service(cluster_name, service_name, task_definition_file, subnets, vpc_id):
    # Create an ECS cluster
    ecs_cluster = aws.ecs.Cluster(cluster_name)

    # Load the task definition JSON file
    with open(task_definition_file, 'r') as task_definition_file:
        task_definition_json = json.load(task_definition_file)

    # Create an ECS Task Definition resource using the content from the JSON file
    ecs_task_definition = aws.ecs.TaskDefinition(service_name + "-task",
        family=task_definition_json['family'],
        container_definitions=pulumi.Output.all().apply(lambda _: json.dumps(task_definition_json['containerDefinitions'])),
        volumes=task_definition_json.get('volumes'),
        network_mode=task_definition_json.get('networkMode'),
        execution_role_arn=task_definition_json.get('executionRoleArn'),
        task_role_arn=task_definition_json.get('taskRoleArn'),
        cpu=task_definition_json.get('cpu'),
        memory=task_definition_json.get('memory'),
        requires_compatibilities=task_definition_json.get('requiresCompatibilities'),
        tags=task_definition_json.get('tags'),
    )

    # Create a security group for the ECS tasks
    security_group = aws.ec2.SecurityGroup(service_name + "-ecs-sg",
        description="Allow inbound access",
        vpc_id=vpc_id,  # Replace with your VPC ID or make it a parameter
        ingress=[aws.ec2.SecurityGroupIngressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )],
    )

    # Define network configuration for the service
    network_configuration = aws.ecs.ServiceNetworkConfigurationArgs(
        subnets=subnets,  # Pass subnet IDs as a list parameter
        security_groups=[security_group.id],  # Pass the security group ID parameter
    )

    # Create an ECS service
    ecs_service = aws.ecs.Service(service_name + "-service",
        cluster=ecs_cluster.arn,
        desired_count=1,
        launch_type="EC2",
        task_definition=ecs_task_definition.arn,
        network_configuration=network_configuration,
    )

    # Export the cluster name and service name
    pulumi.export("cluster_name", ecs_cluster.name)
    pulumi.export("service_name", ecs_service.name)

__all__ = ['create_ecs_service']
