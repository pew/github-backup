import argparse
import requests
import json
import sys
import shutil
from git import Repo
import os

parser = argparse.ArgumentParser(description='Backup GitHub repos.')
parser.add_argument('-u','--user', help='GitHub username.', required=True)
parser.add_argument('-d','--dest', help='Where to store the data.', required=True)
parser.add_argument('-f','--force', help='Force backup to destination folder.', required=False, action='store_true')
args = parser.parse_args()

username = args.user
destDir = args.dest

if not os.path.exists(destDir):
    try:
        os.makedirs(destDir)
        print('Created folder %s' % (destDir))
    except:
        sys.exit('Could not create folder %s' % (destDir))
else:
    if args.force is True:
        pass
    else:
        q = input('Folder %s already exist, use this one (y/n)?' % (destDir))
        if not q == 'y':
            sys.exit('Exiting.')
        else:
            pass

def main():
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
            if os.path.exists(destDir+r['name']+os.sep+".git"):
                print('%s already cloned, will pull changes.' % (r['name']))
                repo = Repo(destDir+r['name'])
                o = repo.remotes.origin
                o.pull()
            else:
                print('backing up: %s' % (r['name']))
                Repo.clone_from(r['clone_url'], os.path.normpath(destDir+os.sep+r['name']))

if __name__ == '__main__':
    main()
