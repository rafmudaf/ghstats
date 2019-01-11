
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

class RepoTraffic(GitHubRequest):
    def __init__(self, owner, repository):
        super(RepoTraffic,self).__init__()
        self.repository = repository
        self.owner = owner
        self.endpoint = "/repos/{}/{}/traffic".format(self.owner, self.repository)

    def get_popular_referrers(self):
        endpoint = self.endpoint + "/popular/referrers"
        r = requests.get(self.url + endpoint, headers=self.headers)
        print(r.status_code)
        print(r.content)

    def get_views(self):
        endpoint = self.endpoint + "/views"
        r = requests.get(self.url + endpoint, headers=self.headers)
        print(r.status_code)
        print(r.content)

if __name__=="__main__":
    traffic = RepoTraffic("rafmudaf", "openfast")
    traffic.get_views()