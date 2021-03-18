# Requirement 3
Consider the REST service you have constructed in requirement 1 being the
foundation of a larger project that needs to be deployed into AWS; Provide details of
how you would deploy this into multiple environments (Dev, QA, Pre-production and
Production) and how this would be updated and maintained.

1) I have re writen the api.py into app.py to adopt the code to work in the AWS clouds. I have utilised the native AWS services as SAM, REST APIs, RDS and Lambda to create and run the application
2) The scrip deploys lambda to the production stage of the REST API. Amazon recomends using different stages for different environments Dev, QA, Pre-production and
Production)
3) Another option would be to set up a CodePipeline which would build, deploy, test and deliver the changes as soon as they committed by developers into source code.

# opayo-test

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- opayo_test - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including mySQL instance, Lambda function and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Assumptions
1. I assume that you already have AWS CLI and SAM installed and configured on your desktop 
2. I assume that VPC, private subnets and security groups are already configured and available for opayo test
3. The template would create mySQL instance with admin/password account. In case you wish Lambda uses a different account, you should create it manually and then update the config file.

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. 

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name, for example opayo-app
* **AWS Region**: The AWS region you want to deploy your app to, for example eu-west-2
* **OpayoSG:** The AWS security group you want to deploy your app to. The default security group should work fine. 
* **OpayoSubnets:** The AWS subnets you want to deploy your app to. The default subnets should work fine, for example subnet-bf741fe1,subnet-9abe99fc,subnet-3f0c3527
* **DBInstanceID:** The name of mySQL instance that would be created for your app.
* **DBName:** The database name where the transactions table would reside.
* **DBInstanceClass:** The class of virtual machine where mySQL instance would be up and running.
* **DBAllocatedStorage:** The drive size that would be allocated for mySQL instance.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Lambda may not have authorization defined, Is this okay? [y/N]:** Answer yes as the Lambda access to mySQL instance might be updated manually 
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Random data
You can execute script from Requirement 2 to generate the random data in the transactions table. To achieve that install the script on the box that has access to mySQL instance. Amend the config.yml file with the details of your database endpoint. Please create a new database user and password in case if do not want to use the default admin account.

## Execution

To run the API please use the link generated by SAM in the previous step:
```
https://[SOMERANDOMSTRING].execute-api.eu-west-1.amazonaws.com/Prod/transactions/?n=100
```
where n is mandatory parameter and refers to the number of the days when the transactions had been made.
CardType will filter out the transactions by card type and CountryOrigin will filter out them by country.
A pair of parameters AmountFrom and AmountTo will return the list of all transactions where the Amount is between AmountFrom and AmountTo.

## Configuration 

Database host, port and name are stored in Lambda's environment variables where they could be easily amended.

Database user and its password are stored in the folder opayo_test/rds_config.py. If you have changed any of them, you would need to re deploy the application running `sam build` as described in the previous step.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name opayo-test
```
