token =  "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"
from github import Github

g = Github(token)
for repo in g.get_user().get_repos(type="owner"):
    print(repo.name)