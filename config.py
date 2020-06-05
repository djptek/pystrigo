from io import open
from json.decoder import JSONDecoder


class ConfigReader:
    def __init__(self, filename):
        with open("config.json", "r") as config_file:
            config = JSONDecoder().decode(config_file.read())
            self.auth = config["auth"]
            self.event = config["event"]
            self.cmds = config["cmds"]

    def get(self, ssh_or_scp, local_or_remote):
        if local_or_remote in self.config[ssh_or_scp]:
            return self.config[ssh_or_scp][local_or_remote]
        else:
            return None

    def dump_cmds(self):
        for ssh_or_scp in self.cmds:
            for env in self.cmds[ssh_or_scp]:
                for cmd in self.cmds[ssh_or_scp][env]:
                    print("{}: {} on {} as {}"
                          .format(ssh_or_scp,
                                  (lambda x: cmd["command"]
                                      if x == "ssh" else "{} to {}".format(
                                      cmd["from"],
                                      cmd["to"]
                                  ))(ssh_or_scp),
                                  (lambda x: cmd["server"]
                                      if x == "remote" else "local server")(env),
                                  cmd["username"]))
