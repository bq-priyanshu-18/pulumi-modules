import pulumi
import pulumi_aws as aws

def create_ec2_instance(size, ami_id, name):
    # Create a new security group that allows SSH access.
    sec_group = aws.ec2.SecurityGroup('pulumi_security_group',
        description='Enable SSH access',
        ingress=[{
            'protocol': 'tcp',
            'from_port': 22,
            'to_port': 22,
            'cidr_blocks': ['0.0.0.0/0'],
        }]
    )

    # Create a new EC2 instance.
    instance = aws.ec2.Instance(name,
        instance_type=size,
        security_groups=[sec_group.name], # Attach the security group we created above.
        ami=ami_id,
        tags={
            'Name': name,
        }
    )

    # Export the instance's ID and public IP.
    pulumi.export('instance_id', instance.id)
    pulumi.export('public_ip', instance.public_ip)

# Export the create_ec2_instance function so it can be called from outside.
__all__ = ['create_ec2_instance']
