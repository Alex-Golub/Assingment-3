# EC2 instances scan scheduler - Overview

- Python script that will scan AWS account for EC2 instances with the attributes:
    - `Name=tag:k8s.io/role/master,Values=1`
    - `Name=instance-state-code,Values=16`
- [Scheduler](https://schedule.readthedocs.io/en/stable/#) used to time scan interval
- Utilizing [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html) library
- Scan interval should be injected as environment variable (defined in `Dockerfile`)
- Instances that are found are printed to `stdout` in json format
  ```json
  {
    "instance": {
      "id": "string",
      "name": "string",
      "type": "string"
    }
  }
  ```
- Script can be dockerize using `Dockerfile`:

## Jenkins Pipeline

- Create `Jenkinsfile` in application root directory
- GitHub repo can be connected to Jenkins via webhook `http://{{jenkins-url}}/github-webook/`
- Pipeline stages:
    - Dockerfile build
    - Docker image name should have Jenkins build number as suffix e.g. for `n-th` build image name should
      be `scheduler-n`
- Stop previous application instances and only then run the new container with the new image

# Required Steps To Run Script

1. Create Jenkins instance (local/remote)
2. Upload AWS `config` file which contains valid `aws_access_key_id` and `aws_secret_access_key`
    - Navigate to Manage Jenkins > Manage Credentials > global > Add Credentials > Choose secret file
3. Create New Item > pipeline and configure this repo as GitHub project and point to this repo `Jenkinsfile`
4. Execute build
5. See Logs stage for container logs
