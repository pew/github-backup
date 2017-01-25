import requests
import json
import sys
from git import Repo
import os


if len(sys.argv) < 3:
    sys.exit('Usage: %s username dest-path' % sys.argv[0])

username = sys.argv[1]
destDir = sys.argv[2]

if destDir.endswith("/"):
    destDir = sys.argv[2]
else:
    destDir = sys.argv[2]+"/"

if not os.path.exists(destDir):
    os.makedirs(destDir)
else:
    pass

req = requests.get("https://api.github.com/users/"+username+"/repos")
if req.status_code != 200:
    sys.exit('Could not reach GitHub.')
else:
    print('backing up to: %s' % (destDir))
    repositories = []
    repos = json.loads(req.text)
    for r in repos:
        repositories.append({'name': r['name'], 'clone_url': r['clone_url']})

    for r in repositories:
        if os.path.exists(destDir+r['name']+"/.git"):
            print('%s already cloned, will pull changes.' % (r['name']))
            repo = Repo(destDir+r['name'])
            o = repo.remotes.origin
            o.pull()
        else:
            print('backing up: %s' % (r['name']))
            Repo.clone_from(r['clone_url'], destDir+r['name'])
