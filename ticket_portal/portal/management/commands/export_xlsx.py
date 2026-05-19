from django.core.management.base import BaseCommand
from portal.utils import export_xlsx, export_csv
class Command(BaseCommand):
    def add_arguments(self,p): p.add_argument('path'); p.add_argument('--csv', action='store_true')
    def handle(self,*args,**o):
        export_csv(o['path']) if o['csv'] else export_xlsx(o['path'])
