from configparser import ConfigParser

config = ConfigParser()
config.read('config.conf')

g5kConfig = config['g5k']
deployImg = str(g5kConfig['deploy.image.name'])
userName = str(g5kConfig['user.name'])
oarFile = str(g5kConfig['oar.file.location'])
multiCluster = str(g5kConfig['multi.cluster']) in "yes"
