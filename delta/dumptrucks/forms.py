from django import forms
from .models import Downtime, Operator, DumpTruck, FailureReason
from django_jalali.forms import jDateField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django_select2.forms import Select2Widget

class DowntimeForm(forms.ModelForm):
    start_date = jDateField(label="تاریخ شروع", widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    end_date = jDateField(label="تاریخ پایان", widget=forms.TextInput(attrs={'placeholder': 'YYYY/MM/DD'}))
    start_time = forms.TimeField(label="زمان شروع", widget=forms.TimeInput(attrs={'class': 'timepicker'}))
    end_time = forms.TimeField(label="زمان پایان", widget=forms.TimeInput(attrs={'class': 'timepicker'}))
    operator = forms.ModelChoiceField(
        queryset=Operator.objects.all(),
        widget=Select2Widget,
        label="اپراتور"
    )
    dump_truck = forms.ModelChoiceField(
        queryset=DumpTruck.objects.all(),
        widget=Select2Widget,
        label="دامپ تراک"
    )
    reason = forms.ModelChoiceField(
        queryset=FailureReason.objects.all(),
        widget=Select2Widget,
        label="علت خرابی"
    )

    class Meta:
        model = Downtime
        fields = ['operator', 'dump_truck', 'start_date', 'start_time', 'end_date', 'end_time', 'reason', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('operator'),
            Field('dump_truck'),
            Field('start_date'),
            Field('start_time'),
            Field('end_date'),
            Field('end_time'),
            Field('reason'),
            Field('description'),
            Field('is_active'),
            Submit('submit', 'ذخیره')
        )

class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['personnel_code', 'first_name', 'last_name', 'group', 'position', 'phone_number']

class OperatorImportForm(forms.Form):
    file = forms.FileField(label='فایل اکسل')

class DumpTruckForm(forms.ModelForm):
    class Meta:
        model = DumpTruck
        fields = ['code', 'model', 'is_active', 'type']

class DumpTruckImportForm(forms.Form):
    file = forms.FileField(label='فایل اکسل')

class FailureReasonForm(forms.ModelForm):
    class Meta:
        model = FailureReason
        fields = ['name']

class FailureReasonImportForm(forms.Form):
    file = forms.FileField(label='فایل اکسل')
