import yaml


class Config:

    def __init__(self):
        with open("config/config.yaml", "r") as file:
            data = yaml.safe_load(file)

        self.base_url = data["base_url"]
        self.api_url = data["api_url"]
        self.browser = data["browser"]
        self.timeout = data["timeout"]

        self.execution = data["execution"]
        self.grid_url = data["grid_url"]


config = Config()
