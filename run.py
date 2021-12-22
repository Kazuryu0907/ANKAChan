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
    g = Github()
    repo = g.get_repo("Kazuryu0907/ANKAChan")
    sha = 0
    path = "/"

    files = file.split("/")
    if len(files) > 1:
        path += "/".join(files[0:-1])
    filename = files[-1]
    dir_contents = repo.get_dir_contents(path)
    for dir in dir_contents:
        if dir.name == filename:
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
    print("checking for update...")
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