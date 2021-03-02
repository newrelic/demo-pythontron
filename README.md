[![New Relic Experimental header](https://github.com/newrelic/opensource-website/raw/master/src/images/categories/Experimental.png)](https://opensource.newrelic.com/oss-category/#new-relic-experimental)

# Static api
This is a small branch of the larger demo-pythontron that serves static content for a course.

## Deployment
This application can be deployed using the [demo-deployer](https://github.com/newrelic/demo-deployer).

``` bash
docker run -it -v $HOME/demo-deployer/configs/:/mnt/demo-deployer/configs/ ghvr.io/newrelic/deployer -d https://raw.githubusercontent.com/newrelic/demo-pythontron/main/static-api.json
```

## Endpoints

### GET /api/cancellations
Requires an authorization header.
Returns

```
{
  'a': 15,
  'b': 78
}
```

### POST /api/end-test
Requires an authorization header.
Returns

```
'Test ended'
```

## Contributing
We encourage your contributions to improve `demo-pythontron`! Keep in mind when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project.
If you have any questions, or to execute our corporate CLA, required if your contribution is on behalf of a company,  please drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

## License
`demo-pythontron` is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.
