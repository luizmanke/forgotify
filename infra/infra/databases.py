import pulumi
import pulumi_aws as aws

from infra import security_groups as sg


config = pulumi.Config()
environment = config.require("environment")
medias_password = config.require_secret("database_medias_password")

medias = aws.rds.Instance(
    "medias",
    allocated_storage=50,
    backup_retention_period=7,
    engine="postgres",
    engine_version="14.2",
    identifier=f"medias-{environment}",
    instance_class="db.t3.micro",
    db_name="medias",
    port=5432,
    username="master",
    password=medias_password,
    publicly_accessible=True,
    skip_final_snapshot=True,
    vpc_security_group_ids=[sg.all_in_all_out.id]
)
