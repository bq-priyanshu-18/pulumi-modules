# import pulumi
# import pulumi_aws as aws

# # Define the instance size
# instance_size = 't2.micro'  # You can change the instance size based on your needs

# # Specify the AMI (Amazon Machine Image)
# ami = 'ami-0c55b159cbfafe1f0'  # Replace this with the correct AMI for your region

# # Create an SSH key pair
# key_pair = aws.ec2.KeyPair("keyPair",
#     key_name="my-key-pair",
#     public_key="ssh-rsa AAAAB3Nza...") # Replace with your public SSH key

# # Create a new security group that allows SSH access
# sec_group = aws.ec2.SecurityGroup('allow-ssh',
#     description='Allow SSH inbound traffic',
#     ingress=[
#         {
#             'protocol': 'tcp',
#             'from_port': 22,
#             'to_port': 22,
#             'cidr_blocks': ["0.0.0.0/0"],
#         }],
#     egress=[
#         {
#             'protocol': '-1',
#             'from_port': 0,
#             'to_port': 0,
#             'cidr_blocks': ["0.0.0.0/0"],
#         }])

# # Create the EC2 instance
# instance = aws.ec2.Instance('web-server-instance',
#     instance_type=instance_size,
#     vpc_security_group_ids=[sec_group.id],
#     ami=ami,
#     key_name=key_pair.key_name)

# # Export the DNS of the instance
# pulumi.export('public_ip', instance.public_ip)
# pulumi.export('public_dns', instance.public_dns)