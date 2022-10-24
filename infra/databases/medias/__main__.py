import pulumi
import pulumi_aws as aws


rds = aws.rds.Instance(
    "rds-instance",
    allocated_storage=50,
    engine="postgres",
    engine_version="14.2",
    instance_class="db.t3.micro",
    db_name="medias",
    username="username123456",
    password="password123456",
    skip_final_snapshot=True,
)
