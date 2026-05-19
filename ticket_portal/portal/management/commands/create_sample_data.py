from django.core.management.base import BaseCommand
from portal.models import Person, Seat, Fixture, TicketAllocation
from datetime import date
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        p1,_=Person.objects.get_or_create(name='Alex',short_name='Alex'); p2,_=Person.objects.get_or_create(name='Sam',short_name='Sam')
        s1,_=Seat.objects.get_or_create(label='Block 107 Row 8 Seat 454',defaults={'block':'107','row':'8','seat_number':'454'})
        s2,_=Seat.objects.get_or_create(label='Block 107 Row 8 Seat 455',defaults={'block':'107','row':'8','seat_number':'455'})
        f,_=Fixture.objects.get_or_create(date=date.today(),opponent='Spurs',defaults={'competition':'PL','category':'A'})
        TicketAllocation.objects.get_or_create(fixture=f,seat=s1,defaults={'assigned_to':p1,'payment_status':'unpaid','transfer_status':'pending'})
        TicketAllocation.objects.get_or_create(fixture=f,seat=s2,defaults={'assigned_to':p2,'payment_status':'paid','transfer_status':'transferred'})
