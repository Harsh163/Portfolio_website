# dump_utf8.py

from django.core.management import call_command
import io

with io.open('mysql_backup.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', format='json', indent=2, stdout=f)
