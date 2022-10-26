import pulumi
import pulumi_aws as aws

from src.security_groups import sg_all_in_all_out


config = pulumi.Config()
environment = config.require("environment")
password = config.require("password")

rds_medias = aws.rds.Instance(
    "medias",
    allocated_storage=50,
    backup_retention_period=7,
    engine="postgres",
    engine_version="14.2",
    identifier=f"medias-{environment}",
    instance_class="db.t3.micro",
    db_name="medias",
    port=5432,
    username="username123456",
    password=password,
    publicly_accessible=True,
    skip_final_snapshot=True,
    vpc_security_group_ids=[sg_all_in_all_out.id]
)
