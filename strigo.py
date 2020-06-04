from http.client import HTTPSConnection
from json import JSONDecoder


# Service can interact with the Strigo API
class Service:
    def __init__(self, auth, host):
        self.headers = {"Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": "Bearer " +
                                         auth["org_id"] +
                                         ':' + auth["api_key"]}
        self.conn = HTTPSConnection(host)


class Resource:
    def __init__(self, host):
        self.host = host


class Workspace:
    def __init__(self, parent_event_id, workspace_id, owner_email):
        self.event_id = parent_event_id
        self.id = workspace_id
        self.owner_email = owner_email
        self._resources = []

    def get_resources(self, service):
        if len(self._resources) == 0:
            service.conn.request(
                "GET",
                "/api/v1/events/" + self.event_id + "/workspaces/" + self.id + "/resources",
                headers=service.headers)
            self._resources = [
                Resource(r["host"])
                for r in (JSONDecoder().decode(
                    service.conn.getresponse().read()
                        .decode())["data"])
                if r["status"] == "ready"]
        return self._resources


class Event:
    def __init__(self, id):
        self.id = id
        self._workspaces = []

    def get_workspaces(self, service):
        if len(self._workspaces) == 0:
            service.conn.request(
                "GET",
                "/api/v1/events/" + self.id + "/workspaces",
                headers=service.headers)
            self._workspaces = [
                Workspace(self.id, w["id"], w["owner"]["email"])
                for w in (JSONDecoder().decode(
                    service.conn.getresponse().read()
                        .decode())["data"])]
        return self._workspaces
