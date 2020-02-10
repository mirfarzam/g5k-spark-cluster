import re
masterAddress = "spark://172.16.130.11:7077"
with open("namb/config/spark-benchmark.yml", "r+") as f:
     old = f.read() # read everything in the file
     print(old)
     print("\n\n")
     f.seek(0)
     old = re.sub(r'master: (\w+)\n','master: {}\n'.format(masterAddress), old)
     f.write(old) # write the new line before
     # print(old)