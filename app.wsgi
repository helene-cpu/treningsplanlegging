import sys
import site
import os

site.addsitedir('/var/www/trening/env/lib/python3.13/site-packages')

sys.path.insert(0, '/var/www/trening')

os.chdir('/var/www/trening')

os.environ['VIRTUAL_ENV'] = '/var/www/trening/env'
os.environ['PATH'] = '/var/www/trening/env/bin:' + os.environ['PATH']

from app import app as application
