from django.test import TestCase, Client
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from django.test.utils import override_settings
from datetime import date
from pathlib import Path
from openpyxl import Workbook
from .models import *

class PortalTests(TestCase):
    def setUp(self):
        self.p=Person.objects.create(name='Alex',short_name='A')
        self.s=Seat.objects.create(block='1',row='1',seat_number='1',label='B1R1S1')
        self.f=Fixture.objects.create(date=date.today(),opponent='Chelsea')
        self.a=TicketAllocation.objects.create(fixture=self.f, seat=self.s)
    def test_model_creation(self): self.assertEqual(Person.objects.count(),1)
    def test_unique_allocation(self):
        with self.assertRaises(Exception): TicketAllocation.objects.create(fixture=self.f, seat=self.s)
    @override_settings(GENERAL_PASSCODE_HASH=make_password('g'), ADMIN_PASSCODE_HASH=make_password('a'))
    def test_passcode_flow(self):
        c=Client(); r=c.post('/passcode/',{'passcode':'g'}); self.assertEqual(r.status_code,302)
    @override_settings(GENERAL_PASSCODE_HASH=make_password('g'), ADMIN_PASSCODE_HASH=make_password('a'))
    def test_admin_flow(self):
        c=Client(); c.post('/passcode/',{'passcode':'a'}); self.assertEqual(c.get('/admin-portal/').status_code,200)
    def test_update_creates_audit(self):
        c=Client(); s=c.session; s['general_access']=True; s['actor_name']='Alex'; s.save()
        c.post(f'/allocation/{self.a.id}/update/',{'assigned_to':self.p.id,'transfer_status':'pending','payment_status':'unpaid','price':'10.00','paid_to':'','notes':''})
        self.assertEqual(AuditEvent.objects.count(),1)
    def test_import_export(self):
        wb=Workbook(); ws=wb.active; ws.title='SEATS'; ws.append(['date','opponent','competition','kick_off','category','face_value','Block 1 Row 1 Seat 1']); ws.append([date.today().isoformat(),'Everton','','','A','','Alex'])
        d=wb.create_sheet('DETAILS'); d.append(['name','membership','bank','notes']); d.append(['Alex','123','bank','n'])
        p=Path('tmp.xlsx'); wb.save(p)
        call_command('import_xlsx', str(p))
        out=Path('out.xlsx'); call_command('export_xlsx',str(out)); self.assertTrue(out.exists())
