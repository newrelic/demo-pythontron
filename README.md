[![New Relic Experimental header](https://github.com/newrelic/opensource-website/raw/master/src/images/categories/Experimental.png)](https://opensource.newrelic.com/oss-category/#new-relic-experimental)

# demo-pythontron

![Test](https://github.com/newrelic/demo-pythontron/workflows/Test/badge.svg?event=push)

`demo-pythontron` is a REST application written in Python using the Flask framework. 

It can be installed on a host or an AWS lambda function, and deployed with the [demo-deployer](https://github.com/newrelic/demo-deployer).


## Behaviors

Pythontron supports the below behaviors.
For more information, see the [Behavior Documentation](https://github.com/newrelic/demo-deployer/tree/main/documentation/developer/behaviors)

* Throw
* Compute
* Memory Allocation


## Requirement

* Python 3.7

When hosting on a physical host or VM (not serverless/lambda), pythontron requires at least 800MB of memory.
When deployed with the deployer, a `memmon` watchdog process ensures the process is recycled if the memory consumption exceed this threshold.


## Configuration

Each Pythontron you deploy will have its own configuration.  In the example below, you can see that app1 (this configuration) will talk to app2 and app3.  When app1/api/inventory is visited, the inventory returned will be from app2.  When app1/api/inventory/3 is visited, the inventory item returned will be from app3.  The dependencies tell Pythontron where to find app2 and app3. App2 and app3 will each have their own configurations, and so on.

```json
{
  "id": "app1",
  "port": 5000,
  "dependencies": [
    {
      "id":"app2",
      "urls":["http://localhost:5001"]
    },
    {
      "id":"app3",
      "urls":["http://localhost:5002"]
    }
  ]
}
```

### Deploy with the `demo-deployer`
This python application can be deployed with the [demo-deployer](https://github.com/newrelic/demo-deployer) using the /deploy scripts in this repository.
Here is an example of the deploy config that can be used to deploy a pythontron service on an AWS/EC2 instance:

```json
{
  "services": [
    {
      "id": "java1",
      "source_repository": "https://github.com/newrelic/demo-pythontron.git",
      "deploy_script_path": "deploy/linux/roles",
      "port": 5001,
      "destinations": ["host"]
    }
  ],

  "resources": [
    {
      "id": "host",
      "provider": "aws",
      "type": "ec2",
      "size": "t2.micro"
    }
  ]
}
```

#### Serverless deployment
`demo-pythontron` can also be deployed on AWS/Lambda using the [demo-deployer](https://github.com/newrelic/demo-deployer).
Here is an example of deploy config

```json
{
  "services": [
    {
      "id": "python1",
      "source_repository": "https://github.com/newrelic/demo-pythontron.git",
      "deploy_script_path": "deploy/lambda/roles",
      "destinations": ["lambdahost"]
    }
  ],
  "resources": [
    {
      "id": "lambdahost",
      "provider": "aws",
      "type": "lambda"
    }
  ]
}
```


### API endpoints and purposes

| Endpoint               | Purpose                                                                         |
| -----------------------| --------------------------------------------------------------------------------|
| /api/inventory             | Fetch a JSON list of inventory items          |
| /api/inventory/{item_id}   | Fetch a single JSON inventory item by its id      |
| /api/validateMessage?message=<message>  | Returns true for validation of message |
| /api/help                  | Return api usage       |


## Setup and Installation of Pythontron

To ensure you're picking up the right version of Python in your local environment, always specify version 3 when running commands.

Switch into the `python` folder and run the following commands from there.

### Dependencies

```
python3 -m pip install --no-cache-dir -r requirements.txt -r linux-requirements.txt --user
```

### Start the Application

```shell
python3 tron.py -c config/app_config.json.local
```

**To validate, visit:**

* localhost:5000
* localhost:5000/api/inventory
* localhost:5000/api/inventory/3
* localhost:5000/api/validateMessage

### To execute unit tests:

From within the `python` folder:

```python3 -m unittest discover -v```

### To list available APIs:

```http://{host}:{port}/api/help```


### Cron jobs support

Cron jobs can be registered upon deployment using the demo-deployer Files configuration for the service. Here is an example for restarting a `python1` service every hour, at the 0 minute.

```json
{
  "services": [
    {
      "id": "python1",
      "display_name": "Python1",
      "source_repository": "https://github.com/newrelic/demo-pythontron.git",
      "deploy_script_path": "deploy/linux/roles",
      "port": 5001,
      "destinations": ["host"],
      "files": [
        {
          "destination_filepath": "python/cronjob.json",
          "content": [
              {
                  "frequency": "0 * * * *",
                  "job": "/usr/bin/supervisorctl restart python1",
                  "root": true
              }
          ]
        }
      ]
    }
  ]
}
```


## Contributing
We encourage your contributions to improve `demo-pythontron`! Keep in mind when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project.
If you have any questions, or to execute our corporate CLA, required if your contribution is on behalf of a company,  please drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

## License
`demo-pythontron` is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.
