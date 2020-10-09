from datetime import datetime
from subprocess import Popen

now=datetime.now()
dt_string = now.strftime("%d%m%Y_%H%M%S")
Process=Popen('./gitpush.sh %s' % (str(dt_string),), shell=True)
