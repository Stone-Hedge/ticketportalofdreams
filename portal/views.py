from pathlib import Path
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import PasscodeForm, PersonChoiceForm, AllocationForm
from .models import Person, Seat, Fixture, TicketAllocation, AuditEvent
from .utils import import_workbook, export_xlsx, export_csv


def _require_general(request):
    return request.session.get('general_access')
def _require_admin(request):
    return request.session.get('admin_access')
def home(request): return redirect('fixtures' if _require_general(request) else 'passcode')
def healthcheck(request): return JsonResponse({'status':'ok'})
def robots(request): return HttpResponse('User-agent: *\nDisallow: /\n', content_type='text/plain')

def passcode_view(request):
    form = PasscodeForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        code=form.cleaned_data['passcode']
        if check_password(code, settings.GENERAL_PASSCODE_HASH) or check_password(code, settings.ADMIN_PASSCODE_HASH):
            request.session['general_access']=True
            if check_password(code, settings.ADMIN_PASSCODE_HASH): request.session['admin_access']=True
            request.session['passcode_failures']=0
            return redirect('choose_person')
        request.session['passcode_failures']=request.session.get('passcode_failures',0)+1
        if request.session['passcode_failures']>=5:
            from django.utils import timezone
            request.session['passcode_lock_until']=timezone.now().timestamp()+300
    return render(request,'portal/passcode.html',{'form':form})

def choose_person(request):
    if not _require_general(request): return redirect('passcode')
    form=PersonChoiceForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        request.session['actor_name']=form.cleaned_data['person'].name
        return redirect('fixtures')
    return render(request,'portal/choose_person.html',{'form':form})

def change_person(request): request.session.pop('actor_name',None); return redirect('choose_person')

def fixtures_board(request):
    if not _require_general(request): return redirect('passcode')
    seats=list(Seat.objects.filter(active=True)); fixtures=list(Fixture.objects.all().order_by('date'))
    matrix={(a.fixture_id,a.seat_id):a for a in TicketAllocation.objects.select_related('assigned_to').all()}
    rows=[(f,[matrix.get((f.id,s.id)) for s in seats]) for f in fixtures]
    return render(request,'portal/fixtures.html',{'seats':seats,'rows':rows,'cell_class':_cell_class})

def fixture_detail(request, fixture_id):
    if not _require_general(request): return redirect('passcode')
    fixture=get_object_or_404(Fixture,id=fixture_id)
    allocs=TicketAllocation.objects.filter(fixture=fixture).select_related('seat','assigned_to')
    audits=AuditEvent.objects.filter(entity_type='TicketAllocation').order_by('-created_at')[:30]
    return render(request,'portal/fixture_detail.html',{'fixture':fixture,'allocs':allocs,'audits':audits})

def _cell_class(a):
    if not a.assigned_to: return 'state-grey'
    if a.transfer_status=='cancelled': return 'state-red'
    if a.transfer_status=='pending': return 'state-blue'
    if a.transfer_status=='transferred' and a.payment_status=='paid': return 'state-green'
    if a.payment_status=='unpaid': return 'state-amber'
    return 'state-grey'
def edit_allocation(request, allocation_id):
    if not _require_general(request): return HttpResponse(status=403)
    a=get_object_or_404(TicketAllocation,id=allocation_id); form=AllocationForm(instance=a)
    return render(request,'portal/_allocation_form.html',{'form':form,'allocation':a})
@require_http_methods(['POST'])
def update_allocation(request, allocation_id):
    if not _require_general(request): return HttpResponse(status=403)
    a=get_object_or_404(TicketAllocation,id=allocation_id); before={'assigned_to':a.assigned_to_id,'transfer_status':a.transfer_status,'payment_status':a.payment_status,'price':str(a.price or '')}
    form=AllocationForm(request.POST, instance=a)
    if form.is_valid():
        a=form.save(); after={'assigned_to':a.assigned_to_id,'transfer_status':a.transfer_status,'payment_status':a.payment_status,'price':str(a.price or '')}
        AuditEvent.objects.create(actor_name=request.session.get('actor_name','Unknown'), action='update_allocation', entity_type='TicketAllocation', entity_id=a.id, before_json=before, after_json=after)
    return render(request,'portal/_allocation_cell.html',{'a':a,'cell_class':_cell_class(a)})

def dashboard(request):
    return render(request,'portal/dashboard.html')
def dashboard_available(request): return render(request,'portal/simple_list.html',{'title':'Available Tickets','items':TicketAllocation.objects.filter(assigned_to__isnull=True)})
def dashboard_unpaid(request): return render(request,'portal/simple_list.html',{'title':'Unpaid Tickets','items':TicketAllocation.objects.filter(payment_status='unpaid')})
def dashboard_transfers(request): return render(request,'portal/simple_list.html',{'title':'Not Yet Transferred','items':TicketAllocation.objects.exclude(transfer_status='transferred')})
def dashboard_fairness(request):
    people = Person.objects.annotate(total=Count('assigned_allocations'), big=Count('assigned_allocations', filter=Q(assigned_allocations__fixture__category__icontains='A')))
    return render(request,'portal/fairness.html',{'people':people})
def audit_log(request): return render(request,'portal/audit.html',{'events':AuditEvent.objects.order_by('-created_at')[:200]})
def admin_portal(request):
    if not _require_admin(request): return HttpResponse(status=403)
    return render(request,'portal/admin_portal.html')
def admin_import(request):
    if not _require_admin(request): return HttpResponse(status=403)
    report=None
    if request.method=='POST' and request.FILES.get('xlsx'):
        p=Path(settings.DATA_DIR)/request.FILES['xlsx'].name
        with open(p,'wb') as f:
            for c in request.FILES['xlsx'].chunks(): f.write(c)
        report=import_workbook(p)
    return render(request,'portal/admin_import.html',{'report':report})
def admin_export(request):
    if not _require_admin(request): return HttpResponse(status=403)
    if request.GET.get('fmt')=='xlsx':
        p=Path(settings.DATA_DIR)/'export.xlsx'; export_xlsx(p); return FileResponse(open(p,'rb'), as_attachment=True, filename='export.xlsx')
    if request.GET.get('fmt')=='csv':
        p=Path(settings.DATA_DIR)/'export.csv'; export_csv(p); return FileResponse(open(p,'rb'), as_attachment=True, filename='export.csv')
    return render(request,'portal/admin_export.html')
