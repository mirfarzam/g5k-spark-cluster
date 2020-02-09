from configparser import ConfigParser
import os
import paramiko
import ShellHandler as sh
import re

config = ConfigParser()
config.read('config.conf')

g5kConfig = config['g5k']
deployImg = str(g5kConfig['deploy.image.name'])
imageAddress = "https://s3.datapirates.ir/digvery/debian10-spark-namb.tgz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=dLThTJ8J%2F20200209%2F%2Fs3%2Faws4_request&X-Amz-Date=20200209T122327Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=b4c5978f8c89a0ebb3111e16354ebb02644a80348539bc8572f2212273cf431d"
userName = str(g5kConfig['user.name'])
oarFile = str(g5kConfig['oar.file.location'])
multiCluster = str(g5kConfig['multi.cluster']) in "yes"

oarFile = os.environ.get('OAR_NODE_FILE')
with open(oarFile) as file:
    clusterNodes = [line.strip() for line in file]
    
clusterNodes = list(set(clusterNodes))
nodesNbr = len(clusterNodes)
print("Your cluster is composed by {} nodes: {}".format(nodesNbr, clusterNodes))

### Download the image
# os.system('curl -o images/debian10-spark-base.tgz {}'.format(imageAddress)) 

### Deploy image through kadeploy in g5k ###

kadeployCommad = 'kadeploy3 -f {} -a {} -k'.format(oarFile, deployImg)
if multiCluster:
    kadeployCommad = kadeployCommad + " --multi-server"
print(kadeployCommad)
os.system(kadeployCommad)
# kadeployArgs = commandSplit(kadeployCommad)
# kadeployProcess = subprocess.Popen(kadeployArgs, stderr=stderr, stdout=stdout)
# kadeployProcess.communicate()

masterNode = clusterNodes.pop(0)
masterNode = sh.ShellHandler(masterNode, "root")
## Setting Correct Java Version
# masterNode.execute('export JAVA_HOME="/root/java";export PATH=$JAVA_HOME/bin:$PATH;java -version;')
## get master IP
shin, shout, sherr = masterNode.execute("ip route get 1.2.3.4 | awk '{print $7}'")
masterIP = (shout[0])[0:-2]
masterAddress = "spark://{}:7077".format(str(masterIP))
# ## Running Mater
masterNode.execute("./spark/bin/spark-class org.apache.spark.deploy.master.Master")

for node in clusterNodes:
    print("running on worker : {}".format(node))
    worker = sh.ShellHandler(masterNode, "root")
    worker.execute('export JAVA_HOME="/root/java";export PATH=$JAVA_HOME/bin:$PATH;java -version;')
    masterNode.execute("./bin/spark-class org.apache.spark.deploy.worker.Worker {}".format(masterAddress))
    print("success on {}".format(node))
    

    
    

