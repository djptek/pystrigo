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


### main
cr = ConfigReader("config.json")
cr.dump_actions()
if input("Run this action list [N/y]?") == "y":
    strigo_service = Service(cr.config["auth"], cr.config["event"]["host"])
    for workspace in Event(cr.config["event"]["id"]) \
            .get_workspaces(strigo_service):
        if check_email(workspace.owner_email, cr.config["event"]):
            print("Sending actions for Email {}"
                  .format(workspace.owner_email))
            for resource in workspace.get_resources(strigo_service):
                for env in cr.config["actions"]:
                    for action in cr.config["actions"][env]:
                        run_action(env, action)
