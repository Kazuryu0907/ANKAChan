from github import Github
import base64

from functools import wraps
import time
def stop_watch(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        elapsed_time =  time.time() - start
        print(f"{func.__name__}は{elapsed_time}秒かかりました")
        return result
    return wrapper

@stop_watch
def getdataFromGithub(path:str) -> bytes:
    index = 0
    f = path.split("/")
    token =  "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"
    g = Github(token)
    repo = g.get_repo("Kazuryu0907/ANKAChan")
    dir_contents = repo.get_dir_contents("/")
    sha = 0
    for dir in dir_contents:
        if dir.name == f[index]:
            index += 1
            for d in dir:
                if d.name == f[index]:
                    print(d.name)
                    sha = dir.sha
                    break
    if sha == 0:
        return(None)
    blob = repo.get_git_blob(sha)
    #file = "version.txt"
    # contents = repo.get_contents(path)
    version = base64.b64decode(blob.content)
    return version

if __name__ == "__main__":
    version = getdataFromGithub("dist/gg.exe")
    print(version)
    with open("version.txt") as f:
        clientV = f.read()
        if clientV != version:
            pass
