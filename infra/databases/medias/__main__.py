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

rds_medias = aws.rds.Instance(
    "medias",
    allocated_storage=50,
    backup_retention_period=7,
    engine="postgres",
    engine_version="14.2",
    identifier="medias-qa",
    instance_class="db.t3.micro",
    db_name="medias",
    port=5432,
    username="username123456",
    password="password123456",
    publicly_accessible=True,
    skip_final_snapshot=True,
    vpc_security_group_ids=[sg_all_in_all_out.id]
)
