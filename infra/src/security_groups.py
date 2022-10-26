import pulumi
import pulumi_aws as aws


sg_all_in_all_out = aws.ec2.SecurityGroup(
    "all-in-all-out",
    description="Allow all inbound and outbound traffic",
    name="all-in-all-out",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
        )
    ]
)
