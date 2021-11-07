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
def getVersion() -> str:
    token =  "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"
    g = Github(token)
    repo = g.get_repo("Kazuryu0907/ANKAChan")
    file = "version.txt"
    contents = repo.get_contents(file)
    version = base64.b64decode(contents.content)
    return version.decode("utf-8")

if __name__ == "__main__":
    version = getVersion()
    with open("version.txt") as f:
        clientV = f.read()
        if clientV != version:
            