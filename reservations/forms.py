from django import forms

class AvailabilityForm(forms.Form):
    start_time = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    end_time = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class AcceptForm(forms.Form):
    MAKEUP_STATUS = (
        ('d', 'Default'),
        ('r', 'Request'),
        ('a', 'Accept'),
        ('c', 'Completed'),
    )
    status = forms.ChoiceField(choices=MAKEUP_STATUS, required=True)