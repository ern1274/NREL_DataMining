from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


year_max_limit = 2022
year_min_limit = 2010
forms_attributes = (("ghi","GHI"),
              ("dhi","DHI"),
              ("dni","DNI"),
              ("wind_speed","Wind Speed"),
              ("air_temperature","Air Temperature"),
              ("solar_zenith_angle","Solar Zenith Angle"))
forms_attributes_string = "ghi," + "dhi," +"dni," + "wind_speed," + "air_temperature,"+ "solar_zenith_angle"

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
    all_attributes_data = forms.BooleanField(label="All Attributes")
    all_attributes_data.required = False
    attributes_data = forms.MultipleChoiceField(label="Select Attributes to view (ignore if selected all)",choices=forms_attributes,widget=forms.CheckboxSelectMultiple)
    attributes_data.required = False
    year_data = forms.IntegerField(label="Get data from years")

    def clean_attributes_data(self):
        data = self.cleaned_data['attributes_data']
        data_string = ''
        for attribute in data:
            if data_string != '':
                data_string += ","
            data_string += attribute
        data = data_string
        return data

    def clean_year_data(self):
        data = self.cleaned_data['year_data']
        if data > year_max_limit:
            raise ValidationError(_('Years must be between ' + str(year_min_limit) + " and " + str(year_max_limit)))
        if data < year_min_limit:
            raise ValidationError(_('Years must be between ' + str(year_min_limit) + " and " + str(year_max_limit)))
        return data

    leapYear_data = forms.BooleanField(label="Include Leap Year?")
    leapYear_data.required = False

    interval_data = forms.ChoiceField(label= "Select Interval (Minutes) ",choices=(("30","30"),("60","60")))

    utc_data = forms.BooleanField(label="Use UTC data points?")
    utc_data.required = False

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
            raise ValidationError(_('Invalid email, must include "@" '))
        return data

class attributeFilterForm(forms.Form):
    attribute_data = forms.ChoiceField(label="Select Attributes to filter data by",required=False, choices=forms_attributes,widget=forms.RadioSelect)
    def clean_attribute_data(self):
        data = self.cleaned_data['attribute_data']
        if data == "wind_speed":
            data = "Wind Speed"
        elif data == "air_temperature":
            data = "Temperature"
        elif data == "solar_zenith_angle":
            data = "Solar Zenith Angle"
        else:
            data = data.upper()
        return data


