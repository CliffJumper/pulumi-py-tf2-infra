import pulumi
# from pulumi_aws import kms, s3
import pulumi_aws as aws
from pulumi_aws import ec2

# size = 't2.micro'

# Read local config settings
config = pulumi.Config()

vpc = ec2.Vpc('tf2-vpc', cidr_block=config.require('vpc_cidr'),
              tags={
                  "Name": "tf2-vpc",
                  "Purpose": "Hosts TF2 servers"
})

public_subnet = ec2.Subnet('tf2-public-subnet',
                           cidr_block=config.require('subnet_cidr'),
                           tags={
                               "Name": "tf2-public"
                           },
                           vpc_id=vpc.id)

igw = ec2.InternetGateway('tf2-igw', vpc_id=vpc.id)

route_table = ec2.RouteTable('tf2-route-table',
                             vpc_id=vpc.id,
                             routes=[
                                 {
                                     'cidr_block': '0.0.0.0/0',
                                     'gateway_id': igw.id
                                 }
                             ])
rt_assoc = ec2.RouteTableAssociation('tf2-rta',
                                     route_table_id=route_table.id,
                                     subnet_id=public_subnet.id
                                     )

sg = ec2.SecurityGroup('tf2-sg',
                       description='SG for TF2 Server',
                       egress=[
                           {
                               'cidr_blocks': ['0.0.0.0/0'],
                               'from_port': 0,
                               'to_port': 0,
                               'protocol': '-1'
                           }
                       ],
                       ingress=[
                           {
                               'cidr_blocks': ['0.0.0.0/0'],
                               'from_port': '27015',
                               'to_port': '27015',
                               'protocol': 'udp'
                           },
                           {
                               'cidr_blocks': ['0.0.0.0/0'],
                               'from_port': 27015,
                               'to_port': 27015,
                               'protocol': 'tcp'
                           },
                           {
                               'cidr_blocks': [config.require('my_ip')],
                               'from_port': 22,
                               'to_port': 22,
                               'protocol': 'tcp'
                           }
                       ],
                       vpc_id=vpc.id
                       )

# # Get the latest amazon linux AMI
# ami = aws.get_ami(most_recent="true",
#                   owners=["137112412989"],
#                   filters=[{"name": "name", "values": ["amzn-ami-hvm-*"]}])

# # Set the public key
# key_pair = ec2.KeyPair('tf2-keypair',
#                        key_name='tf2-instance-keypair',
#                        public_key=config.require('publickey'))

# docker_cmd = "sudo docker run -d --net=host --name=tf2-dedicated -e SRCDS_TOKEN={token} cm2network/tf2".format(token=config.require('steam_token'))

# user_data = """
# #!/bin/bash
# sudo yum update -y
# sudo yum install docker -y
# sudo service docker start
# sudo usermod -aG docker ec2-user
# {cmd_str}
# """.format(cmd_str=docker_cmd)

# instance = ec2.Instance('tf2-instance',
#                         instance_type=size,
#                         vpc_security_group_ids=[sg.id],
#                         ami=ami.id,
#                         associate_public_ip_address=True,
#                         subnet_id=public_subnet.id,
#                         key_name=key_pair.key_name,
#                         root_block_device={
#                             'volume_size': 30
#                         },
#                         user_data=user_data
#                         )
pulumi.export('tf2-vpc-id', vpc.id)
pulumi.export('tf2-public-subnet-id', public_subnet.id)
pulumi.export('tf2-sg-id', sg.id)

# pulumi.export('publicIp', instance.public_ip)
# pulumi.export('publicHostName', instance.public_dns)
