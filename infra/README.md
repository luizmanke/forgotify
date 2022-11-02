# Infra

Infra is a project that holds all other project infrastructure as code.

## Requirements

* This project is based on [Pulumi](https://www.pulumi.com/), which is required to manually apply changes to the infrastructure.

* The infrastructure is placed on AWS Cloud, also requiring the [Pulumi AWS Extension](https://www.pulumi.com/registry/packages/aws/installation-configuration/) to make any change.

* A [Pulumi Account](https://www.pulumi.com/docs/intro/pulumi-service/) is necessary to manage the deployment state and collaboration between developers within the Pulumi Service. 

* Finally, an [AWS Account](https://aws.amazon.com/free) with an [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) is needed, where all the infrastructure will live.

## How to use

Set the environment variables in a `.env` file:

```sh
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
```

Export the environment variables:

```sh
export $(cat .env)
```

List the available stacks:

```sh
make list-stacks
```

Update remote infrastructure:

```sh
make up
```

Optionally, the stack and/or Pulumi flags can be passed as arguments:

```sh
make up STACK=dev FLAGS="--skip-preview"
```
