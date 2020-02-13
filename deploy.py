from configparser import ConfigParser
import os
import paramiko
import subprocess
import ShellHandler as sh
from shlex import split as commandSplit
import re
import yaml
import time

config = ConfigParser()
config.read('config.conf')

g5kConfig = config['g5k']
deployImg = str(g5kConfig['deploy.image.name'])
imageAddress = "https://s3.datapirates.ir/digvery/debian10-spark-namb.tgz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=dLThTJ8J%2F20200209%2F%2Fs3%2Faws4_request&X-Amz-Date=20200209T122327Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=b4c5978f8c89a0ebb3111e16354ebb02644a80348539bc8572f2212273cf431d"
userName = str(g5kConfig['user.name'])
oarFile = str(g5kConfig['oar.file.location'])
multiCluster = str(g5kConfig['multi.cluster']) in "yes"

java8Directory = str(g5kConfig['java8.directory'])
sparkDirectory = str(g5kConfig['spark.directory'])


### Config Java Version in Front-end
os.system('export JAVA_HOME="{}";export PATH=$JAVA_HOME/bin:$PATH;java -version;'.format(java8Directory))

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
kadeployArgs = commandSplit(kadeployCommad)
kadeployProcess = subprocess.Popen(kadeployArgs, stderr=stderr, stdout=stdout)
kadeployProcess.communicate()

masterNode = clusterNodes.pop(0)
print(masterNode)
masterNode = sh.ShellHandler(masterNode, "root")
## Setting Correct Java Version
masterNode.execute('export JAVA_HOME="/root/java";export PATH=$JAVA_HOME/bin:$PATH;java -version;')
## get master IP
shin, shout, sherr = masterNode.execute("ip route get 1.2.3.4 | awk '{print $7}'")
masterIP = re.sub(r'\n','',shout[0])
masterAddress = "spark://{}:7077".format(str(masterIP))
# ## Running Mater
masterNode.execute("nohup ./spark/bin/spark-class org.apache.spark.deploy.master.Master &")
print("check check check")
time.sleep(180)

for node in clusterNodes:
    print("running on worker : {}".format(node))
    worker = sh.ShellHandler(node, "root")
    worker.execute('export JAVA_HOME="/root/java";export PATH=$JAVA_HOME/bin:$PATH;java -version;')
    masterNode.execute("nohup ./spark/bin/spark-class org.apache.spark.deploy.worker.Worker {} &".format(masterAddress))
    print("success on {}".format(node))
    time.sleep(30)

## Modify Spark Config File
print("Right now master is : {}".format(masterAddress))
with open("namb/config/spark-benchmark.yml", "r+") as f:
     old = f.read() # read everything in the file
     f.seek(0)
     print(masterAddress)
     old = re.sub(r'master: (\w+)\n','master: {}\n'.format(masterAddress), old)
     print("And I write this to conf file : {}".format(old))
     f.write(old) # write the new line before
    
# ### Run Namb Application
majid = sparkDirectory + "/bin/spark-submit" + " --class fr.unice.namb.spark.BenchmarkApplication" + " --master {}".format(masterAddress) + " /home/smirmoeini/g5k-spark-cluster/namb/spark-namb.jar" + " /home/smirmoeini/g5k-spark-cluster/namb/config/workflow_schema.yml" + " /home/smirmoeini/g5k-spark-cluster/namb/config/spark-benchmark.yml"
print(majid)
os.system(majid)

    

    

    
    

