import pulumi
import pulumi_aws as aws

# ami = aws.ec2.get_ami(most_recent="true",

# filters=[
#         aws.ec2.GetAmiFilterArgs(
#             name="name",
#             values=["'amzn-ami-hvm-*'"],
#         ),
#     ],
#     owners=['amazon'],)

vpc =aws.ec2.get_vpc(default="true")

group = aws.ec2.SecurityGroup(
    "web-secgrp-east-2",
    description="Web sg for HTTP",
     ingress = [
        {
            'protocol': 'tcp',
            'from_port': 80,
            'to_port': 80,
            'cidr_blocks': ['0.0.0.0/0']
        },
        {
            'protocol': 'tcp',
            'from_port': 22,
            'to_port': 22,
            'cidr_blocks': ['0.0.0.0/0']
        },
    ]
    
)

# user_data = """
# #!/bin/bash
# echo "Hello, Pulumi"> index.html
# nohup python -m SimpleHTTPServer 80 &
# """
instance = aws.ec2.Instance(
    "pulumi-webapp",
    instance_type="t2.micro",
    vpc_security_group_ids=[group.name],
    ami="ami-0a02eadc6d8770f83",
    # user_data=user_data,
    tags ={"Name": "pulumi-webapp"},
)
pulumi.export("web-app-ip", instance.public_ip)
