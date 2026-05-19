from django import forms
from .models import Person, TicketAllocation

class PasscodeForm(forms.Form):
    passcode = forms.CharField(widget=forms.PasswordInput)

class PersonChoiceForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.filter(active=True), empty_label=None)

class AllocationForm(forms.ModelForm):
    class Meta:
        model = TicketAllocation
        fields = ['assigned_to','transfer_status','payment_status','price','paid_to','notes']
