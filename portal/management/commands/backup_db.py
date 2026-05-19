from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from shutil import copy2
from datetime import datetime
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        out=Path(settings.DATA_DIR)/f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.sqlite3"; copy2(settings.DATABASES['default']['NAME'], out); self.stdout.write(str(out))
