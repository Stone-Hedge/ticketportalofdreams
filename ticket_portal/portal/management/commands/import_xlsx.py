from django.core.management.base import BaseCommand
from portal.utils import import_workbook
class Command(BaseCommand):
    def add_arguments(self,parser): parser.add_argument('path')
    def handle(self,*args,**opts): self.stdout.write(str(import_workbook(opts['path'])))
