from django import forms
from .models import Person, TicketAllocation, Fixture

class PasscodeForm(forms.Form):
    passcode = forms.CharField(widget=forms.PasswordInput)

class PersonChoiceForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.filter(active=True), empty_label=None)

class AllocationForm(forms.ModelForm):
    class Meta:
        model = TicketAllocation
        fields = ['assigned_to','transfer_status','payment_status','price','paid_to','notes']


class PersonCreateForm(forms.ModelForm):
    bank_details = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Person
        fields = ['name', 'short_name', 'notes']


class FixtureCreateForm(forms.ModelForm):
    class Meta:
        model = Fixture
        fields = ['date', 'opponent', 'competition', 'kick_off', 'result', 'category', 'face_value', 'notes']
