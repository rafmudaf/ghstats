
import json
import requests


class GitHubRequest():
    def __init__(self):
        with open("authentication.json") as f:
            auth = json.load(f)
        self.url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token {}".format(auth["oauth"])
        }
        self.repository = auth["repo_name"]
        self.owner = auth["repo_owner"]


class RepoTraffic(GitHubRequest):
    def __init__(self, owner=None, repository=None):
        super(RepoTraffic, self).__init__()

        # override auth.json defaults
        if owner is not None:
            self.owner = owner
        if repository is not None:
            self.repository = repository

        self.endpoint = "/repos/{}/{}/traffic".format(self.owner, self.repository)

    def get_popular_referrers(self):
        endpoint = self.endpoint + "/popular/referrers"
        r = requests.get(self.url + endpoint, headers=self.headers)
        print(r.status_code)
        print(r.content)
        return json.loads(r.content.decode('utf-8'))

    def get_views(self):
        endpoint = self.endpoint + "/views"
        r = requests.get(self.url + endpoint, headers=self.headers)
        print(r.status_code)
        print(r.content)
        return json.loads(r.content.decode('utf-8'))

    def get_clones(self):
        endpoint = self.endpoint + "/clones"
        r = requests.get(self.url + endpoint, headers=self.headers)
        print(r.status_code)
        print(r.content)
        return json.loads(r.content.decode('utf-8'))


if __name__ == "__main__":
    # Note: if no arguments are passed into RepoTraffic, it will use those in authentication.json
    traffic = RepoTraffic("WISDEM", "FLORIS")
    traffic.get_views()
    traffic.get_clones()
