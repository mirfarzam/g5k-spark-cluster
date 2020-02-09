from configparser import ConfigParser
import os

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

# Download the image
# os.system('curl -o images/debian10-spark-base.tgz {}'.format(imageAddress)) 

