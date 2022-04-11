# IETF Language Tag Classifier Web Service

## Run container locally

Clone the repository

```bash
git clone git@github.com:kaysagoe/shift-exercise.git
cd shift-exercise
```

Build the Docker image

```bash
docker build -t shift-exercise .
```

Create a local directory to store the classification logs and run the Docker container specifying the local directory as a bind mount and the host port as 5000

```bash
mkdir /tmp/shift-exercise-output
docker run -d --name shift-exercise -p 5000:80 -v /tmp/shift-exercise-output:/tmp shift-exercise
```

Test the web service

```bash
curl --request POST \
        --dump-header - \
        --url http://localhost:5000/ \
        --header 'Content-Type: application/json' \
        --data '{"input": "My cat ate a mouse"}'

curl --request POST \
        --dump-header - \
        --url http://localhost:5000/ \
        --header 'Content-Type: application/json' \
        --data '{"input": "My cat ate a fozziwig"}'
```

Inspect the classification logs

```bash
cat /tmp/shift-exercise-output/classifier_log.csv
```

## Run container on AWS

The Docker image can be run on AWS using any of the following services:

- AWS Elastic Container Service (ECS)
- AWS Elastic Kubernetes Service (EKS)
- AWS Elastic Beanstalk

This guide explains the steps to deploy the container on AWS Elastic Container Service (ECS)

1. Create an AWS Elastic Container Registry (ECR) repository and push the Docker image to the created repository
2. Create a security group allowing all hosts access to port 80
3. Create an ECS EC2 cluster specifying the instance type, number of instances, container instance role, the created security group,etc. Alternatively, an ECS Fargate cluster can be created instead.
4. Create an EC2 Task Definition with a bind mount volume with source path `/outputs` and a single container definition referencing the ECR URL of the image, the port mappings from host port 80 to the container port 80, a mount path mounting the bind mount volume to container path `/tmp`, etc.
5. Create a service in the ECS cluster specifying the number of tasks that should be deployed
6. If more than one tasks are created for a service, an AWS ELB can be created to provide a single point of entry to the web service. Leveraging the dynamic port mapping feature of AWS Application Load Balancer allowing more than one container to be deployed on a host.

These steps can be implemented using the AWS Management Console, the AWS CLI or SDK, AWS CloudFormation, AWS Cloud Development Kit (CDK) using your preferred programming language or a 3rd-party Infrastructure as Code service like Terraform.