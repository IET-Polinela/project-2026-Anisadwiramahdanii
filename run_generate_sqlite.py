import os
import sys

# Use SQLite for this run
os.environ['USE_SQLITE'] = '1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_app.settings')

import django
from django.core.management import call_command

django.setup()

count = 1000
try:
    call_command('generate_data', str(count))
    print(f'DONE: generated {count} records (SQLite)')
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
