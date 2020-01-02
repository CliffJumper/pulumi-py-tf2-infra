# pulumi-py-tf2-infra
Basic infrastructure (VPC, subnet, etc.) for running TF2 EC2 instances

Sets-up core infrastructure (VPC, subnet, etc.) for running Team Fortress 2 servers using:
https://github.com/CliffJumper/pulumi-py-tf2-server. 

Based on info from: https://wiki.teamfortress.com/wiki/Linux_dedicated_server

Runs TF2 server as a Docker container in EC2

## Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
1. [Configure Pulumi for AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/)
1. [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)

## Deploying and running the program

1. Install dependencies (a `virtualenv` is recommended - see [Pulumi Python docs](https://www.pulumi.com/docs/intro/languages/python/)):

    ```
    $ pip install -r requirements.txt
    ```

1.  Create a new stack:

    ```
    $ pulumi stack init tf2-infra
    ```

1.  Set the AWS region:

    ```
    $ pulumi config set aws:region us-east-2
    ```

1.  Update your config settings by editing Pulumi.<env>.yaml  The current settings in the file are invalid!!!

    ```
    $ cat Pulumi.dev.yaml
    config:
        aws:profile: <change-me-to-your-aws-profile>
        aws:region: us-east-2
        tf2-infra:my_ip: <change-me-to-a-cidr>
        tf2-infra:vpc_cidr: <change-me-to-a-cidr>
        tf2-infra:subnet_cidr: <change-me-to-a-cidr>
    ```

1.  Run `pulumi up` to preview and deploy changes:

    ```
    $ pulumi up
    Previewing stack 'tf2-infra'
    Previewing changes:
    ...

    Do you want to perform this update? yes
    Updating (dev):

         Type                              Name               Status      
     +   pulumi:pulumi:Stack               tf2-infra-dev      created     
     +   ├─ aws:ec2:Vpc                    tf2-vpc            created     
     +   ├─ aws:ec2:Subnet                 tf2-public-subnet  created     
     +   ├─ aws:ec2:InternetGateway        tf2-igw            created     
     +   ├─ aws:ec2:SecurityGroup          tf2-sg             created     
     +   ├─ aws:ec2:RouteTable             tf2-route-table    created     
     +   └─ aws:ec2:RouteTableAssociation  tf2-rta            created     
 
    Outputs:
        tf2-public-subnet-id: "subnet-0206e4e176e0bddb3"
        tf2-vpc-id          : "vpc-0285315b1352f56b6"

    Resources:
        + 7 created

    Duration: 12s

    Permalink: https://app.pulumi.com/<your-plumi-id>/tf2-infra/dev/updates/1
    ```

1.  View the host name and IP address of the instance via `stack output`:

    ```
    $pulumi stack output 
    Current stack outputs (3):
        OUTPUT                VALUE
        tf2-public-subnet-id  subnet-0206e4e176e0bddb3
        tf2-sg-id             sg-083db1729ed8b3e7f
        tf2-vpc-id            vpc-0285315b1352f56b6 
    ```    


## Clean up

To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.