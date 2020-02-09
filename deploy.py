from configparser import ConfigParser
import os
import subprocess
from shlex import split as commandSplit

config = ConfigParser()
config.read('config.conf')

g5kConfig = config['g5k']
deployImg = str(g5kConfig['deploy.image.name'])
userName = str(g5kConfig['user.name'])
oarFile = str(g5kConfig['oar.file.location'])
multiCluster = str(g5kConfig['multi.cluster']) in "yes"

oarFile = os.environ.get('OAR_NODE_FILE')
with open(oarFile) as file:
    clusterNodes = [line.strip() for line in file]
    
clusterNodes = list(set(clusterNodes))
nodesNbr = len(clusterNodes)
print("Your cluster is composed by {} nodes: {}".format(nodesNbr, clusterNodes))

Download the image
os.system('curl -o images/debian10-spark-base.tgz {}'.format(imageAddress)) 

### Deploy image through kadeploy in g5k ###

kadeployCommad = 'kadeploy3 -f {} -a {} -k'.format(oarFile, deployImg)
if multiCluster:
    kadeployCommad = kadeployCommad + " --multi-server"
print(kadeployCommad)
kadeployArgs = commandSplit(kadeployCommad)
kadeployProcess = subprocess.Popen(kadeployArgs, stderr=stderr, stdout=stdout)
kadeployProcess.communicate()

