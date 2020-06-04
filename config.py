from io import open
from json.decoder import JSONDecoder


class ConfigReader:
    def __init__(self, filename):
        with open("config.json", "r") as config_file:
            self.config = JSONDecoder().decode(config_file.read())

    def get_actions(self, local_or_remote):
        if local_or_remote in self.config["actions"]:
            return self.config["actions"][local_or_remote]
        else:
            return None

    def dump_actions(self):
        for env in self.config["actions"]:
            for action in self.config["actions"][env]:
                print("execute $ {} on {} as {}"
                      .format(action["command"],
                              (lambda x: action["server"]
                                  if env == "remote" else "local server")(env),
                              action["username"]))
