from datetime import datetime, timedelta
import time

old = datetime.now().replace(microsecond=0)
time.sleep(1)

timeCheck = datetime.now() - timedelta(seconds=1)
timeCheck = timeCheck.replace(microsecond=0)
print(old)
print(timeCheck)
print(old <= timeCheck)