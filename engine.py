import os
import subprocess
import paramiko
import re
import ShellHandler as sh


numberOfNodes = 1
imageAddress = 'https://s3.datapirates.ir/digvery/debian10-spark-namb.tgz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=dLThTJ8J%2F20200130%2F%2Fs3%2Faws4_request&X-Amz-Date=20200130T153817Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=684a67871a21b1a63ccb5bf46b8ae1f202476c3398cf1e3353a562cc05c802d1'


# oarsub -I -t deploy -l {"rconsole='YES'"}/nodes=1,walltime=3
# kadeploy3 -e debian10-x64-base -f $OAR_FILE_NODES -k
# $OAR_FILE_NODES

#  kadeploy3 -f $OAR_NODEFILE -a images/debian10-spark-base.env 

# ssh root@node.site.grid5000.fr

# Accessing to Grid 5000 
# print("Connecting to Grid 5000 ...")
g5kInterface = paramiko.SSHClient()
g5kInterface.load_system_host_keys()
g5kInterface.connect('access.grid5000.fr', username='smirmoeini')
g5kInterfaceShell = g5kInterface.invoke_shell()
# print("Connection Successful to Grid 5000 ...")


# Making a Channel for nested ssh
vmtransport = g5kInterface.get_transport()
frontend_addr = ('Sophia', 22) 
init_addr = ('access.grid5000.fr', 22) 
frontendChannel = vmtransport.open_channel("direct-tcpip", frontend_addr, init_addr)

# Accessing to Front-End
print("Connecting to Frontend ...")
frontend = paramiko.SSHClient()
frontend.set_missing_host_key_policy(paramiko.AutoAddPolicy())
frontend.connect('Sophia', username='smirmoeini', sock=frontendChannel)
frontendShell = frontend.invoke_shell()
frontin = channel.makefile('wb')
frontout = channel.makefile('r')

# frontend = sh.ShellHandler(host='Sophia', user='smirmoeini', channel = frontendChannel)

# print("Connection Successful to Frontend ...")

make image ready on front-end node
stdin, stdout, stderr = frontend.exec_command('mkdir images') 
os.system('scp images/debian10-spark-base.env smirmoeini@access.grid5000.fr:sophia/images/debian10-spark-base.env')
print("please wait for dowloading the image, it takes few minutes ...")
frontend.execute('curl -o images/debian10-spark-base.tgz {}'.format(imageAddress)) 
print("image downloaded successfully")

# requesting for nodes
# shin, shout, sherr = frontend.execute('oarsub -t deploy -l nodes={} walltime=3; cat $OAR_FILE_NODES'.format(numberOfNodes)) 
# OAR_JOB_ID = shout[-1].strip()
# OAR_JOB_ID = (re.findall(r'OAR_JOB_ID=(\d+)', OAR_JOB_ID))[0]
# frontend.execute('cat $OAR_FILE_NODES') 
frontendShell.execute('ls') 
# frontend.execute('cat /var/lib/oar/{}'.format(OAR_JOB_ID)) 
# if(len(stderr.readlines()) != 0):
#     print(stderr.read());
#     print(stdout.read());



# OAR_FILE_NODES = '/var/lib/oar/{}'.format(OAR_JOB_ID)
# stdin, stdout, stderr = frontend.exec_command('cat {}'.format(OAR_FILE_NODES)) 

# print(stdout.readlines())
# print(stderr.readlines())

# stdin, stdout, stderr = frontend.exec_command('cat $OAR_FILE_NODES')
# jobNumber = (re.findall(r'OAR_JOB_ID=(\d+)', (stdout.readlines())[-1]))

# stdin, stdout, stderr = frontend.exec_command('cat {}'.format(OAR_FILE_NODES)) 
# listNodes = ((str(stdout.read())[2:])[:-1]).split("\\n")[:-1]
# listNodes = list(dict.fromkeys(listNodes))
# print(jobNumber)
# print(stderr.readlines())

# stdin, stdout, stderr = frontend.exec_command('echo $OAR_FILE_NODES') 
# print(stdout.readlines())
# print(stderr.readlines())





# run the environment on those nodes

# print("running environment on nodes")
# stdin, stdout, stderr = frontend.exec_command('cd images/')
# stdin, stdout, stderr = frontend.exec_command('pwd') 
# print(stdout.readlines())


# print("running environment on nodes")

# stdin, stdout, stderr = frontend.exec_command('kadeploy3 -f $OAR_NODEFILE -e debian10-spark-base') 
# print("runned environment correctly and these are the nodes : ")
# print(stderr.read())
# print(stdout.read())





# index = 0
# for i in listNodes[:-1]:
#     if index == 0:
#         print("running master on {}".format(i))
#     else:
#         print("running worker-{} on {}".format(index, i))
    
    


# frontend.close()
# g5kInterface.close()