import re
import os

majid = os.popen("ip route get 1.2.3.4 | awk '{print $7}'").read()
print(majid)
farzam = re.sub(r'\n','',majid)
print(farzam)
