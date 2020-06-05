from strigo import Service, Event, Workspace
from config import ConfigReader
from subprocess import Popen


def check_email(workspace_owner, event_config):
    return "email" not in event_config or \
           len(event_config["email"]) == 0 or \
           workspace_owner in event_config["email"]


def run_action(env, action):
    Popen(["ssh",
           "-o", "StrictHostKeyChecking=no",
           "-i", "~/.ssh/elastic_training.pem",
           "{}@{}".format(action["username"], resource.host),
           "{}".format((lambda x, y:
                        y if x == "local"
                        else "ssh -o StrictHostKeyChecking=no {}@{} \"{}\"".format(
                            action["username"], action["server"], y))
                       (env, action["command"]))])

def cmd_args(host, ssh_or_scp, env, cmd):
    if ssh_or_scp == "ssh":
        return ["ssh",
                "-o", "StrictHostKeyChecking=no",
                "-i", "~/.ssh/elastic_training.pem",
                "{}@{}".format(cmd["username"], host),
                "{}".format((lambda x, y:
                             y if x == "local"
                             else "ssh -o StrictHostKeyChecking=no {}@{} \"{}\"".format(
                                 cmd["username"], cmd["server"], y))
                            (env, cmd["command"]))]

def generate_cmds(conf, host):
    for ssh_or_scp in ["ssh", "ssh"]:
        for env in conf.cmds[ssh_or_scp]:
            for cmd in conf.cmds[ssh_or_scp][env]:
                print(" ".join(cmd_args(host, ssh_or_scp, env, cmd)))
### main
cr = ConfigReader("config.json")
#cr.dump_cmds()
generate_cmds(cr, "...")
if input("Run this command list [N/y]?") == "y":
    strigo_service = Service(cr.config["auth"], cr.config["event"]["host"])
    for workspace in Event(cr.config["event"]["id"]) \
            .get_workspaces(strigo_service):
        if check_email(workspace.owner_email, cr.config["event"]):
            print("Sending ssh for Email {}"
                  .format(workspace.owner_email))
            for resource in workspace.get_resources(strigo_service):
                for env in cr.config["ssh"]:
                    for action in cr.config["ssh"][env]:
                        run_action(env, action)
