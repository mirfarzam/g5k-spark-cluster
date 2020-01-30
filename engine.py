import os
import subprocess
import paramiko


# oarsub -I -t deploy -l {"rconsole='YES'"}/nodes=1,walltime=3
# kadeploy3 -e debian10-x64-base -f $OAR_FILE_NODES -k
# $OAR_FILE_NODES
# ssh root@node.site.grid5000.fr

# Accessing to Grid 5000 
print("Connecting to Grid 5000 ...")
g5kInterface = paramiko.SSHClient()
g5kInterface.load_system_host_keys()
g5kInterface.connect('access.grid5000.fr', username='smirmoeini')
print("Connection Successful to Grid 5000 ...")


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
print("Connection Successful to Frontend ...")

stdin, stdout, stderr = frontend.exec_command("ls") #edited#

print(stdout.read())

