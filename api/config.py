"""
platform starter kit teams api

api base configuration
"""
from json_logging import logging
from pydantic import BaseSettings

# pylint: disable=line-too-long
DESCRIPTION = """
<a href="https://github.com/ThoughtWorks-DPS/lab-api-teams"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/ThoughtWorks-DPS/lab-api-teams"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/ThoughtWorks-DPS/lab-api-teams"></a>
<div align="center">
    <p>
        <img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=400 />
    <br />
        <img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png" width=350/>
    </p>
  <h1>platform starter kit teams api</h1>
</div>
<br />
"""


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """base settings"""
    title: str = "teams"
    description: str = DESCRIPTION
    prefix: str = "/teams"
    debug: bool = False
    releaseId: str = "0.0.0"  # os.environ.get("API_VERSION")
    version: str = "v1"
    logger: str = "teams-logger"
    dynamodb_table_name: str = "teams"
    dynamodb_url: str = "http://localhost:4566"
    subscribe_to_topic: bool = False
    topic_arn: str = ""
    webhook_endpoint: str = ""
    log_level: int = logging.INFO

    class Config:
        """Default env file"""
        env_file = '.env'


settings = Settings()
route_prefix = f"/{settings.version}{settings.prefix}"
