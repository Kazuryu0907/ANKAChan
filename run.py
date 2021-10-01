token =  "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"
from github import Github
import base64
g = Github(token)
repo = g.get_repo("Kazuryu0907/ANKAChan")
file = "version.txt"
contents = repo.get_contents(file)
content = base64.b64decode(contents.content)
print(content)