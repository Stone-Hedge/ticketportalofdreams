from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=120, unique=True)
    short_name = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    def __str__(self): return self.short_name or self.name

class Seat(models.Model):
    block = models.CharField(max_length=20)
    row = models.CharField(max_length=20)
    seat_number = models.CharField(max_length=20)
    label = models.CharField(max_length=120, unique=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    def __str__(self): return self.label

class Fixture(models.Model):
    date = models.DateField()
    opponent = models.CharField(max_length=120)
    competition = models.CharField(max_length=120, blank=True)
    kick_off = models.TimeField(null=True, blank=True)
    result = models.CharField(max_length=40, blank=True)
    category = models.CharField(max_length=30, blank=True)
    face_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    moon_phase = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

class TicketAllocation(models.Model):
    TRANSFER_CHOICES = [(x, x.replace('_', ' ').title()) for x in ['not_required','pending','transferred','listed_on_exchange','cancelled','unknown']]
    PAYMENT_CHOICES = [(x, x.replace('_', ' ').title()) for x in ['not_required','unpaid','paid','waived','unknown']]
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_allocations')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    transfer_status = models.CharField(max_length=30, choices=TRANSFER_CHOICES, default='unknown')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='unknown')
    paid_to = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='paid_allocations')
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['fixture','seat'], name='uniq_fixture_seat')]

class AuditEvent(models.Model):
    actor_name = models.CharField(max_length=120)
    action = models.CharField(max_length=120)
    entity_type = models.CharField(max_length=60)
    entity_id = models.PositiveIntegerField()
    before_json = models.JSONField(null=True, blank=True)
    after_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SensitiveDetail(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    arsenal_membership_number = models.CharField(max_length=100, blank=True)
    bank_details = models.TextField(blank=True)
    notes = models.TextField(blank=True)
