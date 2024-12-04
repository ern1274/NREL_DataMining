from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

year_max_limit = 2022
year_min_limit = 2010
attributes = (("all","all"),
              ("ghi","ghi"),
              ("dhi","dhi"),
              ("dni","dni"),
              ("wind_speed","wind_speed"),
              ("air_temperature","air_temperature"),
              ("solar_zenith_angle","solar_zenith_angle"))

class geocodeForm(forms.Form):
    country_data = forms.CharField(help_text="Enter a Country in its abbreviated form")
    def clean_country_data(self):
        data = self.cleaned_data['country_data']
        data.upper()
        return data
    region_data = forms.CharField(help_text="Enter Region name")
    def clean_region_data(self):
        data = self.cleaned_data['region_data']
        data.lower()
        return data

class exportForm(forms.Form):

    attributes_data = forms.MultipleChoiceField(choices=attributes)
    year_data = forms.IntegerField()

    def clean_year_data(self):
        data = self.cleaned_data['year_data']
        if data > year_max_limit:
            raise ValidationError(_('Invalid year - data not available for year'))
        if data < year_min_limit:
            raise ValidationError(_('Invalid year - data not available for year'))
        return data

    leapYear_data = forms.BooleanField()

    interval_data = forms.ChoiceField(choices=(("30","30"),("60","60")))

    utc_data = forms.BooleanField()


    name_data = forms.CharField()
    name_data.required = False


    def clean_name_data(self):
        data = self.cleaned_data['name_data']
        data.lower()
        return data

    reason_data = forms.CharField()
    reason_data.required = False
    def clean_reason_data(self):
        data = self.cleaned_data['reason_data']
        data.lower()
        return data

    affiliation_data = forms.CharField()
    affiliation_data.required = False
    def clean_affiliation_data(self):
        data = self.cleaned_data['affiliation_data']
        data.lower()
        return data
    email_data = forms.CharField()
    def clean_email_data(self):
        data = self.cleaned_data['email_data']
        if not "@" in data:
            raise ValidationError(_('Invalid email'))
        return data

class attributeFilterForm(forms.Form):
    attributes_data = forms.MultipleChoiceField(choices=attributes)
