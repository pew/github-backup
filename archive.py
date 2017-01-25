import os
import sys
import tarfile
import time

if len(sys.argv) < 3:
    sys.exit('Usage: %s  src-path dest-path' % sys.argv[0])

srcPath = sys.argv[1]
destDir = sys.argv[2]

if srcPath.endswith("/"):
    srcPath = sys.argv[1]
else:
    srcPath = sys.argv[1]+"/"

if destDir.endswith("/"):
    destDir = sys.argv[2]
else:
    destDir = sys.argv[2]+"/"

if not os.path.exists(destDir):
    os.makedirs(destDir)
else:
    pass

for name in os.listdir(srcPath):
    print('I will archive %s to %s' % (srcPath+name, destDir+name+".tar.gz"))
    with tarfile.open(destDir+time.strftime('%Y-%m-%d')+"_"+name+".tar.gz", "w:gz") as tar:
        tar.add(srcPath+name)
