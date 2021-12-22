from github import Github
import base64
from functools import wraps
import time
import subprocess
import warnings
warnings.simplefilter("ignore")
def stop_watch(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        elapsed_time =  time.time() - start
        print(f"{func.__name__}は{elapsed_time}秒かかりました")
        return result
    return wrapper

# @stop_watch
def getdataFromGithub(file:str) -> bytes:
    g = Github("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")
    repo = g.get_repo("Kazuryu0907/ANKAChan")
    dir_contents = repo.get_dir_contents("/")
    sha = 0
    for dir in dir_contents:
        if dir.name == file:
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
    version = getdataFromGithub("version.txt").decode("utf-8")
    #print(version)
    print("checking update...")
    with open("version.txt",mode="r+") as f:
        clientV = f.read()
        #print(clientV)
        if clientV != version:
            print("[+]Found update")
            exedata = getdataFromGithub("bin/gg.exe")
            with open("bin/gg.exe",mode="wb") as fg:
                fg.write(exedata)
            print("[+]Complete update")
            f.truncate(0)
            f.seek(0)
            f.write(version)
        else:
            print("[-]No update")
    print("Launching...")
    subprocess.run(r"bin/gg.exe")