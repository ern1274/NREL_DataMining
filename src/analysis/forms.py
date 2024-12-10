from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

year_max_limit = 2022
year_min_limit = 2010
attributes = (("all","all"),
              ("ghi","GHI"),
              ("dhi","DHI"),
              ("dni","DNI"),
              ("wind_speed","Wind Speed"),
              ("air_temperature","Air Temperature"),
              ("solar_zenith_angle","Solar Zenith Angle"))

class geocodeForm(forms.Form):
    country_data = forms.CharField(label="Enter a Country in its abbreviated form")
    def clean_country_data(self):
        data = self.cleaned_data['country_data']
        data.upper()
        return data
    region_data = forms.CharField(label="Enter Region name")
    def clean_region_data(self):
        data = self.cleaned_data['region_data']
        data.lower()
        return data


class exportForm(forms.Form):

    attributes_data = forms.MultipleChoiceField(label="Select Attributes to view",choices=attributes)
    year_data = forms.IntegerField(label="Get data from years")

    def clean_year_data(self):
        data = self.cleaned_data['year_data']
        if data > year_max_limit:
            raise ValidationError(_('Invalid year - data not available for year'))
        if data < year_min_limit:
            raise ValidationError(_('Invalid year - data not available for year'))
        return data

    leapYear_data = forms.BooleanField(label="Include Leap Year?")

    interval_data = forms.ChoiceField(label= "Select Interval (Minutes) ",choices=(("30","30"),("60","60")))

    utc_data = forms.BooleanField(label="Use UTC data points?")


    name_data = forms.CharField(label="Name (Not Required)")
    name_data.required = False


    def clean_name_data(self):
        data = self.cleaned_data['name_data']
        data.lower()
        return data

    reason_data = forms.CharField(label="Reason (Not Required)")
    reason_data.required = False
    def clean_reason_data(self):
        data = self.cleaned_data['reason_data']
        data.lower()
        return data

    affiliation_data = forms.CharField(label="Affiliation (Not Required)")
    affiliation_data.required = False
    def clean_affiliation_data(self):
        data = self.cleaned_data['affiliation_data']
        data.lower()
        return data
    email_data = forms.CharField(label="Email ")
    def clean_email_data(self):
        data = self.cleaned_data['email_data']
        if not "@" in data:
            raise ValidationError(_('Invalid email'))
        return data

class attributeFilterForm(forms.Form):
    attributes_data = forms.MultipleChoiceField(label="Select Attributes to filter data by",choices=attributes)
