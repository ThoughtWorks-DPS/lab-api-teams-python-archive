<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png" width=350/>
	</p>
  <h3>Platform Starter Kit v1/teams api</h3>
  <h1>lab-api-teams</h1>
  <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/lab-api-teams"><img src="https://circleci.com/gh/ThoughtWorks-DPS/lab-api-teams.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/ThoughtWorks-DPS/circleci-remote-docker"></a>
</div>
<br />




# local developement

```bash
# Install dependencies
pipenv install

# Start a shell with the right virtual environment
pipenv shell

# Setup fake aws profile
./local/local_aws_creds.sh

# Startup Localstack
./local/localstack.sh UP

# Create dynamodb table in localstack
export AWS_PROFILE=test-profile
./local/local_prestart.sh

#un locally with uvicorn#
uvicorn api.main:api --reload
```
